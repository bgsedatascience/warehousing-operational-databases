CREATE DATABASE week1;
\c week1

CREATE TABLE office_info (
office_code INTEGER PRIMARY KEY,
city VARCHAR,
state VARCHAR,
country VARCHAR,
office_location VARCHAR
);
    
CREATE TABLE employee_info (
employee_number INTEGER PRIMARY KEY,
office_code INTEGER REFERENCES office_info(office_code),
last_name VARCHAR,
first_name VARCHAR,
reports_to VARCHAR,
job_title VARCHAR
);

CREATE TABLE customer_info (
customer_number INTEGER PRIMARY KEY, 
sales_rep_employee_number INTEGER REFERENCES employee_info(employee_number),
customer_name VARCHAR, 
contact_last_name VARCHAR, 
contact_first_name VARCHAR, 
city VARCHAR, 
state VARCHAR,
country VARCHAR, 
credit_limit MONEY, 
customer_location VARCHAR
);

CREATE TABLE product_info (
product_code VARCHAR PRIMARY KEY,
product_name VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR, 
product_line VARCHAR, 
product_description VARCHAR, 
quantity_in_stock INTEGER, 
buy_price MONEY, 
_m_s_r_p MONEY, 
html_description VARCHAR
);

CREATE TABLE order_items(
order_number INTEGER, 
order_line_number INTEGER, 
product_code VARCHAR REFERENCES product_info(product_code), 
quantity_ordered INTEGER, 
price_each MONEY,
PRIMARY KEY (order_number, order_line_number)
);



CREATE TABLE order_info (
order_number INTEGER PRIMARY KEY, 
customer_number INTEGER REFERENCES customer_info(customer_number), 
order_date DATE, 
required_date DATE,
status VARCHAR, 
comments VARCHAR
);