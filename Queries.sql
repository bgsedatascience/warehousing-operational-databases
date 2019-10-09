CREATE TABLE employee_id (
SELECT employee_number, last_name, first_name ,job_title, office_code
FROM employees);

CREATE TABLE office_info (
SELECT office_code, reports_to, city, state, country,
FROM employees);



CREATE TABLE product_inventory (
SELECT product_code, product_name, quantity_in_stock, html_description
FROM products);

CREATE TABLE production (
SELECT product_code, product_line, product_scale, product_vendor, buy_price, _m_s_r_p,
FROM products);




CREATE TABLE orders (
SELECT customer_number, order_number, product_code, quantity_ordered, price_each, order_line_number, order_date, required_date, shipping_date, status, comments
FROM orders);

CREATE TABLE customers (
SELECT customer_number, customer_name, contact_last_name, contact_first_name, city, state, country, sales_rep_employee_number, credit_limit,
FROM orders);
