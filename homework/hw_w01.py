import pandas as pd
import psycopg2
import ast

#-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #--
#
# db_connection Class
#
#-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #--
class db_connection():
    """Class to handle the database connection"""
    def __init__(self,
                 dbname="company_db",
                 user="postgres",
                 host="localhost"):
        """Constructor initialises connection and cursor"""
        self.configure_conn(dbname, user, host)
        self.connect()
        self.open_cursor()

    def __del__(self):
        """Destructor to tidy up if required"""
        if self.cur is not None:
            self.close_cursor()
        if self.conn is not None:
            self.disconnect()

    def connect(self):
        """Connect to configured host"""
        conn_str = f"dbname={self.dbname} user={self.user} host={self.host}"
        self.conn = psycopg2.connect(conn_str)

    def configure_conn(self, dbname, user, host):
        """Configure connection"""
        self.dbname=dbname
        self.user=user
        self.host=host

    def disconnect(self, close_cursor_b=False):
        """Close connection to database"""
        if close_cursor_b:
            self.close_cursor
        self.conn.close()
        self.conn = None

    def is_connected(self):
        """Check if connection is active"""
        if self.conn is None:
            return False
        else:
            return True

    def open_cursor(self):
        """Open database cursor"""
        self.cur = self.conn.cursor()

    def close_cursor(self):
        """Close database cursor"""
        self.cur.close()
        self.cur = None

    def select_query(self, query):
        """Execute SELECT query"""
        self.cur.execute(query)
        return self.cur.fetchall()

    def insert_query(self, query, var_tuple):
        """Execute INSERT query"""
        self.cur.execute(query, var_tuple)
        self.conn.commit()

    def _delete_query(self, query):
        """Execute DELETE query :: Testing only"""
        # Not a fan of providing direct delete methods, testing only...
        self.cur.execute(query)
        self.conn.commit()

#-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #--
#
# Module functions to construct queries and insert records
#
#-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #--
def build_query(row, table, query_type):
    """Construct query from row for table"""
    # Abstracted to allow for additon of UPDATE and SELECT later on
    # if required
    if query_type == "INSERT":
        return build_insert_query(row, table)
    else:
        return ""

def build_insert_query(row, table):
    """Construct insert query from row for table"""
    query_columns = ""
    variable_list = list()
    for key in row.keys():
        # Insert is columns then values, so construct as two strings
        query_columns += f"{key}, "
        # Use format value to handle value types in SQL
        variable_list.append(row[key])
    values = "%s, " * len(row.keys())
    # Index to -2 to remove ", " from last value
    query = f"INSERT INTO {table} ({query_columns[:-2]}) VALUES ({values[:-2]})"
    return query, variable_list

def load_table(conn, table_name, frame):
    """Load a dataframe into a specified table"""
    # Build table
    for index, row in frame.iterrows():
        query_str, var_tuple = build_query(row, table_name, "INSERT")
        #print(query_str)
        conn.insert_query(query_str, var_tuple)

def _torch_tables(conn, tables=['products', 'orders',
                                'customers', 'employees', 'offices',  ]):
    """Delete the contents of the database"""
    # This is for testing only, method should not be used.
    for table in tables:
        conn._delete_query(f"DELETE FROM {table};")

def load_products_file(conn, filename):
    """Load the records from the products file"""
    products = pd.read_csv(filename)
    # From products, take all columns
    load_table(conn, 'products', products)

def load_orders_file(conn, filename):
    """Load the records from the orders file"""
    orders_full = pd.read_csv(filename)
    # Convert byte columns to string literals
    orders_full["customer_location"] = (orders_full["customer_location"]
        .apply(ast.literal_eval))
    # Fix nulls to None as it messes with the dates
    orders_full = orders_full.where(pd.notnull(orders_full), None)
    # Split orders into three tables; customers, orders and order_items
    load_customers_table(conn, orders_full)
    #Second part, orders
    load_orders_table(conn, orders_full)
    # Third part, order_items
    load_order_items_table(conn, orders_full)

def load_customers_table(conn, orders_full):
    """Load the records into the customers_table"""
    customers_col_list = ['customer_number', 'customer_name',
                          'contact_last_name', 'contact_first_name',
                          'city', 'state', 'country',
                          'sales_rep_employee_number', 'credit_limit',
                          'customer_location']
    customers_df = orders_full[customers_col_list].drop_duplicates()
    load_table(conn, 'customers', customers_df)

def load_orders_table(conn, orders_full):
    """Load the records into the orders table"""
    orders_col_list = [ 'order_number', 'customer_number', 'order_date',
                       'required_date', 'shipped_date', 'status',
                       'comments' ]
    orders_df = orders_full[orders_col_list].drop_duplicates()
    load_table(conn, 'orders', orders_df)

def load_order_items_table(conn, orders_full):
    """Load the records into the order_items table"""
    # Create new index for order_item that combines the order_number with the
    # line number
    orders_full["order_item_number"] = (orders_full["order_number"]
        .astype(str) + "-" +
        orders_full["order_line_number"].astype(str))
    order_items_col_list = [ 'order_item_number', 'order_number',
                            'product_code', 'quantity_ordered',
                            'price_each', 'order_line_number']
    order_items_df = orders_full[order_items_col_list]
    load_table(conn, 'order_items', order_items_df)

def load_employees_file(conn, filename):
    """Load the records from the employees_file"""
    employees_full = pd.read_csv(filename)
    employees_full["office_location"] = (employees_full["office_location"]
        .apply(ast.literal_eval))
    # Split the employees table into two tables; offices and employees
    load_office_table(conn, employees_full)
    # Second part, employees
    load_employees_table(conn, employees_full)

def load_office_table(conn, employees_full):
    """Load the records into the offices table"""
    offices_col_list = {'office_code', 'city', 'state', 'country',
                        'office_location' }
    offices_df = employees_full[offices_col_list].drop_duplicates()
    load_table(conn, 'offices', offices_df)

def load_employees_table(conn, employees_full):
    """Load the records into the employees table"""
    employees_col_list = {'employee_number', 'last_name', 'first_name',
                          'reports_to', 'job_title'}
    employees_df = employees_full[employees_col_list]
    load_table(conn, 'employees', employees_df)

#-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #--
#
# Code to execute the loads
#
#-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #-- #--
if __name__ == "__main__":
    # Create database db_connection
    conn = db_connection()
    load_products_file(conn, "extracts/products.csv")
    load_employees_file(conn, 'extracts/employees.csv')
    load_orders_file(conn, 'extracts/orders.csv')
    if conn.is_connected():
        conn.disconnect(True)
    print("Insert complete.")
