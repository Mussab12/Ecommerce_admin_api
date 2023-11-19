from fastapi import APIRouter,HTTPException,status,Query
from dependencies import dependencies
from models.models import Sales
from schemas import schema
from crud import cruds
from datetime import date

sales_route=APIRouter()

@sales_route.get("/sales")
async def get_sales_data_ByFilter(db:dependencies.db_dependency,start_date: str = Query(None, alias="startDate", description="Start date for filtering sales"),
        end_date: str = Query(None, alias="endDate", description="End date for filtering sales"),
        product_id: int = Query(None, description="Filter by product ID")):
    query = db.query(Sales)

    if start_date:
        query = query.filter(Sales.sale_date >= start_date)
    if end_date:
        query = query.filter(Sales.sale_date <= end_date)
    if product_id:
        query = query.filter(Sales.product_id == product_id)


    sales_data = query.all()
    return sales_data


# Get All Sales

@sales_route.get('/get_allsales/',status_code=status.HTTP_200_OK)
async def get_allsales(db:dependencies.db_dependency):
    sales = cruds.get_allsales_handler(db)
    return sales


# Get Sales By ID
@sales_route.get("/get_salebyid/{sale_id}",status_code=status.HTTP_200_OK)
def sales_by_id(sale_id: int,db: dependencies.db_dependency):
    sales = cruds.get_sales_byid_handler(db, sale_id)
    return sales


# Create Sales
@sales_route.post("/create_sales/{product_id}",status_code=status.HTTP_201_CREATED)
async def create_product(product_id:int,quantity:int,sale_date:date,db:dependencies.db_dependency):
    get_productid = cruds.get_product_byid_handler(db, product_id)
    
    sales=cruds.add_productsales_handler(db,get_productid,quantity,sale_date)

    return {"product":sales}


# Updating Sales

@sales_route.put('/update_sales/{product_id}',status_code=status.HTTP_200_OK)
async def update_sales(sales_id,sales:schema.SalesBase,db:dependencies.db_dependency):
    new_sales = cruds.update_sales_handler(db,sales_id,sales)
    return new_sales


# Deleting Sales
   
@sales_route.delete('/delete-sales/{sales_id}')
async def delete_product(sales_id:int,db:dependencies.db_dependency):
    sales=cruds.delete_sales_handler(db,sales_id)
    return {"sales":sales}