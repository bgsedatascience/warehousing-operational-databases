import pandas as pd
import dataset


def create_table(df, columns):
    table = df[columns].copy()
    table = table.drop_duplicates().reset_index(drop=True)
    table = table.where((pd.notnull(table)), None)
    return table.to_dict('records')


# data processing
products = pd.read_csv('extracts/products.csv')
products_table = create_table(products, products.columns)

employees = pd.read_csv('extracts/employees.csv')
offices_columns = ['office_code', 'city', 'state', 'country', 'office_location']
employees_columns = ['employee_number', 'last_name', 'first_name', 'reports_to', 'job_title', 'office_code']
offices_table = create_table(employees, offices_columns)
employees_table = create_table(employees, employees_columns)

orders = pd.read_csv('extracts/orders.csv')
customers_columns = ['customer_number', 'customer_name', 'contact_last_name', 'contact_first_name',
                     'city', 'state', 'country', 'credit_limit', 'customer_location']
orders_columns = ['order_number', 'customer_number', 'order_date', 'required_date',
                  'shipped_date', 'status', 'comments', 'sales_rep_employee_number']
items_columns = ['order_number', 'order_line_number', 'product_code',
                 'quantity_ordered', 'price_each']
customers_table = create_table(orders, customers_columns)
orders_table = create_table(orders, orders_columns)
items_table = create_table(orders, items_columns)


# data loading
data_base = dataset.connect("postgresql://postgres@localhost/data_base_hw01")

products = data_base['products']
offices = data_base['offices']
employees = data_base['employees']
customers = data_base['customers']
orders = data_base['orders']
items = data_base['items']

products.insert_many(products_table)
offices.insert_many(offices_table)
employees.insert_many(employees_table)
customers.insert_many(customers_table)
orders.insert_many(orders_table)
items.insert_many(items_table)

data_base.commit()
