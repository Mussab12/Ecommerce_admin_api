# Ecommerce_admin_api
First You need to run the app using unicorn main:app --reload it will create database models.
Then to populate with demo data run the demodata.py script it will populate database with data.
I have created endpoints like /get_inventory/{product_id} for inventory it will get the status of inventory whether its low stock or not.
Endpoint for adding products in inventory: It is for adding products in the inventory
Endpoint for getting status of inventory.
and remaining crud endpoints
Crud endpoints related to product 
Endpoint For getting the revenue of the product according to periods like weekly, monthly, or annually
Endpoint for filtering sales according to product, and date.
DATABASE:
There are 3 models used Products, Sales and Inventory. product_id is used in both sales and inventory table as Foreign key.
It is used in Sales to get the product sales. And in Inventory to show how many products are in Inventory.
