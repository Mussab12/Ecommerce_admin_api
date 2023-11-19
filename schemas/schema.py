from pydantic import BaseModel
from datetime import date


class ProductBase(BaseModel):
    name:str
    description:str
    price:int


class InventoryBase(BaseModel):
    product_id:int
    quantity:int
    is_low_stock:bool
    

class SalesBase(BaseModel):
    product_id :int
    quantity:int
    sale_date:date