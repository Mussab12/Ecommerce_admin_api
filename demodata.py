from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from models.models import Products, Inventory, Sales
from datetime import datetime
import random
from faker import Faker

fake = Faker()

def create_demo_products(db: Session, num_products: int):
    product_types = ["TCL", "Samsung", "Oven", "Car Kits", "Headphones", "Laptop", "Tablet"]
    generated_names = set()

    for _ in range(num_products):
        product_type = random.choice(product_types)
        name = f"{product_type} {fake.word()}"

        # Ensure the name is unique
        while name in generated_names:
            name = f"{product_type} {fake.word()}"

        generated_names.add(name)

        description = f"Description for {name}"
        price = random.randint(100, 50000)
        db_product = Products(name=name, description=description, price=price)
        db.add(db_product)

    db.commit()

def create_demo_inventory(db: Session, products: list):
    for product in products:
        product_id = product.id
        quantity = random.randint(1, 100)
           
        # Adjust is_low_stock based on the quantity
        is_low_stock = 1 if quantity < 100 else 0
        db_inventory = Inventory(product_id=product_id, quantity=quantity, is_low_stock=is_low_stock)

        db.add(db_inventory)
    db.commit()

def create_demo_sales(db: Session, products: list):
    for product in products:
        product_id = product.id
        quantity = random.randint(1, 20)  # Adjust the range based on your requirements
        sale_date = fake.date_time_between(start_date='-30d', end_date='now')  # Sale date within the last 30 days
        db_sale = Sales(product_id=product_id, quantity=quantity, sale_date=sale_date)
        db.add(db_sale)
    db.commit()

def create_demo_data(num_products: int):
    db = SessionLocal()
    try:
        create_demo_products(db, num_products)

        # Retrieve the products for inventory and sales creation
        products_list = db.query(Products).all()

        # Populate inventory
        create_demo_inventory(db, products_list)

        # Simulate sales
        create_demo_sales(db, products_list)
    finally:
        db.close()

if __name__ == "__main__":
    # Specify the number of fake products to generate
    num_fake_products = 20
    create_demo_data(num_fake_products)
