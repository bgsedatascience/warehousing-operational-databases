DROP DATABASE hw1_data_warehouse;

CREATE DATABASE hw1_data_warehouse;
\c hw1_data_warehouse;

CREATE TABLE employees_new(
office_code INTEGER,
employee_number INTEGER PRIMARY KEY,
last_name VARCHAR,
first_name VARCHAR,
reports_to VARCHAR,
job_title VARCHAR);

CREATE TABLE offices_a(
office_code INTEGER PRIMARY KEY,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR);

CREATE TABLE order_metadata_a(
order_number INTEGER PRIMARY KEY,
order_date DATE,
required_date DATE,
shipped_date DATE,
status VARCHAR,
comments VARCHAR,
rep_employee_number INTEGER);

CREATE TABLE orders_new_a(
orders_unique_id INTEGER PRIMARY KEY,
customer_number INTEGER,
order_number INTEGER,
product_code VARCHAR,
quantity_ordered INTEGER,
price_each FLOAT,
order_line_number INTEGER,
status VARCHAR,
comments VARCHAR,
rep_employee_number INTEGER);

CREATE TABLE products_a(
product_line VARCHAR,
product_code VARCHAR PRIMARY KEY,
product_name VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
product_description VARCHAR,
quantity_in_stock INTEGER,
buy_price FLOAT,
_m_s_r_p FLOAT,
html_description VARCHAR
);

CREATE TABLE customers_a(
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR,
contact_last_name VARCHAR,
contact_first_name VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
credit_lim INTEGER,
customer_location VARCHAR);

