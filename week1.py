#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 10:50:23 2019

@author: vivek
"""

import pandas as pd
import psycopg2

employees = pd.read_csv("~/Desktop/DataWarehousing/HW1/employees.csv")
orders = pd.read_csv("~/Desktop/DataWarehousing/HW1/orders.csv")
products = pd.read_csv("~/Desktop/DataWarehousing/HW1/products.csv")

conn = psycopg2.connect("dbname=week1 user=postgres host=localhost")
cursor = conn.cursor()

office_info_df = employees.loc[:,['office_code','city', 'state', 'country', 'office_location']].drop_duplicates()
tuples = [tuple(x) for x in office_info_df.values]
for i in tuples:
    cursor.execute("INSERT INTO office_info (office_code, city, state, country, office_location) VALUES(%s, %s, %s, %s, %s)", i)

employee_info_df = employees.loc[:,['employee_number', 'office_code', 'last_name', 'first_name', 'reports_to', 'job_title']].drop_duplicates()
tuples = [tuple(x) for x in employee_info_df.values]
for i in tuples:
    cursor.execute("INSERT INTO employee_info (employee_number, office_code, last_name, first_name, reports_to, job_title) VALUES(%s, %s, %s, %s, %s, %s)", i)
    
customer_info_df = orders.loc[:,['customer_number', 'sales_rep_employee_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'city', 'state', 'country', 'credit_limit', 'customer_location']].drop_duplicates()
tuples = [tuple(x) for x in customer_info_df.values]
for i in tuples:
    cursor.execute("INSERT INTO customer_info (customer_number, sales_rep_employee_number, customer_name, contact_last_name, contact_first_name, city, state, country, credit_limit, customer_location) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", i)

product_info_df = products.loc[:,['product_code', 'product_name', 'product_scale', 'product_vendor',   'product_line', 'product_description', 'quantity_in_stock', 'buy_price', '_m_s_r_p', 'html_description']].drop_duplicates()
tuples = [tuple(x) for x in product_info_df.values]
for i in tuples:
    cursor.execute("INSERT INTO product_info (product_code, product_name, product_scale, product_vendor, product_line, product_description, quantity_in_stock, buy_price, _m_s_r_p, html_description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", i)

order_items_df = orders.loc[:,['order_number', 'order_line_number', 'product_code', 'quantity_ordered', 'price_each']].drop_duplicates()
tuples = [tuple(x) for x in order_items_df.values]
for i in tuples:
    cursor.execute("INSERT INTO order_items (order_number, order_line_number, product_code, quantity_ordered, price_each) VALUES(%s, %s, %s, %s, %s)", i)
    
order_info_df = orders.loc[:,['order_number', 'customer_number', 'order_date', 'required_date', 'status', 'comments']].drop_duplicates()
tuples = [tuple(x) for x in order_info_df.values]
for i in tuples:
    cursor.execute("INSERT INTO order_info (order_number, customer_number, order_date, required_date, status, comments) VALUES(%s, %s, %s, %s, %s, %s)", i)

conn.commit()
cursor.close()
conn.close()