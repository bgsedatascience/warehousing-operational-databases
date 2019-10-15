DROP DATABASE car_sales;
CREATE DATABASE car_sales;
\c car_sales;

CREATE TABLE customers (
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR,
contact_last_name VARCHAR,
contact_first_name VARCHAR,
state VARCHAR,
sales_rep_employee_number INTEGER,
credit_limit MONEY,
customer_location VARCHAR
);


CREATE TABLE products (
product_code VARCHAR PRIMARY KEY,
product_line VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
html_description VARCHAR
);

CREATE TABLE employees (
employee_number INTEGER PRIMARY KEY,
office_code INTEGER,
last_name VARCHAR,
first_name VARCHAR,
reports_to NUMERIC,
job_title VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);

CREATE TABLE orders (
order_number INTEGER,
required_date DATE,
shipped_date DATE,
price_each MONEY,
status VARCHAR,
comments VARCHAR,
PRIMARY KEY (order_number, price_each)
);

CREATE TABLE measures (
total_quantity INTEGER,
sales MONEY,
profit MONEY,
total_cost MONEY,
d8d INTEGER,
d8q INTEGER,
order_date DATE,
customer_city VARCHAR,
customer_country VARCHAR,
customer_number INTEGER,
product_code VARCHAR,
office_location VARCHAR,
employee_number INTEGER,
order_number INTEGER,
order_delivery_id INTEGER
);