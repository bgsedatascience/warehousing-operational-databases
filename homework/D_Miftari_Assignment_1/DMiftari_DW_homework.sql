DROP DATABASE dw_database_assignment;
CREATE DATABASE dw_database_assignment;
\c dw_database_assignment;

CREATE TABLE offices (
office_code INTEGER PRIMARY KEY,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);

--offices = employees[['office_code', 'city', 'state', 'country', 'office_location']].copy()


CREATE TABLE employees_info (
employee_number INTEGER PRIMARY KEY,
last_name VARCHAR,
first_name VARCHAR,
reports_to VARCHAR,
job_title VARCHAR,
office_code INTEGER REFERENCES offices(office_code)
);

--employees_info = employees[['employee_number', 'last_name', 'first_name', 'reports_to', 'job_title', 'office_code']].copy()

CREATE TABLE customers (
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR,
contact_last_name VARCHAR,
contact_first_name VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
customer_location VARCHAR
);

--customers = orders[['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name', 'city', 'state',
--                    'country', 'customer_location']].copy()


CREATE TABLE products (
product_code VARCHAR PRIMARY KEY,
product_line VARCHAR,
product_name VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
product_description VARCHAR,
quantity_in_stock INTEGER,
buy_price MONEY,
_m_s_r_p MONEY,
html_description VARCHAR
);

--products = products[['product_line', 'product_code', 'product_name', 'product_scale', 'product_vendor',
--                     'product_description', 'quantity_in_stock', 'buy_price', '_m_s_r_p', 'html_description']].copy()


CREATE TABLE product_orders (
order_number INTEGER PRIMARY KEY,
customer_number INTEGER REFERENCES customers(customer_number),
order_line_number INTEGER,
order_date DATE,
required_date DATE,
shipped_date DATE,
status VARCHAR
);

--product_orders = orders[['customer_number', 'order_number', 'order_date', 'required_date', 'shipped_date', 'status']].copy()

CREATE TABLE item_orders (
product_code VARCHAR REFERENCES products(product_code),
order_number INTEGER REFERENCES product_orders(order_number),
quantity_ordered INTEGER,
price_each MONEY,
order_line_number INTEGER
);

--item_orders = orders[['order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']].copy()
--item_orders = item_orders.drop_duplicates()