#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 20:13:24 2019

@author: keyvanamini
"""

# if not already available, pip install dataset

import pandas as pd
import numpy as np
import dataset
import datetime

#Load data
employees = pd.read_csv('warehousing-operational-databases/homework/extracts/employees.csv')
orders = pd.read_csv('warehousing-operational-databases/homework/extracts/orders.csv')
products = pd.read_csv('warehousing-operational-databases/homework/extracts/products.csv')

#Create new tables applying normalization
new_employees = employees[['employee_number', 'last_name', 'first_name','reports_to','job_title']].copy()
offices = employees[['office_code', 'city','state', 'country','office_location']].copy()
new_orders = orders[[ 'order_number', 'order_date', 'required_date' ,'shipped_date', 'status', 'comments', 'customer_number']].copy()
customers = orders[['customer_number','customer_name','contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location']].copy()
products_ordered = orders[[ 'order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']].copy()

#Get rid of duplicates and some formatting
offices = offices.drop_duplicates()
new_employees = new_employees.drop_duplicates()
customers = customers.drop_duplicates()
new_employees.reports_to = new_employees.reports_to.fillna('-1').astype(int)
new_orders = new_orders.drop_duplicates()
new_orders[[ 'order_date', 'required_date' ,'shipped_date']] = new_orders[[ 'order_date', 'required_date' ,'shipped_date']].fillna(datetime.date(1111,11,11))

#Connect to postgres server via dataset
db = dataset.connect('postgresql://postgres@localhost:5432/ordersdb')

# Create aliases
off = db['offices']
empl = db['employees']
cust = db['customers']
ord = db['order_details']
prod = db['products']
prod_ord = db['products_ordered']

# Insert data into predefined SQL tables
off.insert_many(offices.to_dict('records'))
empl.insert_many(new_employees.to_dict('records'))
cust.insert_many(customers.to_dict('records'))
ord.insert_many(new_orders.to_dict('records'))
prod.insert_many(products.to_dict('records'))
prod_ord.insert_many(products_ordered.to_dict('records'))