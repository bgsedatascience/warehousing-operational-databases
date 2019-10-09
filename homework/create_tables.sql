--SQL file to initialize database.

CREATE DATABASE salesdata;
\c salesdata;

CREATE TABLE customers (
customer_number INTEGER PRIMARY KEY,
customer_location VARCHAR,
customer_name VARCHAR,
contact_last_name VARCHAR,
contact_first_name VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
CREDIT_LIMIT FLOAT
);

CREATE TABLE employees (
employee_number INTEGER PRIMARY KEY,
office_code INTEGER,
last_name VARCHAR,
first_name VARCHAR,
reports_to FLOAT,
job_title VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);

CREATE TABLE orders (
order_number INTEGER PRIMARY KEY,
order_date VARCHAR,
sales_rep_employee_number INTEGER
);

CREATE TABLE order_items (
order_item_id INTEGER PRIMARY KEY,
order_number INTEGER,
product_code VARCHAR,
quantity_ordered INTEGER,
price_each FLOAT,
order_line_number INTEGER,
required_date VARCHAR,
shipped_date VARCHAR,
status VARCHAR,
comments VARCHAR
);

CREATE TABLE products (
product_code VARCHAR PRIMARY KEY,
product_line VARCHAR,
product_name VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
quantity_in_stock INTEGER,
buy_price FLOAT,
_m_s_r_p FLOAT,
product_description VARCHAR,
html_description VARCHAR
);