# another try with dataset, can also be used for display of tables
import dataset

db = dataset.connect('postgresql://postgres@localhost:5432/foo')
print(db.tables)
table = db['empl']
print(table.columns)
for row in table:
   print(row['office_code'])
#print(len(db['customers']))