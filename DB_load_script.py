import psycopg2

# Connect to DB

conn = psycopg2.connect("dbname=alex user=postgres host=localhost")
cur = conn.cursor()
print (conn.encoding)

# Create table EMPLOYEES

cur.execute("""CREATE TABLE employees(
office_code integer,
employee_number integer PRIMARY KEY,
last_name text,
first_name text,
reports_to VARCHAR,
job_title text,
city text,
state text,
country text)""")
conn.commit()

# Load to the DB

with open('/home/alex/Desktop/employees.csv', 'r') as f:
# Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'employees', sep=',')
    conn.commit()


# Create table ORDERS

cur.execute("""CREATE TABLE orders(
order_id INTEGER PRIMARY KEY,
customer_number VARCHAR,
order_number VARCHAR,
product_code VARCHAR,
quantity_ordered VARCHAR,
price_each VARCHAR,
order_line_number VARCHAR,
order_date date,
required_date date,
shipped_date date,
status text,
comments VARCHAR,
customer_name text,
contact_last_name text,
contact_first_name text,
city text,
state text,
country text,
sales_rep_employee_number VARCHAR,
credit_limit VARCHAR)
""")
conn.commit()

# Load to the DB

import dataset
import pandas as pd

orders = pd.read_csv('/home/alex/Desktop/orders.csv')
orders['orders_id'] = orders.index
orders = orders.fillna('1')
db = dataset.connect('postgresql://postgres@localhost:5432/alex')
db['orders'].insert_many(orders.to_dict('records'))

"""
with open('/home/alex/Desktop/orders.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'orders', sep=',')
    conn.commit()
"""

# Create table PRODUCTS

cur.execute("""CREATE TABLE products(
product_line text,
product_code VARCHAR PRIMARY KEY,
product_name text,
product_scale text,
product_vendor text,
quantity_in_stock VARCHAR,
buy_price VARCHAR,
_m_s_r_p VARCHAR,
html_description text)""")
conn.commit()

# Load to the DB

with open('/home/alex/Desktop/products.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'products', sep=',')
    conn.commit()

# Close connection to the DB
cur.close()
conn.close()
