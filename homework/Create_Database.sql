DROP DATABASE ordersdb;
CREATE DATABASE ordersdb;
\c ordersdb;

CREATE TABLE products (
product_code VARCHAR PRIMARY KEY,
product_line VARCHAR NOT NULL,
product_name VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
product_description VARCHAR,
quantity_in_stock INTEGER,
buy_price FLOAT,
html_description VARCHAR,
_m_s_r_p FLOAT
);

CREATE TABLE offices (
office_code INTEGER PRIMARY KEY,
city VARCHAR NOT NULL,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);

CREATE TABLE employees (
employee_number INTEGER PRIMARY KEY,
last_name VARCHAR NOT NULL,
first_name VARCHAR NOT NULL,
reports_to INTEGER,
job_title VARCHAR,
office_code INTEGER REFERENCES offices(office_code)
);

CREATE TABLE customers (
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR NOT NULL,
contact_last_name VARCHAR ,
contact_first_name VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
credit_limit INTEGER,
customer_location VARCHAR,
sales_rep_employee_number INTEGER REFERENCES employees(employee_number)
);

CREATE TABLE order_details (
order_number INTEGER PRIMARY KEY,
order_date DATE NOT NULL,
required_date DATE,
shipped_date DATE,
status VARCHAR,
comments VARCHAR,
customer_number INTEGER REFERENCES customers(customer_number)
);

CREATE TABLE products_ordered (
quantity_ordered INTEGER NOT NULL,
price_each FLOAT NOT NULL,
order_line_number INTEGER,
order_number INTEGER REFERENCES order_details(order_number),
product_code VARCHAR REFERENCES products(product_code)
);
