import numpy as np
import pandas as pd
import os
import psycopg2

os.chdir('/home/bcohen/Documents/BGSE/Classes/1_Warehousing/warehousing-operational-databases')
os.listdir('homework/extracts/')

employees = pd.read_csv('homework/extracts/employees.csv')
orders = pd.read_csv('homework/extracts/orders.csv')
products = pd.read_csv('homework/extracts/products.csv')

[print(c) for c in employees.columns if c in orders.columns] # city, state, country
[print(c) for c in employees.columns if c in products.columns] # none!
[print(c) for c in orders.columns if c in products.columns] # product_code

employees.shape
employees.drop_duplicates().shape

len(employees.employee_number.drop_duplicates())

products.shape
products.drop_duplicates().shape

orders.shape
orders.drop_duplicates().shape

orders['order_item_id'] = np.arange(len(orders))

#Break out customer data
customer_cols = ['customer_number', 'customer_location', 'customer_name', 'contact_last_name', 'contact_first_name',
                 'city', 'state', 'country', 'credit_limit']

customers = orders[customer_cols + ['order_item_id']].copy()
len(customers.customer_number.drop_duplicates()) == len(customers.drop('order_item_id', axis=1).drop_duplicates())

customers.drop('order_item_id',axis=1,inplace=True)
customers.drop_duplicates(inplace=True)

orders.drop(customer_cols,axis=1, inplace=True)
del customer_cols

#Break orders into orders and sub-orders
order_items_cols = ['order_item_id','product_code','quantity_ordered','price_each','order_line_number','required_date',
                    'shipped_date','status','comments']

order_items = orders[['order_number'] + order_items_cols].copy()

orders.drop(order_items_cols,axis=1,inplace=True)
orders.drop_duplicates(inplace=True)
orders = orders.reset_index(drop=True)
del order_items_cols

#to make writing the sql initialization easier
for c in customers.columns:
    print('%s : %s' % (c,type(customers.loc[0,c])))

for c in employees.columns:
    print('%s : %s' % (c,type(employees.loc[0,c])))

[print('%s : %s' % (c, type(orders.loc[0, c]))) for c in orders.columns]

[print('%s : %s' % (c, type(order_items.loc[0, c]))) for c in order_items.columns]

[print('%s : %s' % (c, type(products.loc[0, c]))) for c in products.columns]

employees = employees[['employee_number', 'office_code', 'last_name', 'first_name', 'reports_to', 'job_title', 'city',
                       'state', 'country', 'office_location']]

order_items = order_items[['order_item_id', 'order_number', 'product_code', 'quantity_ordered', 'price_each',
                           'order_line_number', 'required_date', 'shipped_date', 'status', 'comments']]

products = products[['product_code', 'product_line', 'product_name', 'product_scale','product_vendor',
                     'quantity_in_stock', 'buy_price', '_m_s_r_p', 'product_description', 'html_description']]

#didn't end up using
"""
sql = "INSERT INTO customers(customer_number, customer_location, customer_name, contact_last_name, contact_first_name,\
      city, state, country, credit_limit) VALUES (%s);"
row = 0

sql_insert = sql % [x for x in list(customers.iloc[row])]

conn = psycopg2.connect('dbname=salesdata user=postgres host=localhost')
cur = conn.cursor()
cur.execute(sql, )
cur.commit()
cur.close()

conn = psycopg2.connect('dbname=salesdata user=postgres host=localhost')
cur = conn.cursor()
cur.execute('SELECT * FROM customers;')
res = cur.fetchall()
cur.close()
"""

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres@localhost:5432/salesdata')
customers.to_sql('customers', engine, if_exists='append', index=False)
employees.to_sql('employees', engine, if_exists='append', index=False)
orders.to_sql('orders', engine, if_exists='append', index=False)
order_items.to_sql('order_items', engine, if_exists='append', index=False)
products.to_sql('products', engine, if_exists='append', index=False)



