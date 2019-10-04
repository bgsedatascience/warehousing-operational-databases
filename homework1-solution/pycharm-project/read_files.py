import pandas as pd
import dataset
import psycopg2

orders = pd.read_csv("orders.csv")
employees = pd.read_csv('employees.csv')
products = pd.read_csv('products.csv')

empl = employees[['employee_number', 'last_name', 'first_name', 'reports_to', 'job_title', 'office_code']]
offices = employees[['office_code', 'city', 'state', 'country', 'office_location']]
customers = orders[['customer_number', 'customer_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location']]
order_overview = orders[['order_number', 'order_date', 'required_date', 'shipped_date', 'status', 'comments', 'customer_number']]
order_details = orders[['order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']]

db = dataset.connect('postgresql://postgres@localhost:5432/foo')

#empl_db = db['empl'] # alias table from database
#empl_db.insert_many(empl.to_dict('records')) # insert into database

print(db.tables)