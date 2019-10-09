#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 23:23:18 2019

@author: pedro freitas NIS: 173976
"""
#Import packages
import pandas as pd
import psycopg2
import os

#Load data into df. 
data_orders = pd.read_csv("orders.csv")
data_prod = pd.read_csv("products.csv")
data_emp = pd.read_csv("employees.csv")

#Remove duplicates 
data_office = data_emp.drop_duplicates(subset = 'office_code',inplace=False) 
data_customers = data_orders.drop_duplicates(subset = 'customer_number',inplace=False)
data_order_info = data_orders.drop_duplicates(subset = 'order_number',inplace=False) 

#Transfer data to list of tuples, so psycopg2 can read them
data_prod_tuple = list(map(tuple, data_prod.itertuples(index=False)))
data_orders_tuple = list(map(tuple, data_orders.itertuples(index=False)))
data_emp_tuple = list(map(tuple, data_emp.itertuples(index=False)))
data_office_tuple = list(map(tuple, data_office.itertuples(index=False)))
data_customers_tuple = list(map(tuple, data_customers.itertuples(index=False)))
data_order_info_tuple = list(map(tuple, data_order_info.itertuples(index=False)))

#Coonect to database hw1
conn = psycopg2.connect("dbname=hw1 user=postgres host=localhost")
cur = conn.cursor()

#Load data into database
#INSERT INTO TABLE products
for i in data_prod_tuple:   
    cur.execute("INSERT INTO products (product_line, product_code, product_name, product_scale, product_vendor, product_description, quantity_in_stock, buy_price, _m_s_r_p, html_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", i)

#INSERT INTO TABLE offices
for i in data_office_tuple:
    cur.execute("INSERT INTO offices (office_code, city, state, country, office_location) VALUES (%(oc)s, %(cty)s, %(ste)s, %(cnt)s, %(ol)s)", {'oc': i[0], 'cty': i[6], 'ste': i[7], 'cnt': i[8], 'ol': i[9]})

#INSERT INTO TABLE employees
for i in data_emp_tuple:
    cur.execute("INSERT INTO employees (employee_number, first_name, last_name, reports_to, job_title, office_code) VALUES (%(num)s, %(fn)s, %(ln)s, %(rt)s, %(jt)s, %(oc)s)", {'num': i[1], 'fn': i[3], 'ln': i[2], 'rt': i[4], 'jt': i[5], 'oc': i[0]})

#INSERT INTO TABLE customers
for i in data_customers_tuple:
    cur.execute("INSERT INTO customers (customer_number, customer_name, contact_last_name, contact_first_name, city, state, country, sales_rep_employee_number, credit_limit, customer_location) VALUES (%(cnum)s, %(cname)s, %(cln)s, %(cfn)s, %(cty)s, %(ste)s, %(cnty)s, %(sren)s, %(clim)s, %(cloc)s)", {'cnum': i[0], 'cname': i[11], 'cln': i[12], 'cfn': i[13], 'cty': i[14], 'ste': i[15], 'cnty': i[16], 'sren': i[17], 'clim': i[18], 'cloc': i[19]})

#INSERT INTO TABLE order_info
for i in data_order_info_tuple:
    cur.execute("INSERT INTO order_info (order_number, customer_number, order_date, required_date, shipped_date, status, comments) VALUES (%(on)s, %(cn)s, %(od)s, %(rd)s, %(sd)s, %(sts)s, %(comm)s)", {'on': i[1], 'cn': i[0], 'od': i[6], 'rd': i[7], 'sd': i[8], 'sts': i[9], 'comm': i[10]})

#INSERT INTO TABLE order_products
for i in data_orders_tuple:
    cur.execute("INSERT INTO order_products (order_number, order_line_number, product_code, quantity_ordered, price_each) VALUES (%(on)s, %(oln)s, %(pc)s, %(qo)s, %(pe)s)", {'on': i[1], 'oln': i[5], 'pc': i[2], 'qo': i[3], 'pe': i[4]})

#Commit close connection
conn.commit()
cur.close()
conn.close()
