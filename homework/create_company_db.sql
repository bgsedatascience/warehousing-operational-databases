DROP DATABASE company_db;
CREATE DATABASE company_db;
\c company_db;

CREATE TABLE products(
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

CREATE TABLE offices(
        office_code INTEGER PRIMARY KEY,
        city VARCHAR,
        state VARCHAR,
        country VARCHAR,
        office_location BYTEA
      );

CREATE TABLE employees(
        employee_number INTEGER PRIMARY KEY,
        last_name VARCHAR,
        first_name VARCHAR,
        reports_to VARCHAR,
        job_title VARCHAR,
        office_code INTEGER REFERENCES offices(office_code)
      );

CREATE TABLE customers(
        customer_number INTEGER PRIMARY KEY,
        customer_name VARCHAR,
        contact_first_name VARCHAR,
        contact_last_name VARCHAR,
        city VARCHAR,
        state VARCHAR,
        country VARCHAR,
        sales_rep_employee_number INTEGER REFERENCES employees(employee_number),
        credit_limit MONEY,
        customer_location BYTEA
      );

CREATE TABLE orders(
      order_number INTEGER PRIMARY KEY,
      customer_number INTEGER REFERENCES customers(customer_number),
      order_date DATE,
      required_date DATE,
      shipped_date DATE,
      status VARCHAR,
      comments VARCHAR
    );

CREATE TABLE order_items(
       order_item_number VARCHAR PRIMARY KEY,
       order_number INTEGER REFERENCES orders(order_number),
       product_code VARCHAR,
       quantity_ordered INTEGER,
       price_each INTEGER,
       order_line_number INTEGER
     );
