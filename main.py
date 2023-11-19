from fastapi import FastAPI
from models import models
from db.database import engine
from apis import product,inventory,sales
from fastapi.middleware.cors import CORSMiddleware



app=FastAPI()
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product.product_route)
app.include_router(inventory.inventory_route)
app.include_router(sales.sales_route)
models.Base.metadata.create_all(bind=engine)

   


@app.get('/')
def root_api():
    return{"message":"Welcome to Ecommerce App"}

    
