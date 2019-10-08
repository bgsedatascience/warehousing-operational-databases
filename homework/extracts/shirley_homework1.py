import pandas as pd
import numpy as np
import psycopg2


from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres: @localhost:5432/shirley_homework')

#read csv into python
raw_employees = pd.read_csv('/Users/shirleyxueyinghe/programming/barcelona_gse/databases/warehousing-operational-databases/homework/extracts/employees.csv')
raw_orders = pd.read_csv('/Users/shirleyxueyinghe/programming/barcelona_gse/databases/warehousing-operational-databases/homework/extracts/orders.csv')
raw_products = pd.read_csv('/Users/shirleyxueyinghe/programming/barcelona_gse/databases/warehousing-operational-databases/homework/extracts/products.csv')

#create tables
offices_table = raw_employees[['office_code', 'city', 'state', 'country', 'office_location']].drop_duplicates().reset_index(drop=True)
employees_table = raw_employees[['employee_number', 'last_name', 'first_name', 'reports_to', 'job_title']].drop_duplicates().reset_index(drop=True)
orders_table = raw_orders[['order_number', 'order_date', 'order_line_number', 'required_date', 'shipped_date', 'status', 'comments', 'sales_rep_employee_number','credit_limit']].drop_duplicates().reset_index(drop=True)
customers_table = raw_orders[['customer_number', 'customer_name', 'contact_last_name','contact_first_name']].drop_duplicates().reset_index(drop=True)
products_table = raw_products[['product_code', 'product_name', 'product_line', 'product_scale', 'product_vendor', 'product_description','quantity_in_stock', 'buy_price', '_m_s_r_p', 'html_description']].drop_duplicates().reset_index(drop=True)
location_table = raw_orders[['city', 'state', 'country', 'customer_location']].drop_duplicates().reset_index(drop=True)

#connect to the database
conn = psycopg2.connect("host=localhost dbname=shirley_homework user=postgres")
cur = conn.cursor()

#Push the data into the database

offices_table.to_sql(name ='offices_table', con=engine, index=False, if_exists='replace', index_label='office_code')
employees_table.to_sql(name='employees_table', con=engine, index=False, if_exists='replace', index_label='employee_number')
orders_table.to_sql(name='orders_table', con=engine, index=False, if_exists='replace', index_label='order_number')
customers_table.to_sql(name='customers_table', con=engine, index=False, if_exists='replace', index_label='customer_number')
products_table.to_sql(name='products_table', con=engine, index=False, if_exists='replace', index_label='product_code')
location_table.to_sql(name='location_table', con=engine, index=False, if_exists='replace', index_label='city')

#code to check my tables using read_sql
query="SELECT office_code FROM offices_table;"
print(pd.read_sql(query, engine))
print(pd.read_sql('products_table', engine))