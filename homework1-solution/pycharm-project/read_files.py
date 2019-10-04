import pandas as pd
import dataset
import sqlalchemy



orders = pd.read_csv("orders.csv")
employees = pd.read_csv('employees.csv')
products = pd.read_csv('products.csv').drop_duplicates()

empl = employees[['employee_number', 'last_name', 'first_name', 'reports_to', 'job_title', 'office_code']].drop_duplicates()
offices = employees[['office_code', 'city', 'state', 'country', 'office_location']].drop_duplicates()
customers = orders[['customer_number', 'customer_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location']].drop_duplicates()
order_overview = orders[['order_number', 'order_date', 'required_date', 'shipped_date', 'status', 'comments', 'customer_number']].drop_duplicates()
order_details = orders[['order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']].drop_duplicates()

engine = sqlalchemy.create_engine('postgresql://postgres@localhost:5432/foo')
for df, name in [(empl, 'empl'), (offices, 'offices'), (customers, 'customers'), (order_overview, 'order_overview'),
                 (order_details, 'order_details'), (products, 'products')]:
    df.to_sql(con=engine, name=name, if_exists='replace', index=False)

