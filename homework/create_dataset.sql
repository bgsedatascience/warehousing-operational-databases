DROP DATABASE ds_assignment1;
CREATE DATABASE ds_assignment1;
\c ds_assignment1;

CREATE TABLE offices (
	office_code INTEGER PRIMARY KEY
);

CREATE TABLE employees (
	employee_number INTEGER  PRIMARY KEY,
	office_code INTEGER REFERENCES offices(office_code)
);

CREATE TABLE customers (
	customer_number INTEGER PRIMARY KEY
);

CREATE TABLE orders (
	order_number INTEGER PRIMARY KEY,
	customer_number INTEGER REFERENCES customers(customer_number),
	sales_rep_employee_number INTEGER REFERENCES employees(employee_number)
);

CREATE TABLE products (
	product_code VARCHAR PRIMARY KEY,
	html_description VARCHAR
);

CREATE TABLE products_ordered (
	order_number INTEGER REFERENCES orders(order_number),
	product_code VARCHAR REFERENCES products(product_code)
);
