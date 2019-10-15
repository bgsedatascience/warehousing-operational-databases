#Install packages and connect to Postgres
import dataset
import sqlalchemy
import pandas as pd

ds = dataset.connect("postgresql://postgres@localhost/my_first_database")

#Extract tables from Postgres
engine = sqlalchemy.create_engine("postgresql://postgres@localhost/my_first_database")

customers = pd.read_sql_query('select * from "customers_1"', con=engine)
employees =pd.read_sql_query('select * from "employees_1"', con=engine)
offices =pd.read_sql_query('select * from "offices_1"', con=engine)
orders_composition =pd.read_sql_query('select * from "orders_composition_1"', con=engine)
orders_delivery = pd.read_sql_query('select *, price_each::numeric as price_each_numeric, order_date::DATE as order_date_datetime from "orders_delivery_1"', con=engine).drop(columns="order_delivery_id")
product_stock_details =pd.read_sql_query('select *, buy_price::numeric as buy_price_numeric from "product_stock_details_1"', con=engine)
products =pd.read_sql_query('select * from "products_1"', con=engine)


#Transform the data

#Create a megatable
merge_1= orders_composition.merge(orders_delivery, on= ['order_number', 'price_each'])
merge_2= merge_1.merge(customers, on= 'customer_number')
merge_3=merge_2.merge(products, on= 'product_code')
merge_4=merge_3.merge(product_stock_details, on='product_code')
merge_5=merge_4.merge(employees, left_on= 'sales_rep_employee_number', right_on= 'employee_number')
super_merge=merge_5.merge(offices, on='office_code')

#Create calculated fields
super_merge['sales']= super_merge['price_each_numeric'] * super_merge['quantity_ordered']
super_merge['profit']=(super_merge['price_each_numeric']-super_merge['buy_price_numeric'])* super_merge['quantity_ordered']
super_merge['total_cost']=super_merge['quantity_ordered']*super_merge['buy_price_numeric']
super_merge['d8d']= super_merge['order_date_datetime'].map(lambda x: x.day)
super_merge['d8m']=super_merge['order_date_datetime'].map(lambda x: x.month)
def class_q(x):
    if x < 4:
        return '1'
    elif x<7:
        return '2'
    elif x<10:
        return '3'
    else:
        return '4'
super_merge['d8q']=super_merge['d8m'].map(lambda x : class_q(int(x)))
super_merge['customer_city']=super_merge['city_x']
super_merge['customer_country']=super_merge['country_x']
super_merge['office_city']=super_merge['city_y']

#Create measures table for upload by selecting key columns
measures=super_merge[['quantity_ordered', 'sales', 'profit', 'total_cost', 'd8d', 'd8q', 'order_date', 'customer_city', 'customer_country', 'customer_number', 'product_code', 'office_code', 'office_city', 'employee_number', 'order_number']]
orders_pre=super_merge[['order_number', 'required_date', 'shipped_date', 'price_each', 'status', 'comments']].drop_duplicates()
orders=orders_pre.astype(object).where(pd.notnull(orders_pre), None)
employees=super_merge[['employee_number', 'office_code', 'last_name', 'first_name', 'reports_to', 'job_title', 'city_y', 'state_y', 'country_y', 'office_location']].drop_duplicates()
products=super_merge[['product_code', 'product_line', 'product_scale', 'product_vendor', 'html_description']].drop_duplicates()
customers=super_merge[['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'state_x', 'sales_rep_employee_number', 'credit_limit', 'customer_location']].drop_duplicates()

#Load data into new database
#engine2 required?/close previous connection?

import dataset

ds = dataset.connect("postgresql://postgres@localhost/car_sales")

ms1 = ds['measures']
ms1.insert_many(measures.to_dict('records'))

or1 = ds['orders']
or1.insert_many(orders.to_dict('records'))

e1 = ds['employees']
e1.insert_many(employees.to_dict('records'))

p1 = ds['products']
p1.insert_many(products.to_dict('records'))

c1 = ds['customers']
c1.insert_many(customers.to_dict('records'))
