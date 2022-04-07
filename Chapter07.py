from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:')

# sessionmaker - provides arguments which are same through an application
Session = sessionmaker(bind=engine)
session = Session()

from datetime import datetime

from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer(), primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    def __repr__(self):
        return f"Cookie(cookie_name='{self.cookie_name}'," \
               f"cookie_recipe_url='{self.cookie_recipe_url}'" \
               f"cookie_sku='{self.cookie_sku}'" \
               f"quantity={self.quantity}" \
               f"unit_cost={self.unit_cost})".format(self=self)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(), nullable=False, unique=True)
    email_address = Column(String(20), nullable=False)
    phone = Column(String(25), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return f"User(username='{self.username}'," \
               f"email_address='{self.email_address}'," \
               f"phone = '{self.phone}'" \
               f"password = '{self.password}')".format(self=self)


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)

    user = relationship("User", backref=backref('orders', order_by=order_id))

    def __repr__(self):
        return f"Order(user_id = {self.user_id}," \
               f"shipped={self.shipped})".format(self=self)


class LineItem(Base):
    __tablename__ = 'line_items'
    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))

    order = relationship("Order", backref=backref('line_items', order_by=line_item_id))
    cookie = relationship("Cookie", uselist=False)

    def __repr__(self):
        return f"LineItems(order_id={self.order_id}," \
               f"cookie_id={self.cookie_id}," \
               f"quantity={self.quantity}," \
               f"extended_cost={self.extended_cost})".format(self=self)


# create the database tables
Base.metadata.create_all(engine)

# Create an instance of the Cookie class
cc_cookie = Cookie(cookie_name='chocolate chip',
                   cookie_recipe_url='http://some.aweso.me/cookie/recipe.html',
                   cookie_sku='CC01',
                   quantity=12,
                   unit_cost=0.50)
# Add the instance to the session
session.add(cc_cookie)

# Commit the data to the database
session.commit()

print(cc_cookie.cookie_id)

# Another Two Cookie Instance
dcc = Cookie(cookie_name='dark chocolate chip',
             cookie_recipe_url='http://some.aweso.me/cookie/recpie_dark.html',
             cookie_sku='CC02',
             quantity=1,
             unit_cost=0.75)
mol = Cookie(cookie_name='molasses',
             cookie_recipe_url='http://some.aweso.me/cookie/recipe_molasses.html',
             quantity=1,
             unit_cost=0.80)
# Add sessions
session.add(dcc)
session.add(mol)
session.flush()

print(dcc.cookie_id)
print(mol.cookie_id)

c1 = Cookie(cookie_name='peanut_butter',
            cookie_recipe_url='http://some.aweso.me/cookie/peanut.html',
            cookie_sku='PB01',
            quantity=24,
            unit_cost=0.25)

c2 = Cookie(cookie_name='oatmeal_raisin',
            cookie_recipe_url='http://some.aweso.me/cookie/raisin.html',
            cookie_sku='EWW01',
            quantity=100,
            unit_cost=1.00)

# Bulk object save
session.bulk_save_objects([c1, c2])
session.commit()

print(c1.cookie_id)

# Query the table for Cookie
cookies = session.query(Cookie).all()
print(cookies)

# Getting only first value
print(session.query(Cookie.cookie_name, Cookie.quantity).first())

# Iteration way to select the data
for cookie in session.query(Cookie).order_by(Cookie.quantity):
    print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name))

# Iterating by ordering the quantity in descending order
from sqlalchemy import desc

for cookie in session.query(Cookie).order_by(desc(Cookie.quantity)):
    print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name))

# Iterating over the Cookie table and just select the second column
query = session.query(Cookie).order_by(Cookie.quantity)[:2]
print([result.cookie_name for result in query])

# Iterating over the Cookie table an limit the data for 2 rows
query = session.query(Cookie).order_by(Cookie.quantity).limit(2)
print([result.cookie_name for result in query])

# Aggregating the data
from sqlalchemy import func

inv_count = session.query(func.sum(Cookie.quantity)).scalar()
print(inv_count)

rec_count = session.query(func.count(Cookie.cookie_name)).first()
print(rec_count)

rec_count = session.query(func.count(Cookie.cookie_name).label('inventory_count')).first()
print(rec_count.keys())
print(rec_count.inventory_count)

# Get the Data for Chocolate Chip - Filter
record = session.query(Cookie).filter(Cookie.cookie_name == 'chocolate chip').first()
print(record)

# - Filter By Method
record = session.query(Cookie).filter_by(cookie_name='chocolate chip').first()
print(record)

query = session.query(Cookie).filter(Cookie.cookie_name.like('%chocolate%'))
for record in query:
    print(record.cookie_name)

# Concatenating the string to the column
query = session.query(Cookie.cookie_name, 'SKU-' + Cookie.cookie_sku).all()
for row in query:
    print(row)

# casting the Flat data
from sqlalchemy import cast

query = session.query(Cookie.cookie_name,
                      cast((Cookie.quantity * Cookie.unit_cost),
                           Numeric(12, 2)).label('inv_cost'))
for result in query:
    print('{} - {}'.format(result.cookie_name, result.inv_cost))

# And Or Condition
from sqlalchemy import and_, or_, not_
# AND condition
query = session.query(Cookie).filter(
    Cookie.quantity > 23,
    Cookie.unit_cost < 0.40
)
for result in query:
    print(result.cookie_name)
# OR Condition
query = session.query(Cookie).filter(
    or_(
        Cookie.quantity.between(10, 50),
        Cookie.cookie_name.contains('chip')
    )
)

for result in query:
    print(result.cookie_name)

# Update a specific column value using session
query = session.query(Cookie)
cc_cookie = query.filter(Cookie.cookie_name == 'chocolate chip').first()
cc_cookie.quantity = cc_cookie.quantity + 120
session.commit()
print(cc_cookie.quantity)

# In-Place update using session
query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "chocolate chip")
query.update({Cookie.quantity: Cookie.quantity - 20})

cc_cookie = query.first()
print(cc_cookie.quantity)

# Deleting the data from the table
query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "dark chocolate chip")
dcc_cookie = query.one()
session.delete(dcc_cookie)
session.commit()
dcc_cookie = query.first()
print(dcc_cookie)