from db import dal
from sqlalchemy.sql import select

def get_orders_by_customer(cust_name, shipped=None, details = False):
    # Select the columns
    columns = [dal.orders.c.order_id, dal.users.c.username, dal.users.c.phone]
    # Join Condition for table
    joins = dal.users.join(dal.orders)
    if details:
        # add the columns for getting the joins to the table
        # line_items, cookies
        columns.extend([dal.cookies.c.cookie_name,
                        dal.line_items.c.quantity,
                        dal.line_items.c.extended_cost])
        # Join the columns line_items, cookies
        joins = joins.join(dal.line_items).join(dal.cookies)
    # Select Statement using the above columns list
    cust_orders = select(columns)
    # add the table of the joins
    cust_orders = cust_orders.select_from(joins).where(
        dal.users.c.username == cust_name
    )
    if shipped is not None:
        cust_orders = cust_orders.where(dal.orders.c.shipped == shipped)
    result = dal.connection.execute(cust_orders).fetchall()
    return result