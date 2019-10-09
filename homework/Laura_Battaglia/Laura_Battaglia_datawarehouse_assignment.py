import pandas as pd
import numpy as np
import dataset
import datetime

#read csv files as pandas dataframes

employees = pd.read_csv('warehousing-operational-databases/homework/extracts/employees.csv')
orders = pd.read_csv('warehousing-operational-databases/homework/extracts/orders.csv')
products = pd.read_csv('warehousing-operational-databases/homework/extracts/products.csv')

#define relational tables (and drop duplicates)
offices = employees[['office_code', 'city','state', 'country','office_location']].copy()
offices = offices.drop_duplicates()

new_employees = employees[['employee_number', 'last_name', 'first_name','reports_to','job_title','office_code']].copy()
new_employees = new_employees.drop_duplicates()

#replace nas with -1 so to be able to change type to int
new_employees.reports_to = new_employees.reports_to.fillna('-1').astype(int)


customers = orders[['customer_number','customer_name','contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location']].copy()
customers = customers.drop_duplicates()

new_orders = orders[[ 'order_number', 'order_date', 'required_date' ,'shipped_date', 'status', 'comments', 'customer_number']].copy()
new_orders = new_orders.drop_duplicates()

#replace nas with 1111-11-11 so to be able to change type to date
new_orders[[ 'order_date', 'required_date' ,'shipped_date']] = new_orders[[ 'order_date', 'required_date' ,'shipped_date']].fillna(datetime.date(1111,11,11))
products_ordered = orders[[ 'order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']].copy()

#connect to sql database via python dataset package
db = dataset.connect('postgresql://postgres@localhost:5432/dw_assignment_1')

#alias the tables within the sql database
off = db['offices']
empl = db['employees']
cust = db['customers']
orde = db['orders']
prod = db['products']
prod_ord = db['products_ordered']

#insert panda dataframes into the sql tables (first converting dataframes into lists of dictionaries)
off.insert_many(offices.to_dict('records'))
empl.insert_many(new_employees.to_dict('records'))
cust.insert_many(customers.to_dict('records'))
orde.insert_many(new_orders.to_dict('records'))
prod.insert_many(products.to_dict('records'))
prod_ord.insert_many(products_ordered.to_dict('records'))

#replace NaN with SQL NULL type
db.query('''UPDATE orders SET shipped_date = NULL WHERE shipped_date = '1111-11-11';''')
db.query('''UPDATE employees SET reports_to = NULL WHERE reports_to = '-1';''')
db.query('''UPDATE orders SET comments = NULL WHERE comments = 'NaN';''')
db.query('''UPDATE products SET html_description = NULL WHERE html_description = 'NaN';''')
db.query('''UPDATE offices SET state = NULL WHERE state = 'NaN';''')
db.query('''UPDATE customers SET state = NULL WHERE state = 'NaN';''')


