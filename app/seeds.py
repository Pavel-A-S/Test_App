#!/usr/bin/env python3

import os
import pymysql
import random
import time
from datetime import datetime, timedelta

def require(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value

MYSQL_HOST = require("MYSQL_HOST")
MYSQL_USER = require("MYSQL_USER")
MYSQL_PASSWORD = require("MYSQL_PASSWORD")
MYSQL_DB = require("MYSQL_DB")

# Waiting for database
for i in range(20):
    try:
        db = pymysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PASSWORD,
            database = MYSQL_DB,
            charset = "utf8mb4",
            port = 3306,
            autocommit = False
        )
        print("DB connected")
        break
    except Exception as e:
        print("Waiting for DB...")
        time.sleep(2)
else:
    raise RuntimeError("DB not ready")

cursor = db.cursor()

# Empty tables
print("Clearing database tables...")

tables = ["order_items", "orders", "customers", "products", "categories"]
for t in tables:
    cursor.execute(f"SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute(f"TRUNCATE TABLE {t};")
    cursor.execute(f"SET FOREIGN_KEY_CHECKS=1;")

print("Tables cleared successfully")

# Data settings
NUM_CUSTOMERS = 500
NUM_ORDERS = 1000
MIN_ORDER_ITEMS = 1
MAX_ORDER_ITEMS = 30
NUM_PRODUCTS = 200
NUM_CATEGORIES = 50
EACH_TOP_CATEGORY = 3

print("Inserting test data...")

# Inserting data into categories table
category_ids = []
for i in range(1, NUM_CATEGORIES + 1):
    name = f"Category_{i}"
    parent_id = None if (i == 1 or i % EACH_TOP_CATEGORY == 0) else random.randint(1, i - 1)

    cursor.execute(
        "INSERT INTO categories (id, name, parent_id) VALUES (%s, %s, %s)",
        (i, name, parent_id)
    )

    category_ids.append(i)

# Inserting data into products table
product_ids = []
for i in range(1, NUM_PRODUCTS + 1):
    name = f"Product_{i}"
    price = round(random.uniform(10, 5000), 2)
    quantity = random.randint(10, 200)
    category_id = random.choice(category_ids)
    cursor.execute("INSERT INTO products (id, name, quantity, price, category_id) VALUES (%s, %s, %s, %s, %s)",
                   (i, name, quantity, price, category_id))
    product_ids.append(i)

# Inserting data into customers table
customer_ids = []
for i in range(1, NUM_CUSTOMERS + 1):
    name = f"Customer_{i}"
    address = f"{random.randint(100, 9999)} Main Street"
    cursor.execute("INSERT INTO customers (id, name, address) VALUES (%s, %s, %s)", (i, name, address))
    customer_ids.append(i)

# Inserting data into orders table
order_ids = []
for i in range(1, NUM_ORDERS + 1):
    customer_id = random.choice(customer_ids)
    now = datetime.now()
    order_date = now - timedelta(
        days=random.randint(0, 60),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    cursor.execute("INSERT INTO orders (id, customer_id, order_date) VALUES (%s, %s, %s)", 
                   (i, customer_id, order_date))
    order_ids.append(i)

# Inserting data into order_items table
order_item_id = 1
for order_id in order_ids:
    num_items = random.randint(MIN_ORDER_ITEMS, MAX_ORDER_ITEMS)
    chosen_products = random.sample(product_ids, k=min(num_items, len(product_ids)))
    for product_id in chosen_products:
        quantity = random.randint(1, 5)
        cursor.execute("SELECT price FROM products WHERE id=%s", (product_id,))
        price = cursor.fetchone()[0]
        cursor.execute("INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s, %s)",
                       (order_item_id, order_id, product_id, quantity, price))
        order_item_id += 1

db.commit()
cursor.close()
db.close()

print("Inserting completed!\n")
print(f"Customers: {NUM_CUSTOMERS}\nOrders: {NUM_ORDERS}\nProducts: {NUM_PRODUCTS}\nCategories: {NUM_CATEGORIES}")
