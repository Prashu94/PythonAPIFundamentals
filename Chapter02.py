from datetime import datetime
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine, insert, select)

metadata = MetaData()
# Mysql connection
engine = create_engine("mysql+pymysql://prashant:admin123@@localhost:3306/online_movie_rating")

# Create a new connection
connection = engine.connect()

# Autoload the table without creating everytime
cookies = Table(
    'cookies',
    metadata,
    autoload=True,
    autoload_with=engine
)

# Insert the data into the cookie table
ins = cookies.insert().values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)

print("-------- STRING FORMAT of INSERT STATEMENT ---------")
print(str(ins))

print("-------- PARAMETERS AFTER THE Insert Statement is compiled ----------")
print(ins.compile().params)

# This will actually insert the data
result = connection.execute(ins)

print("-------- The Primary Key after the data is inserted ---------")
print(result.inserted_primary_key)

# Insert function of SQLAlchemy
ins = insert(cookies).values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)

print("-------- STRING FORMAT of INSERT STATEMENT of type where values are directly provided as **kwargs ---------")
print(str(ins))

ins = cookies.insert()
result = connection.execute(ins, cookie_name="chocolate chip",
                            cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
                            cookie_sku="CC01",
                            quantity="12",
                            unit_cost="0.50")
print("-------- The Primary Key after the data is inserted after insert of type disassociated insert ---------")
print(result.inserted_primary_key)

# List of multiple data to be inserted
inventory_list = [
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    }
]

print("----------------- Inserting the list of objects ---------------------")
result = connection.execute(ins, inventory_list)

# Querying the Database
# select all the columns of the cookies table
s = select([cookies])
print("------------------ Select Statement Print -------------------------")
print(str(s))

# ResultProxy will store the data returned by the query run in the database
rp = connection.execute(s)
# Fetch all the results into the results variable
results = rp.fetchall()
# Get the first row from the results variable
first_row = results[0]
print("---------------- The First Row of the Result Set ------------------------")
print(first_row)

# Select the first index from the first_row
print("--------------- The First Column of the First Result Using Index ---------------------")
print(first_row[1])
print("--------------- The First Column of the First Result Using Column Name ---------------------")
print(first_row.cookie_name)
print("--------------- The First Column of the First Result Using Table object with column object and variable name "
      "---------------------")
print(first_row[cookies.c.cookie_name])

print("------------------------ Print Using the Iteration Over the ResultProxy ---------------------------------")
# Iterating over the ResultProxy
rp = connection.execute(s)
for record in rp:
    print(record.cookie_name)

# Selecting specific columns of the table
s = select([cookies.c.cookie_name, cookies.c.quantity])
rp = connection.execute(s)
print("------------------- Print the columns returned by the ResultProxy --------------------------------------")
print(rp.keys())
results = rp.fetchall()

# Select from pre-loaded table
s = select([cookies.c.cookie_name, cookies.c.quantity])
rp = connection.execute(s)
print("------------------- Print the columns returned by the ResultProxy --------------------------------------")
print(rp.keys())  # List of Columns returned
results = rp.fetchall()
print("------------------ Print the Result set fetched through fetchall() method -------------------------------")
print(results)

# Order By Clause
print("--------------------------- Order By Clause Example ----------------------------")
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity, cookies.c.cookie_name)
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))

# Descending
print("----------------------- Order By Descending Example --------------------------")
from sqlalchemy import desc

s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(desc(cookies.c.quantity))
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))

# Limit the query result
print("----------------------- Select the data With a Limit --------------------------")
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity)
s = s.limit(2)
rp = connection.execute(s)
print([result.cookie_name for result in rp])

# Aggregation function of the database
print("--------------------- Aggregation Function using the func object which calls the native sql method for "
      "aggregation ------------------")
from sqlalchemy import func

s = select([func.count(cookies.c.cookie_name)])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.count_1)

from sqlalchemy import func

s = select([func.count(cookies.c.cookie_name).label('inventory_count')])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.inventory_count)

# Filtering
print("------------------ Filtering The Data ----------------------")

print("--- Select the cookie with name - chocolate chip ---")
s = select([cookies]).where(cookies.c.cookie_name == 'chocolate chip')
rp = connection.execute(s)
record = rp.first()
print(record.items())

print("--- Select the cookie like %chocolate% and quantity = 12 ---")
s = select([cookies]).where(cookies.c.cookie_name.like('%chocolate%')).where(cookies.c.quantity == 12)
rp = connection.execute(s)
for record in rp.fetchall():
    print(record.cookie_name)

print("--- String Representation of SELECT Statement ---")
print(str(s))

print("--- Concatenating the string to columns ---")
s = select([cookies.c.cookie_name, 'SKU-' + cookies.c.cookie_sku])
for row in connection.execute(s):
    print(row)

print("--- Adding a calculated column to the select ---")
s = select([cookies.c.cookie_name, cookies.c.quantity * cookies.c.unit_cost])
for row in connection.execute(s):
    print('{} - {}'.format(row.cookie_name, row.anon_1))

print("--- Casting the Columns in select ---")
from sqlalchemy import cast

s = select([cookies.c.cookie_name, (cookies.c.quantity * cookies.c.unit_cost).label('inv_cost')])
for row in connection.execute(s):
    print('{:<25}{:.2f}'.format(row.cookie_name, row.inv_cost))

