DROP DATABASE alex
CREATE DATABASE alex
\c alex

CREATE TABLE employee_id AS (
SELECT employee_number, last_name, first_name ,job_title, office_code
FROM employees);

CREATE TABLE office_info AS (
SELECT office_code, reports_to, city, state, country
FROM employees);

CREATE TABLE product_inventory AS (
SELECT product_code, product_name, quantity_in_stock, html_description
FROM products);

CREATE TABLE production AS (
SELECT product_code, product_line, product_scale, product_vendor, buy_price, _m_s_r_p
FROM products);

CREATE TABLE order_log AS (
SELECT orders_id,customer_number, order_number, product_code, quantity_ordered, price_each, order_line_number, order_date, required_date, shipped_date, status, comments
FROM orders);

CREATE TABLE customers AS (
SELECT orders_id,customer_number, customer_name, contact_last_name, contact_first_name, city, state, country, sales_rep_employee_number, credit_limit, customer_location
FROM orders);
