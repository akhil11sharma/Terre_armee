import mysql.connector
import csv
import os
import pandas as pd

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    return result is not None

def get_column_names(cursor, table_name):
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
    columns = cursor.fetchall()
    return [col[0] for col in columns]

def get_row_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
    row_count = cursor.fetchone()[0]
    return row_count

def compare_columns(existing_columns, new_columns):
    extra_columns = list(set(new_columns) - set(existing_columns))
    missing_columns = list(set(existing_columns) - set(new_columns))
    return extra_columns, missing_columns

def compare_table_columns(cursor, table_name, new_columns):
    existing_columns = get_column_names(cursor, table_name)
    extra_columns, missing_columns = compare_columns(existing_columns, new_columns)
    if extra_columns or missing_columns:
        print(f"Table '{table_name}' has the following discrepancies:")
        if extra_columns:
            print(f"- Extra columns: {', '.join(extra_columns)}")
        if missing_columns:
            print(f"- Missing columns: {', '.join(missing_columns)}")
        print("")
    return len(existing_columns)

def create_table_information_table(cursor):
    create_table_info_sql = """
    CREATE TABLE IF NOT EXISTS table_information (
        table_name VARCHAR(255) NOT NULL PRIMARY KEY,
        column_count INT NOT NULL,
        row_count INT NOT NULL DEFAULT 0
    )
    """
    cursor.execute(create_table_info_sql)

def insert_table_information(cursor, table_name, column_count, row_count):
    insert_sql = """
    INSERT INTO table_information (table_name, column_count, row_count) 
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    column_count = %s, row_count = %s
    """
    cursor.execute(insert_sql, (table_name, column_count, row_count, column_count, row_count))

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="emprec"
    )

    cursor = mydb.cursor()
    create_table_information_table(cursor)

    folder_path = r'C:\Users\Nikhil Sharma\Desktop\testing'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        table_name = os.path.splitext(filename)[0]
        
        if filename.endswith('.csv'):
            with open(file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                columns = next(csvreader)
                if table_exists(cursor, table_name):
                    column_count = compare_table_columns(cursor, table_name, [col.strip() for col in columns if col.strip()])
                    row_count = sum(1 for _ in csvreader) 
                    insert_table_information(cursor, table_name, column_count, row_count)
                else:
                    print(f"Table '{table_name}' does not exist in the database.")
                    create_table(cursor, table_name, columns)
                    row_count = sum(1 for _ in csvreader)
                    insert_table_information(cursor, table_name, len(columns), row_count)
                    
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
            columns = df.columns.tolist()
            if table_exists(cursor, table_name):
                column_count = compare_table_columns(cursor, table_name, [col.strip() for col in columns if col.strip()])
                row_count = len(df.index)  
                insert_table_information(cursor, table_name, column_count, row_count)
            else:
                print(f"Table '{table_name}' does not exist in the database.")
                create_table(cursor, table_name, columns)
                row_count = len(df.index)
                insert_table_information(cursor, table_name, len(columns), row_count)
    mydb.commit()

except mysql.connector.Error as err:
    print(f"MySQL Error: {err}")

finally:
    if 'mydb' in locals() and mydb.is_connected():
        cursor.close()
        mydb.close()
