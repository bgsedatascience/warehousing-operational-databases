DROP DATABASE my_first_database;
CREATE DATABASE my_first_database;
\c my_first_database;

CREATE TABLE customers_1 (
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR,
contact_last_name VARCHAR,
contact_first_name VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
sales_rep_employee_number INTEGER,
credit_limit MONEY,
customer_location VARCHAR
);

CREATE TABLE employees_1 (
employee_number INTEGER PRIMARY KEY,
office_code INTEGER,
last_name VARCHAR,
first_name VARCHAR,
reports_to NUMERIC,
job_title VARCHAR
);


CREATE TABLE offices_1 (
office_code INTEGER PRIMARY KEY,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);

CREATE TABLE orders_composition_1 (
order_number INTEGER,
customer_number INTEGER,
product_code VARCHAR,
quantity_ordered INTEGER,
price_each MONEY,
order_line_number INTEGER,
PRIMARY KEY (order_number, order_line_number)
);

CREATE TABLE orders_delivery_1 (
order_delivery_id INTEGER PRIMARY KEY,
order_number INTEGER,
required_date DATE,
shipped_date DATE,
price_each MONEY,
status VARCHAR,
comments VARCHAR
);

CREATE TABLE product_stock_details_1 (
product_code VARCHAR PRIMARY KEY,
product_name VARCHAR,
quantity_in_stock INTEGER,
product_description VARCHAR,
buy_price MONEY,
_m_s_r_p NUMERIC
);

CREATE TABLE products_1 (
product_code VARCHAR PRIMARY KEY,
product_line VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
html_description VARCHAR
);