DROP DATABASE foo;
CREATE DATABASE foo;
\c foo;
CREATE TABLE empl (
employee_number INTEGER PRIMARY KEY,
last_name VARCHAR,
first_name VARCHAR,
reports_to INTEGER,
job_title VARCHAR,
office_code INTEGER
);

CREATE TABLE offices (
office_code INTEGER PRIMARY KEY,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);

CREATE TABLE customers (
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
sales_rep_employee_number VARCHAR,
credit_limit INTEGER,
customer_location VARCHAR
);

CREATE TABLE order_overview (
order_number INTEGER PRIMARY KEY,
order_date DATE,
required_date DATE,
shipped_date DATE,
status VARCHAR,
comments VARCHAR,
customer_number INTEGER
);

CREATE TABLE order_details (
order_number INTEGER,
product_code VARCHAR,
quantity_ordered INTEGER,
price_each FLOAT,
order_line_number INTEGER
);

CREATE TABLE products (
product_code VARCHAR PRIMARY KEY,
product_line VARCHAR,
product_name VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
product_description VARCHAR,
quantity_in_stock INTEGER,
buy_price FLOAT,
_m_s_r_p FLOAT,
html_description VARCHAR
);
