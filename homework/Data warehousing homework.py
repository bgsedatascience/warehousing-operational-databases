# Import packages
import pandas as pd
import os
import numpy as np

#Navigate to relevant folder and have a looksie
os.chdir("/Users/chloemaine/Documents/Chloe/BGSE/Computing/warehousing-operational-databases/homework/extracts")
os.listdir("/Users/chloemaine/Documents/Chloe/BGSE/Computing/warehousing-operational-databases/homework/extracts")

#Open CSVs
products = pd.read_csv("products.csv")
orders = pd.read_csv("orders.csv")
employees = pd.read_csv("employees.csv")

#Create sub-tables
orders['order_ID']=np.arange(len(orders))
customers = orders[['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location', 'order_ID']].copy()
customers.drop('order_ID', axis=1, inplace=True)
customers_clean = customers.drop_duplicates()
orders_clean = orders[['order_number', 'customer_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number', 'order_date', 'required_date', 'shipped_date', 'status', 'comments', 'order_ID']]
orders_delivery_clean = orders_clean[['order_number','order_date', 'required_date', 'shipped_date','price_each', 'status', 'comments']].drop_duplicates()
orders_delivery_clean_denulled= orders_delivery_clean.astype(object).where(pd.notnull(orders_delivery_clean), None)
orders_delivery_clean_denulled['order_delivery_id']= np.arange(len(orders_delivery_clean_denulled))
orders_composition_clean = orders_clean[['order_number', 'customer_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']]
orders_composition_clean_denulled=orders_composition_clean.astype(object).where(pd.notnull(orders_composition_clean), None)
offices_clean = employees[['office_code', 'city', 'state', 'office_location', 'country']].drop_duplicates()
employees_clean = employees [['employee_number','office_code', 'employee_number', 'last_name', 'first_name', 'reports_to', 'job_title']]
product_stock_details_clean =products[['product_code', 'product_name', 'quantity_in_stock', 'product_description', 'buy_price', '_m_s_r_p']].drop_duplicates()
product_stock_details_clean_denulled=product_stock_details_clean.astype(object).where(pd.notnull(product_stock_details_clean), None)
products_clean = products[['product_code', 'product_line', 'product_scale', 'product_vendor', 'html_description']].drop_duplicates()
products_clean_denulled=products_clean.astype(object).where(pd.notnull(product_stock_details_clean), None)
products_stock_details_clean_copy= product_stock_details_clean.copy()

#Install psycopg2 package
import dataset

ds = dataset.connect("postgresql://postgres@localhost/my_first_database")

cs = ds['customers_1']
cs.insert_many(customers_clean.to_dict('records'))

e1 = ds['employees_1']
e1.insert_many(employees_clean.to_dict('records'))

of1 = ds['offices_1']
of1.insert_many(offices_clean.to_dict('records'))

oc1 = ds['orders_composition_1']
oc1.insert_many(orders_composition_clean_denulled.to_dict('records'))

or1 = ds['orders_delivery_1']
or1.insert_many(orders_delivery_clean_denulled.to_dict('records'))

psd1 = ds['product_stock_details_1']
psd1.insert_many(product_stock_details_clean_denulled.to_dict('records'))

pr1 = ds['products_1']
pr1.insert_many(products_clean.to_dict('records'))




#WIP code

#Look for overlapping columns

#Look at shape & whether shape changes when you drop duplicates
# employees.shape
# employees.drop_duplicates().shape
# products.shape
# products.drop_duplicates().shape
# orders.shape
# orders.drop_duplicates().shape

#Which field can we use as an unique identifier?
# print(len(employees.employee_number.drop_duplicates()))
# print(len(employees.employee_number))

#Create an ID column for orders
#orders['order_ID']=np.arange(len(orders))

#Create a new table for customer-related columns from the orders table
#customers = orders[['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location', 'order_ID']].copy()

#Check if customer number is unique
#Note this is a crap way of doing this. Much better would be to create the customer table as all columns called something like customer columns plus ID.
# print(len(customers))
# print(len((customers[['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location']]).drop_duplicates()))
# print(len((customers[['customer_number']]).drop_duplicates()))