print("--- Conjunction ---")
from sqlalchemy import and_, or_, not_

print("--- AND ---")
s = select([cookies]).where(and_(
    cookies.c.quantity > 23,
    cookies.c.unit_cost < 0.40
))

for row in connection.execute(s):
    print(row.cookie_name)

print("--- OR ---")
s = select([cookies]).where(or_(
    cookies.c.quantity.between(10, 50),
    cookies.c.cookie_name.contains('chip')
))

for row in connection.execute(s):
    print(row.cookie_name)

print("---- Updating the Table ----")
from sqlalchemy import update

# update statement creation
u = update(cookies).where(cookies.c.cookie_name == "chocolate chip")
# values to be updated
u = u.values(quantity=(cookies.c.quantity + 120))
result = connection.execute(u)
print(result.rowcount)

# check the records updated
print("-- Check the updated Records --")
s = select([cookies]).where(cookies.c.cookie_name == "chocolate chip")
result = connection.execute(s).first()
for key in result.keys():
    print('{:>20}: {}'.format(key, result[key]))

# Deleting the data from the table
print("---- Deleting a data from the cookie table ----")
from sqlalchemy import delete

u = delete(cookies).where(cookies.c.cookie_id == 2)
result = connection.execute(u)
print(result.rowcount)

print("--- Check the data after deleting ---")
s = select([cookies]).where(cookies.c.cookie_id == 2)
result = connection.execute(s).fetchall()
print(len(result))

# Load Some Data for orders and line_items table.
# Pre-Load the Table customer_list to the users table
# Autoload the table without creating everytime
users = Table(
    'users',
    metadata,
    autoload=True,
    autoload_with=engine
)

orders = Table(
    'orders',
    metadata,
    autoload=True,
    autoload_with=engine
)

line_items = Table(
    'items',
    metadata,
    autoload=True,
    autoload_with=engine
)

# Customer List
customer_list = [
    {
        'username': "cookiemon",
        'email_address': "mon@cookie.com",
        'phone': "111-111-1111",
        "password": "password"
    },
    {
        'username': 'cakeeater',
        'email_address': "cakeeater@cake.com",
        'phone': "222-222-2222",
        'password': "password"
    },
    {
        'username': "pieguy",
        'email_address': "guy@pie.com",
        'phone': "333-333-3333",
        'password': "password"
    }
]

# Insert the data in the user table
ins = users.insert()
result = connection.execute(ins, customer_list)

# Insert the data in the order table
ins = insert(orders).values(user_id=1, order_id=1)
result = connection.execute(ins)

ins = insert(orders).values(user_id=2, order_id=2)
result = connection.execute(ins)

# Insert the order items
ins = insert(line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity': 2,
        'extended_cost': 1.00
    },
    {
        'order_id': 1,
        'cookie_id': 3,
        'quantity': 2,
        'extended_cost': 3.00
    }
]

result = connection.execute(ins, order_items)

# Joins
# Create a list of column names for the cookie tables
columns = [orders.c.order_id, users.c.username, users.c.phone,
           cookies.c.cookie_name, line_items.c.quantity,
           line_items.c.extended_cost]
# select the column names
cookiemon_orders = select(columns)
# Join statement
cookiemon_orders = cookiemon_orders.select_from(
    orders.join(users).join(line_items).join(cookies)
).where(users.c.username == 'cookiemon')
# Get the result
results = connection.execute(cookiemon_orders).fetchall()
for row in results:
    print(row)

# Example: Outer Join
columns = [users.c.username, func.count(orders.c.order_id)]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders))
all_orders = all_orders.group_by(users.c.username)
print(str(all_orders))
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)


# Chaining
def get_orders_by_customer(cust_name):
    columns = [orders.c.order_id, users.c.username,
               users.c.phone, cookies.c.cookie_name,
               line_items.c.quantity, line_items.c.extended_cost]
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(
        users.join(orders).join(line_items)
            .join(cookies)
    )
    cust_orders = cust_orders.where(users.c.username == cust_name)
    print(str(cust_orders))
    result = connection.execute(cust_orders).fetchall()
    return result


print(get_orders_by_customer('cookiemon'))


# Conditional Chaining
def get_orders_by_customer(cust_name, shipped=None, details=False):
    columns = [orders.c.order_id, users.c.username, users.c.phone]
    joins = users.join(orders)
    if details:
        columns.extend([cookies.c.cookie_name,line_items.c.quantity, line_items.c.extended_cost])
        joins=joins.join(line_items).join(cookies)
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(joins).where(users.c.username == cust_name)
    if shipped is not None:
        cust_orders = cust_orders.where(orders.c.shipped == shipped)
    result = connection.execute(cust_orders).fetchall()
    return result

# Get all the orders with customer name 'cakeeater'
print(get_orders_by_customer('cakeeater'))
# Get all the orders with details
print(get_orders_by_customer('cakeeater', details = True))
# Gets only orders that have shipped
get_orders_by_customer('cakeeater', shipped=True)
# Gets only orders that have not shipped
get_orders_by_customer('cakeeater', shipped=False)
# Gets orders that haven't shipped yet with the details
get_orders_by_customer('cakeeater', shipped=False, details=True)