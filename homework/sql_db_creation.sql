DROP DATABASE company;
CREATE DATABASE company ;
\c company;

CREATE TABLE employee (
employee_number INTEGER PRIMARY KEY,
last_name VARCHAR NOT NULL,
first_name VARCHAR NOT NULL,
reports_to FLOAT,
job_title VARCHAR,
office_code INTEGER
);

CREATE TABLE office (
office_code BIGINT PRIMARY KEY,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);


/*
CREATE TABLE products (
product_code VARCHAR PRIMARY KEY,
product_name VARCHAR,
product_line VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
product_description VARCHAR,
quantity_in_stock INTEGER,
buy_price FLOAT,
_m_s_r_p FLOAT
);
*/

/*
CREATE TABLE customers (
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR,
contact_last_name VARCHAR,
contact_first_name VARCHAR,
city VARCHAR,
state VARCHAR,
country VARCHAR,
sales_rep_employee_number INTEGER,
credit_limit FLOAT,
customer_location VARCHAR
);
*/

CREATE TABLE orders (
unique_id INTEGER,
order_number INTEGER,
product_code VARCHAR,
PRIMARY KEY (order_number, product_code),
customer_number INTEGER,
quantity_ordered INTEGER,
order_line_number FLOAT,
price_each FLOAT,
order_date DATE,
required_date DATE,
shipped_date DATE,
status VARCHAR,
comments VARCHAR
);
