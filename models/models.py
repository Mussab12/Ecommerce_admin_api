from sqlalchemy import Boolean,Column,Integer,String,ForeignKey,Date
from sqlalchemy.orm import relationship
from db.database import Base



class Products(Base):
    __tablename__='products'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),index=True)
    description=Column(String(100))
    price=Column(Integer)    
    inventory = relationship("Inventory", back_populates="product")
    sales=relationship('Sales',back_populates='product')
    def calculate_revenue(self, start_date, end_date):
        # Convert datetime to date
        start_date = start_date.date()
        end_date = end_date.date()

        # Assuming 'sale_date' is a Date column in the Sales model
        relevant_sales = [sale for sale in self.sales if start_date <= sale.sale_date <= end_date]
        revenue = sum(sale.quantity * self.price for sale in relevant_sales)
        return revenue



class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    sale_date = Column(Date)
    product = relationship('Products', back_populates='sales')


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    is_low_stock = Column(Boolean, default=False)
    # Define a relationship with the Product model
    product = relationship("Products", back_populates="inventory")


# class InventoryStatus(Base):
#     __tablename__="inventorystatus"
#     id=Column(Integer,primary_key=True,index=True)