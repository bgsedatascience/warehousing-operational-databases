import pandas as pd
import dataset
import datetime
import math

#import data into pandas dataframe
employees = pd.read_csv('./extracts/employees.csv')
orders = pd.read_csv('./extracts/orders.csv')
products = pd.read_csv('./extracts/products.csv')

#split the data into the tables I want in the SQL dataset and convert them into lists of dictionaries
offices = employees.loc[:,['office_code','city','state','country','office_location']].drop_duplicates().to_dict('records')
employees = employees.loc[:,['office_code','employee_number','last_name','first_name','reports_to','job_title']].to_dict('records')
customers = orders.loc[:,['customer_number','customer_name','contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'credit_limit', 'customer_location']].drop_duplicates().to_dict('records')
products_ordered = orders.loc[:,[ 'order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']].to_dict('records')
products = products.to_dict('records')
orders = orders.loc[:,[ 'order_number', 'order_date', 'required_date' ,'shipped_date', 'status', 'comments', 'sales_rep_employee_number']].drop_duplicates()
orders.comments = orders.comments.astype(str)
orders = orders.to_dict('records')

#I had issues dealing with missing values directly in Pandas dataframes, 
#What I did is to parse through the dictionaries and remove the keys with NaN values. 

#remove from dictionary every key that has a nan value
for o in orders:
    if type(o['shipped_date']) is not str:
        del o['shipped_date']
    else:
        o['shipped_date'] = datetime.datetime.strptime(o['shipped_date'], '%Y-%m-%d').date()
    o['order_date'] = datetime.datetime.strptime(o['order_date'], '%Y-%m-%d').date()
    o['required_date'] = datetime.datetime.strptime(o['required_date'], '%Y-%m-%d').date()
       
for o in orders:
    if o['comments'] == 'nan':
        del o['comments']
        
for o in employees:
    if math.isnan(o['reports_to']):
        del o['reports_to']
    else:
        o['reports_to'] = int(o['reports_to'])
    
for o in products:
    if math.isnan(o['html_description']):
        del o['html_description']

for o in offices:
    if type(o['state']) is not str:
        del o['state']
        
for o in customers:
    if type(o['state']) is not str:
        del o['state']


#once the data are ready, I use the dataset package to insert them in the sql tables
db = dataset.connect("postgresql://postgres@localhost/ds_assignment1")
emp = db['employees']
of = db['offices']
cust = db['customers']
pr = db['products']
pr_ord = db['products_ordered']
orde = db['orders']

of.insert_many(offices)
emp.insert_many(employees)
cust.insert_many(customers)
pr.insert_many(products)
orde.insert_many(orders)
pr_ord.insert_many(products_ordered)
db.commit()