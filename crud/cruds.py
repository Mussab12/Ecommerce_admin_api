from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from models import models
from schemas import schema
from utils.utilities import validate
from datetime import datetime, timedelta
from datetime import date

# Product Cruds

def update_product_handler(db: Session, product_id: int, updated_product: schema.ProductBase):
    try:
        current_product = get_product_byid_handler(db,product_id)
        if current_product:
            current_product.name = updated_product.name
            current_product.description = updated_product.description
            current_product.price = updated_product.price
            db.commit()
            db.refresh(current_product)
        return current_product
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )


def create_product_handler(db: Session, new_product: schema.ProductBase):
    try:
        product = models.Products(name=new_product.name, description=new_product.description, price=new_product.price)
        if product is not None:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product already exists: {str(e)}"
            )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


# Get All products
def get_all_products_handler(db: Session):
    try:
        products = db.query(models.Products).all()
        return products
    except Exception as e:
        error_message = f"Error creating product: {str(e)}"
        validate(None, 500, error_message)
          

def get_product_byid_handler(db: Session, product_id: int):
    product = db.query(models.Products).filter(models.Products.id == product_id).first()
    validate(product, 404, 'Product not found')
    return product

def delete_product_handler(db:Session,product_id:int):
    try:
      product=db.query(models.Products).filter(models.Products.id==product_id).first()
      db.delete(product)
      db.commit()
      return {"deleted"}
    except Exception as e:
        error_message = f"Error creating product: {str(e)}"
        validate(None, 500, error_message)



def get_revenue_by_period_handler(db: Session, period: str, category: str = None):
    end_date = datetime.utcnow()
    
    if period == 'daily':
        start_date = end_date - timedelta(days=1)
    elif period == 'weekly':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = end_date - timedelta(weeks=4)
    elif period == 'annual':
        start_date = end_date - timedelta(days=365)
    else:
        raise ValueError("Invalid period")

    products_query = db.query(models.Products)

    if category:
        products_query = products_query.filter(models.Products.name.like(f"%{category}%"))

    products = products_query.all()

    revenue_data = []
    for product in products:
        revenue = product.calculate_revenue(start_date, end_date)
        revenue_data.append({"product_name": product.name, "revenue": revenue})

    return revenue_data





# Inventory Crud

def get_inventory_by_productid_handler(db: Session, product_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()


def add_product_to_inventory_handler(db: Session, product: models.Products, quantity: int,LOW_STOCK_THRESHOLD):
    # Create a new Inventory record and associate it with the product
    inventory_item = models.Inventory(product_id=product.id, quantity=quantity)
    try:
      if inventory_item is not None:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product already exists: {str(e)}"
            )
      db.add(inventory_item)
      db.commit()
    # Refresh the product object to include the updated relationship
      db.refresh(product)

    # Check for low stock and update the is_low_stock flag
      if inventory_item.quantity < LOW_STOCK_THRESHOLD:
        inventory_item.is_low_stock = True
      else:
        inventory_item.is_low_stock = False

      db.commit()

      return inventory_item
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


def update_inventory_handler(db: Session, inventory_id: int, quantity: int,LOW_STOCK_THRESHOLD):
    # Retrieve the inventory item using its ID
    inventory_item = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    # Update the quantity
    inventory_item.quantity = quantity
    db.commit()
    db.refresh(inventory_item)
    # Check for low stock and update the is_low_stock flag
    if inventory_item.quantity < LOW_STOCK_THRESHOLD:
        inventory_item.is_low_stock = True
    else:
        inventory_item.is_low_stock = False
    db.commit()
    return inventory_item




def delete_inventory_handler(db:Session,inventory_id:int):
    try:
      product=db.query(models.Inventory).filter(models.Inventory.id==inventory_id).first()
      db.delete(product)
      db.commit()
      return {"deleted"}
    except Exception as e:
        error_message = f"Error creating product: {str(e)}"
        validate(None, 500, error_message)


# Sales Crud



def add_productsales_handler(db: Session,product: models.Products,quantity:id,sale_date:date):
    # Create a new Inventory record and associate it with the product
    product_sales = models.Sales(product_id=product.id,quantity=quantity,sale_date=sale_date)
    db.add(product_sales)
    db.commit()
    # Refresh the product object to include the updated relationship
    db.refresh(product)
    return product_sales


# Get All Sales
def get_allsales_handler(db: Session):
    try:
        sales = db.query(models.Sales).all()
        return sales
    except Exception as e:
        error_message = f"Error creating product: {str(e)}"
        validate(None, 500, error_message)

def get_sales_byid_handler(db: Session, sale_id: int):
    sales = db.query(models.Sales).filter(models.Sales.id == sale_id).first()
    validate(sales, 404, 'Sales not found')
    return sales


def update_sales_handler(db: Session, sale_id: int, sales: schema.SalesBase):
    try:
        current_sales = get_sales_byid_handler(db,sale_id)
        
        if current_sales:
            current_sales.quantity = sales.quantity
            current_sales.sale_date = sales.sale_date
            db.commit()
            db.refresh(current_sales)
        return current_sales
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )
    

def delete_sales_handler(db:Session,sales_id:int):
    try:
      sales=db.query(models.Sales).filter(models.Sales.id==sales_id).first()
      db.delete(sales)
      db.commit()
      return {"deleted"}
    except Exception as e:
        error_message = f"Error creating product: {str(e)}"
        validate(None, 500, error_message)    