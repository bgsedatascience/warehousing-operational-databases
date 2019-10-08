import pandas as pd
import numpy as np
import dataset

# reading the csv files

employees = pd.read_csv('extracts/employees.csv')
orders = pd.read_csv('extracts/orders.csv')
products = pd.read_csv('extracts/products.csv')

# changing Nan types

employees = employees.where((pd.notnull(employees)), None)
orders = orders.where((pd.notnull(orders)), None)
products = products.where((pd.notnull(products)), None)

# new dataframes

products = products[['product_line', 'product_code', 'product_name', 'product_scale', 'product_vendor',
                     'product_description', 'quantity_in_stock', 'buy_price', '_m_s_r_p', 'html_description']].copy()
products = products.drop_duplicates()

offices = employees[['office_code', 'city', 'state', 'country', 'office_location']].copy()
offices = offices.drop_duplicates()

employees_info = employees[['employee_number', 'last_name', 'first_name', 'reports_to', 'job_title', 'office_code']].copy()
employees_info = employees_info.drop_duplicates()

customers = orders[['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'city', 'state',
                    'country', 'customer_location']].copy()
customers = customers.drop_duplicates()

product_orders = orders[['customer_number', 'order_number', 'order_date', 'required_date', 'shipped_date', 'status']].copy()
product_orders = product_orders.drop_duplicates()

item_orders = orders[['order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']].copy()
item_orders = item_orders.drop_duplicates()

# connecting the datasets to the database

db = dataset.connect('postgresql://postgres@localhost:5432/dw_database_assignment')

# renaming each table in the database

offi = db['offices']
empl_info = db['employees_info']
cust = db['customers']
prod = db['products']
prod_orde = db['product_orders']
item_orde = db['item_orders']

# inserting datasets

offi.insert_many(offices.to_dict('records'))
empl_info.insert_many(employees_info.to_dict('records'))
cust.insert_many(customers.to_dict('records'))
prod.insert_many(products.to_dict('records'))
prod_orde.insert_many(product_orders.to_dict('records'))
item_orde.insert_many(item_orders.to_dict('records'))

