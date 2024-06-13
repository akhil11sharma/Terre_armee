import mysql.connector
import csv
import os
import pandas as pd

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    return result is not None

def create_table(cursor, table_name, columns):
    columns = [col.strip() for col in columns if col.strip()]
    columns_with_types = ", ".join([f"`{col}` VARCHAR(255)" for col in columns])
    create_table_sql = f"CREATE TABLE `{table_name}` ({columns_with_types})"
    print(f"Executing SQL: {create_table_sql}")
    cursor.execute(create_table_sql)
    return columns

def insert_data(cursor, table_name, columns, values):
    if len(columns) != len(values):
        print(f"Skipping row due to column/value mismatch: {values}")
        return
    columns_str = ", ".join([f"`{col}`" for col in columns])
    placeholders = ", ".join(["%s"] * len(values))
    insert_sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
    cursor.execute(insert_sql, values)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",
    database="emprec"
)

cursor = mydb.cursor()

folder_path = r'C:\Users\Nikhil Sharma\Desktop\testing'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    table_name = os.path.splitext(filename)[0]
    
    if filename.endswith('.csv'):
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            columns = next(csvreader)
            if not table_exists(cursor, table_name):
                columns = create_table(cursor, table_name, columns)
            else:
                columns = [col.strip() for col in columns if col.strip()]
            for row in csvreader:
                print(f"Inserting row: {row}")
                insert_data(cursor, table_name, columns, row)
    
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        columns = df.columns.tolist()
        if not table_exists(cursor, table_name):
            columns = create_table(cursor, table_name, columns)
        else:
            columns = [col.strip() for col in columns if col.strip()]
        for _, row in df.iterrows():
            print(f"Inserting row: {row.tolist()}")
            insert_data(cursor, table_name, columns, row.tolist())

mydb.commit()
cursor.close()
mydb.close()
