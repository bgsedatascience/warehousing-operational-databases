import pandas as pd
employees = pd.read_csv("/Users/kristin.lomicka/Documents/BGSE_Courses/Data_Warehousing/warehousing-operational-databases/homework/extracts/employees.csv")
orders = pd.read_csv("/Users/kristin.lomicka/Documents/BGSE_Courses/Data_Warehousing/warehousing-operational-databases/homework/extracts/orders.csv")
products = pd.read_csv("/Users/kristin.lomicka/Documents/BGSE_Courses/Data_Warehousing/warehousing-operational-databases/homework/extracts/products.csv")
print(employees)
print(orders)
offices = employees[['office_code','city', 'state', 'country', 'office_location']].drop_duplicates().reset_index(drop=True)
employees_new = employees[['office_code', 'employee_number', 'last_name', 'first_name', 'reports_to', 'job_title']]
customers = orders[['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'credit_limit', 'customer_location']].drop_duplicates().reset_index(drop=True)
order_metadata = orders[['order_number', 'order_date', 'required_date', 'shipped_date', 'status', 'comments', 'sales_rep_employee_number']].drop_duplicates().reset_index(drop=True)
orders_new = orders[['customer_number', 'order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number',]].drop_duplicates().reset_index(drop=True)

#check dytpes for each dataframe
result1 = customers.dtypes
print(result1)

#change NaN to None
customers_a = customers.astype(object).where(pd.notnull(customers), None)
offices_a = offices.astype(object).where(pd.notnull(offices), None)
order_metadata_a = order_metadata.astype(object).where(pd.notnull(order_metadata), None)
orders_new_a = orders_new.astype(object).where(pd.notnull(orders_new), None).reset_index()
products_a = products.astype(object).where(pd.notnull(products), None)

#check orders_new_a for duplicate values
dupes_orders_new_a = orders_new_a.pivot_table(index=['product_code'], aggfunc='size')
print(dupes_orders_new_a)

#assign a unique ID to orders_new_a
orders_new_a.insert(0, 'orders_unique_id', range(100, 100 + len(orders_new_a)))

#import data values to postgres 
import dataset
#import employees_new
ds = dataset.connect("postgresql://postgres@localhost/hw1_data_warehouse")
cs = ds['employees_new'] #python code name#
cs.insert_many(employees_new.to_dict('records')) #sql code name#
# # import customers_a
ds = dataset.connect("postgresql://postgres@localhost/hw1_data_warehouse")
cs = ds['customers_a'] #python code name#
cs.insert_many(customers_a.to_dict('records')) #sql code name#
# #import offices_a
ds = dataset.connect("postgresql://postgres@localhost/hw1_data_warehouse")
cs = ds['offices_a'] #python code name#
cs.insert_many(offices_a.to_dict('records')) #sql code name#
# #import order_metadata_a
ds = dataset.connect("postgresql://postgres@localhost/hw1_data_warehouse")
cs = ds['order_metadata_a'] #python code name#
cs.insert_many(order_metadata_a.to_dict('records')) #sql code name#
# #import products_a
ds = dataset.connect("postgresql://postgres@localhost/hw1_data_warehouse")
cs = ds['products_a'] #python code name#
cs.insert_many(products_a.to_dict('records')) #sql code name#
# #import orders_new_a
ds = dataset.connect("postgresql://postgres@localhost/hw1_data_warehouse")
cs = ds['orders_new_a'] #python code name#
cs.insert_many(orders_new_a.to_dict('records')) #sql code name#

