import dataset

db = dataset.connect('postgresql://postgres@localhost:5432/foo')
print(db.tables)

employees_in_db = db['order_overview']
print(employees_in_db.columns)
for employee in employees_in_db:
   print(employee['required_date'])
#print(len(db['customers']))