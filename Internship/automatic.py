import mysql.connector
import csv
import os
import pandas as pd
import time

# MySQL connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@123',
    'database': 'emprec'
}

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    return result is not None

def drop_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

def create_table(cursor, table_name, columns):
    columns = [col.strip() for col in columns if col.strip()]  
    
    create_table_sql = f"""
    CREATE TABLE `{table_name}` (
        {', '.join([f"`{col}` TEXT" for col in columns])}
    )
    """
    cursor.execute(create_table_sql)

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

def insert_data_into_table(cursor, table_name, columns, data):
    placeholders = ', '.join(['%s'] * len(columns))
    insert_sql = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in columns])}) VALUES ({placeholders})"
    cursor.executemany(insert_sql, data)

def fetch_data_from_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = cursor.fetchall()
    return {tuple(row): row for row in rows}

def compare_table_columns(cursor, table_name, expected_columns):
    cursor.execute(f"DESCRIBE `{table_name}`")
    existing_columns = [row[0] for row in cursor.fetchall()]
    
    extra_columns = [col for col in expected_columns if col not in existing_columns]
    missing_columns = [col for col in existing_columns if col not in expected_columns]
    
    if extra_columns:
        print(f"Extra columns in table '{table_name}': {extra_columns}")
    
    if missing_columns:
        print(f"Missing columns in table '{table_name}': {missing_columns}")

def process_files(cursor, folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        table_name = os.path.splitext(filename)[0]
        
        if filename.endswith('.csv'):
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                columns = next(csvreader)
                columns = [col.strip() for col in columns if col.strip()]
                
                if table_exists(cursor, table_name):
                    drop_table(cursor, table_name)
                
                create_table(cursor, table_name, columns)
                compare_table_columns(cursor, table_name, columns)
                
                data = [tuple(row) for row in csvreader]
                insert_data_into_table(cursor, table_name, columns, data)
                
                insert_table_information(cursor, table_name, len(columns), len(data))
                
                print(f"Table '{table_name}' replaced with new data from CSV.")
                    
        elif filename.endswith('.xlsx'):
            with pd.ExcelFile(file_path) as xls:
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    columns = df.columns.tolist()
                    columns = [col.strip() for col in columns if col.strip()]
                    
                    if table_exists(cursor, table_name):
                        drop_table(cursor, table_name)
                    
                    create_table(cursor, table_name, columns)
                    compare_table_columns(cursor, table_name, columns)
                    
                    data = [tuple(row) for row in df.values.tolist()]
                    insert_data_into_table(cursor, table_name, columns, data)
                    
                    insert_table_information(cursor, table_name, len(columns), len(data))
                    
                    print(f"Table '{table_name}' replaced with new data from Excel sheet.")

def main():
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        cursor = mydb.cursor()
        create_table_information_table(cursor)
        folder_path = r'C:\Users\Nikhil Sharma\Desktop\testing'

        while True:
            process_files(cursor, folder_path)
            mydb.commit()
            print("Files processed. Sleeping for 60 seconds...")
            time.sleep(60)

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if 'mydb' in locals() and mydb.is_connected():
            cursor.close()
            mydb.close()

if __name__ == "__main__":
    main()
