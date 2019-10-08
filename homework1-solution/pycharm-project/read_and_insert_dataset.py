import pandas as pd
import dataset
import datetime

orders = pd.read_csv("orders.csv")
employees = pd.read_csv('employees.csv')
products = pd.read_csv('products.csv').drop_duplicates()

empl = employees[['employee_number', 'last_name', 'first_name', 'reports_to', 'job_title', 'office_code']].drop_duplicates()
#print([products.isna().any()])
#print([employees.isna().any()])
#print([orders.isna().any()])
# We see from the above commented print statements: Values with NaN are in columns state, comments, shipped_date, reports_to and html_description
# in in reports_to and shipped_date, the type is not str, so we have to change it manually


# replace NaN of reports_to of boss in order to convert to int, later we will change to NULL in sql
empl['reports_to'] = empl['reports_to'].fillna(-1).astype(int)

offices = employees[['office_code', 'city', 'state', 'country', 'office_location']].drop_duplicates().fillna('')
customers = orders[['customer_number', 'customer_name', 'city', 'state', 'country', 'sales_rep_employee_number', 'credit_limit', 'customer_location']].drop_duplicates()
# fill Nan dates with default date 1111-11-11 and convert them to SQL NULL later

order_overview = orders[['order_number', 'order_date', 'required_date', 'shipped_date', 'status', 'comments', 'customer_number']].drop_duplicates()
order_overview['comments']=order_overview['comments']
order_overview[['order_date', 'required_date', 'shipped_date']]=order_overview[['order_date', 'required_date', 'shipped_date']].fillna(datetime.date(1111, 11, 11))
order_details = orders[['order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number']].drop_duplicates()

db = dataset.connect('postgresql://postgres@localhost:5432/foo')

for df, name in [ (offices, 'offices'), (empl, 'empl'),(customers, 'customers'), (products, 'products'), (order_overview, 'order_overview'),
                 (order_details, 'order_details')]:
    row_dict = df.to_dict(orient='records')
    db[name].insert_many(row_dict)

# now set (previously modified) NaN values to proper SQL NULL values
db.query('''UPDATE order_overview SET shipped_date= NULL WHERE shipped_date='1111-11-11';''')
db.query('''UPDATE empl SET reports_to= NULL WHERE reports_to=-1;''')
db.query('''UPDATE order_overview SET comments= NULL WHERE comments='NaN';''')
db.query('''UPDATE offices SET state= NULL WHERE state='NaN';''')
db.query('''UPDATE customers SET state= NULL WHERE state='NaN';''')
db.query('''UPDATE products SET html_description= NULL WHERE html_description='NaN';''')