#So now we can get rid of our end column called ID
#customers.drop('order_ID', axis=1, inplace=True)

#And we can drop the duplicates to create one, condensed table with customer IDs
#customers_clean = customers.drop_duplicates()

#And remove the columns we are not using in orders to create a cleaner table there
#orders_clean = orders[['order_number', 'customer_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number', 'order_date', 'required_date', 'shipped_date', 'status', 'comments', 'ID', 'order_ID']]

#Now check in the clean orders table that the number of unique rows in the order_number field is the same as or less the number of unique rows in the order date>comments fields.
# print(len(orders_clean))
# print(len((orders_clean[['order_number']].drop_duplicates())))
# print(len((orders_clean[['order_date', 'required_date', 'shipped_date', 'status', 'comments']].drop_duplicates())))

#Now remove these fields to create an order delivery details table, collapse this into a smaller table
#orders_delivery_clean = orders_clean[['order_number','order_date', 'required_date', 'shipped_date','price_each', 'status', 'comments']].drop_duplicates()

#Check if it's ok to collapse the orders_delivery table
# print(len(orders_delivery_clean[['order_number']].drop_duplicates()))
# print(len(orders_delivery_clean[['order_ID']].drop_duplicates()))

#Create new orders_composition_clean table to make things clean
#orders_composition_clean = orders_clean[['order_number', 'customer_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']]
# N.B. Don't collapse this table as this is the table that links customers to orders

#can we move the price field in the orders table into the products table? i.e. are there the same number of rows in the price_each table as the product_code table? Check that we wont lose any data when we move the column. i.e. that all products can be found in the price table
# print(len(orders[['product_code']].drop_duplicates()))
# print(len(orders[['price_each']].drop_duplicates()))
#Hence conclude no, there are way more prices than products! This cannot be amalgamated. Hence we should move the prices field into the order table

#Investigating the employees table: can we condense locations? If yes, we should have the same number/lower number of distinct rows across city>office location
# print(len(employees[['city']].drop_duplicates()))
# print(len(employees[['state']].drop_duplicates()))
# print(len(employees[['country']].drop_duplicates()))
# print(len(employees[['office_location']].drop_duplicates()))

#Hence create separate office table
#offices_clean = employees[['office_code', 'city', 'state', 'office_location', 'country']].drop_duplicates()

#And clean employees table
#employees_clean = employees [['office_code', 'employee_number', 'last_name', 'first_name', 'reports_to', 'job_title']]

#Checking out the products table
# print(len(products[['product_line']].drop_duplicates()))
# print(len(products[['product_code']].drop_duplicates()))
# print(len(products[['product_name']].drop_duplicates()))
# print(len(products[['product_scale']].drop_duplicates()))
# print(len(products[['product_vendor']].drop_duplicates()))
# print(len(products[['product_description']].drop_duplicates()))
# print(len(products[['quantity_in_stock']].drop_duplicates()))
# print(len(products[['buy_price']].drop_duplicates()))
# print(len(products[['_m_s_r_p']].drop_duplicates()))
# print(len(products[['html_description']].drop_duplicates()))
#Looks like product_code, product_name, product quantity, buy price and m_s_r_p depend on each other (all values of 108/110)
#What about their length as a combined group?
# print(len(products[['product_code', 'product_name', 'quantity_in_stock', 'buy_price', '_m_s_r_p']].drop_duplicates()))
#Length 110, bingo!

#So we can create a separate table of product stock details
#product_stock_details_clean =products[['product_code', 'product_name', 'quantity_in_stock', 'product_description', 'buy_price', '_m_s_r_p']].drop_duplicates()

#And everything else in the product table... But wait, not sure this helps us as we still need a list of how the 110 products relate?
#products_clean = products[['product_code', 'product_line', 'product_scale', 'product_vendor', 'html_description']].drop_duplicates()

#Try to separate out the product description field...
#products_stock_details_clean_copy= product_stock_details_clean.copy()


