# Import libraries
import pandas as pd

# Import datasets
employees=pd.read_csv("./extracts/employees.csv")
products=pd.read_csv("./extracts/products.csv")
orders=pd.read_csv("./extracts/orders.csv")


# Inspect datasets
print("Employees")
print(employees.shape)
print(employees.head())

print("Products")
print(products.shape)
print(products.head())

print("Orders")
print(orders.shape)
print(orders.head())


# Check if reporting system is standard and linked to job titles
print(employees.groupby('job_title').reports_to.nunique()) # Report-to is unique to the different office-position combinations

print(products.groupby('product_line').product_code.nunique()) # This is linked to the product code
print(products.groupby('html_description').product_code.nunique()) # Every value is NaN, we can drop this variable
print(products.product_name.nunique()) # Product name is also unique (hypothesis was that product code is the cartesian product of product name and scale)


print(max(orders.groupby('customer_name').sales_rep_employee_number.nunique())) # Since this is 1, Sales reps are unique to the customers, not the orders
print(products[products.product_code=="S18_1749"]) # Prices in the Products and Orders tables do not match, therefore we cannot streamline with that

# Function to check if primary keys are valid
def prim_key_checker(df):
    """
    Assumes that primary key is the first column of the dataframe
    Check whether primary key variable has null values or whether it is unique
    """
    if df.iloc[:,0].isnull().values.any() | df.iloc[:,0].nunique()<len(df.iloc[:,0]):
        print("There is a problem with the primary key!!")
    else:
        print("Primary key is in good format") ##MAKE IT TYPEERROR ETC!!

def new_table_inspector(df):
    print(df.shape) # MAKE OUTPUTS MORE UNDERSTANDABLE!!
    print(df.head())
    print(prim_key_checker(df))

# EMPLOYEE TABLE
# Split data into new, normalized tables according to 3NF
employee=employees[['employee_number','last_name','first_name','reports_to',
                    'job_title','office_code']].drop_duplicates()

# Fill NaN values with 'NULL'
#values={'reports_to':''}
#employee=employee.fillna(value=values)

# Inspect datasets
print(new_table_inspector(employee))

# OFFICE TABLE
# Split data into new, normalized tables according to 3NF
office=employees[['office_code','city','state','country',
                    'office_location',]].drop_duplicates()

print(office.dtypes)

# Inspect datasets
print(new_table_inspector(office))

# PRODUCTS TABLE
# Split data into new, normalized tables according to 3NF
products=products[['product_code','product_name','product_line','product_scale',
                     'product_vendor','product_description',
                    'quantity_in_stock','buy_price',
                    '_m_s_r_p']].drop_duplicates()

# Replace characters to be able to separate them when import/export csv files
#products['product_description'] = products['product_description'].str.replace(',',';')
#products['product_description'] = products['product_description'].str.strip()
#products['product_description'] = products['product_description'].str.replace('\n','', regex=False)


# Inspect datasets
print(new_table_inspector(products))


# CUSTOMERS TABLE
# Split data into new, normalized tables according to 3NF
customers=orders[['customer_number','customer_name','contact_last_name','contact_first_name',
                     'city','state',
                    'country','sales_rep_employee_number',
                    'credit_limit','customer_location']].drop_duplicates()

# Inspect datasets
print(new_table_inspector(customers))


# ORDERS TABLE
# Split data into new, normalized tables according to 3NF
order=orders[['order_number','product_code','customer_number','quantity_ordered',
                     'price_each','order_line_number',
                    'order_date','required_date',
                    'shipped_date','status','comments']].drop_duplicates()

# Set a unique ID for inspection purposes
order.set_index(['order_number', 'product_code'])
order["unique_id"]=order.index.values

# Reset column order
order = order[['unique_id','order_number','product_code','customer_number','quantity_ordered',
                     'price_each','order_line_number',
                    'order_date','required_date',
                    'shipped_date','status','comments']]

# Inspect datasets
print(new_table_inspector(order))


# INSTERT FILES INTO the Databases
print(products.iloc[37,5])
print(products.iloc[38,5])

employee.to_csv('./employee.csv', index = None, header=True,sep=';')
office.to_csv('./office.csv', index = None, header=True,encoding='utf-8',sep=';')
products.to_csv('./products.csv', index = None, header=True,sep=';')
order.to_csv('./order.csv', index = None, header=True,sep='|')
customers.to_csv('./customers.csv', index = None, header=True,sep=';')

# Import needed libraries
import psycopg2

# TABLE 1
conn = psycopg2.connect("host=localhost dbname=company user=postgres")
cur = conn.cursor()

with open('employee.csv', 'r') as f:

    next(f) # Skip the header row.
    cur.copy_from(f, 'employee', sep=';',null='')

conn.commit()

# TABLE 2
conn = psycopg2.connect("host=localhost dbname=company user=postgres")
cur = conn.cursor()

with open('order.csv', 'r') as f:

    next(f) # Skip the header row.
    cur.copy_from(f, 'orders', sep='|',null='')

conn.commit()

# Other tables

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres@localhost:5432/company')

products.to_sql('products', engine,index=False,if_exists='append')
customers.to_sql('customers', engine,index=False,if_exists='append')
office.to_sql('offices', engine,index=False,if_exists='append')


# Define primary key
conn = psycopg2.connect("dbname=company  user=postgres host=localhost")
cur = conn.cursor()
cur.execute('alter table offices add primary key (office_code);')
conn.commit()

conn = psycopg2.connect("dbname=company  user=postgres host=localhost")
cur = conn.cursor()
cur.execute('alter table customers add primary key (customer_number);')
conn.commit()

conn = psycopg2.connect("dbname=company  user=postgres host=localhost")
cur = conn.cursor()
cur.execute('alter table products add primary key (product_code);')
conn.commit()

## Sanity check
conn = psycopg2.connect("dbname=company  user=postgres host=localhost")
cur = conn.cursor()
cur.execute('SELECT * FROM products limit 10;')
res = cur.fetchall()

for row in res:
    print(row)

conn.close()
