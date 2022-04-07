"""Exceptions and Transactions"""
from datetime import datetime
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine, CheckConstraint
                        , select)

metadata = MetaData()
# MySQL Connection
engine = create_engine("mysql+pymysql://prashant:admin123@@localhost:3306/online_movie_rating")

# Create a new connection
connection = engine.connect()

# Get the existing tables
# cookies table
cookies = Table(
    'cookies',
    metadata,
    autoload=True,
    autoload_with=engine
)
# users table
users = Table(
    'users',
    metadata,
    autoload=True,
    autoload_with=engine
)

# orders table
orders = Table(
    'orders',
    metadata,
    autoload=True,
    autoload_with=engine
)

# items table
line_items = Table(
    'items',
    metadata,
    autoload=True,
    autoload_with=engine
)

# Select the data from each of the above table
# Select from cookies table
print("Cookies Table")
s = select([cookies])
for row in connection.execute(s):
    print(row)

# Select from users table
print("Users Table")
s = select([users])
for row in connection.execute(s):
    print(row)

# Select from orders table
print("Orders Table")
s = select([orders])
for row in connection.execute(s):
    print(row)

# Select from items table
print("Items Table")
s = select([line_items])
for row in connection.execute(s):
    print(row)

# Insert data into users table
from sqlalchemy import select, insert, update
ins = insert(users).values(
    username="cookiemon1",
    email_address="mon@cookie.com",
    phone="111-111-1111",
    password="password"
)
result = connection.execute(ins)

# Check the data inserted
print("Users Table")
s = select([users])
for row in connection.execute(s):
    print(row)

# Insert data into cookies table
ins = cookies.insert()
inventory_list = [
    {
        'cookie_name':'butter cookie',
        'cookie_recipe_url':'http://some.aweso.me/cookie/recipe.html',
        'cookie_sku':'CC012',
        'quantity':'20',
        'unit_cost':'0.50'
    },
    {
        'cookie_name':'choco nut cookie',
        'cookie_recipe_url':'http://some.aweso.me/cookie/recipe.html',
        'cookie_sku':'CN012',
        'quantity':'50',
        'unit_cost':'0.75'
    }
]

result = connection.execute(ins, inventory_list)

# Check the newly inserted data
print("Cookies Inserted")
s = select([cookies])
for row in connection.execute(s):
    print(row)

# Insert the data for orders and items
ins = insert(orders).values(user_id = 1, order_id=3, shipped = False)
result = connection.execute(ins)
print("Orders Inserted")
s = select([orders])
for row in connection.execute(s):
    print(row)

# Insert the data for items
ins = insert(line_items)
order_items = [
    {
        'order_id':1,
        'cookie_id':1,
        'quantity':9,
        'extended_cost':4.50
    }
]

result=connection.execute(ins, order_items)
print("Order Items Inserted")
s = select([line_items])
for row in connection.execute(s):
    print(row)

# Insert more orders and items
ins = insert(orders).values(user_id=1, order_id=4, shipped = False)
result = connection.execute(ins)

print("Order Items inserted")
s = select([orders])
for row in connection.execute(s):
    print(row)

ins = insert(line_items)
order_items = [
    {
        'order_id':1,
        'cookie_id':1,
        'quantity':1,
        'extended_cost':1.50
    },
    {
        'order_id':1,
        'cookie_id':1,
        'quantity':4,
        'extended_cost':4.50
    }
]
result=connection.execute(ins, order_items)
print("Order Items inserted")
s = select([line_items])
for row in connection.execute(s):
    print(row)


# Transaction Level Programming
from sqlalchemy.exc import IntegrityError
def ship_it(order_id):
    s = select([line_items.c.cookie_id, line_items.c.quantity])
    s = s.where(line_items.c.order_id == order_id)
    # Starting the transaction
    transaction = connection.begin()
    cookies_to_ship = connection.execute(s).fetchall()
    try:
        for cookie in cookies_to_ship:
            u = update(cookies).where(cookies.c.cookie_id == cookie.cookie_id)
            u = u.values(quantity = cookies.c.quantity-cookie.quantity)
            result = connection.execute(u)
        u = update(orders).where(orders.c.order_id == order_id)
        u = u.values(shipped=True)
        result = connection.execute(s)
        print("Shipped order ID: {}".format(order_id))
        transaction.commit()
    except IntegrityError as error:
        transaction.rollback()
        print(error)

ship_it(2)

