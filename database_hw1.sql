-- author: pedro freitas NIS: 173976

DROP DATABASE hw1;
CREATE DATABASE hw1;
\c hw1

CREATE TABLE products (
	product_line text,
	product_code text PRIMARY KEY,
	product_name text,
	product_scale text,
	product_vendor text,
	product_description text,
	quantity_in_stock integer,
	buy_price NUMERIC,
	_m_s_r_p text,
	html_description text
	);

CREATE TABLE offices (
	office_code integer PRIMARY KEY,
	city text,
	state text,
	country text,
	office_location text
	);

CREATE TABLE employees (
	employee_number integer PRIMARY KEY,
	first_name text,
	last_name text,
	reports_to text,
	job_title text,
	office_code integer REFERENCES offices(office_code)
	);

CREATE TABLE customers (
	customer_number integer PRIMARY KEY,
	customer_name text,
	contact_last_name text,
	contact_first_name text,
	city text,
	state text,
	country text,
	sales_rep_employee_number integer REFERENCES employees(employee_number),
	credit_limit integer,
	customer_location text
	);

CREATE TABLE order_info (
	order_number integer PRIMARY KEY,
	customer_number integer REFERENCES customers(customer_number),
	order_date date,
	required_date date,
	shipped_date text,
	status text,
	comments text
	);

CREATE TABLE order_products (
	order_number integer REFERENCES order_info(order_number),
	order_line_number integer,
	product_code text REFERENCES products(product_code),
	quantity_ordered integer,
	price_each NUMERIC,
	PRIMARY KEY (order_number, order_line_number)
	);