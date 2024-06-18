import mysql.connector
import csv
import os
import pandas as pd
import time
import tkinter as tk
from tkinter import ttk, messagebox

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@123',
    'database': 'emprec'
}

def execute_query(query, params=None, fetch=False):
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        cursor = mydb.cursor()
        if params:
            cursor.callproc(query, params)
        else:
            cursor.callproc(query)
        if fetch:
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            return results
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def add_student():
    student_id = entry_id.get()
    student_name = entry_name.get()
    marks = entry_marks.get()
    class_ = entry_class.get()
    sec = entry_sec.get()
    if student_id and student_name and marks and class_ and sec:
        execute_query('AddStudent', (student_id, student_name, marks, class_, sec))
        refresh_table()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

def update_student():
    student_id = entry_id.get()
    student_name = entry_name.get()
    marks = entry_marks.get()
    class_ = entry_class.get()
    sec = entry_sec.get()
    if student_id:
        execute_query('UpdateStudent', (student_id, student_name, marks, class_, sec))
        refresh_table()
    else:
        messagebox.showwarning("Input Error", "Student ID is required")

def delete_student():
    student_id = entry_id.get()
    if student_id:
        execute_query('DeleteStudent', (student_id,))
        refresh_table()
    else:
        messagebox.showwarning("Input Error", "Student ID is required")

def refresh_table():
    try:
        for i in tree.get_children():
            tree.delete(i)
    except tk.TclError:
        pass 
        
    students = execute_query('GetStudents', fetch=True)
    if students:
        for student in students:
            tree.insert("", "end", values=student)

def main():
    root = tk.Tk()
    root.title("Student Management")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Student ID").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame, text="Student Name").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(frame, text="Marks").grid(row=0, column=2, padx=10, pady=5)
    tk.Label(frame, text="Class").grid(row=0, column=3, padx=10, pady=5)
    tk.Label(frame, text="Sec").grid(row=0, column=4, padx=10, pady=5)

    global entry_id, entry_name, entry_marks, entry_class, entry_sec
    entry_id = tk.Entry(frame)
    entry_id.grid(row=1, column=0, padx=10, pady=5)
    entry_name = tk.Entry(frame)
    entry_name.grid(row=1, column=1, padx=10, pady=5)
    entry_marks = tk.Entry(frame)
    entry_marks.grid(row=1, column=2, padx=10, pady=5)
    entry_class = tk.Entry(frame)
    entry_class.grid(row=1, column=3, padx=10, pady=5)
    entry_sec = tk.Entry(frame)
    entry_sec.grid(row=1, column=4, padx=10, pady=5)

    add_button = tk.Button(frame, text="Add Student", command=add_student)
    add_button.grid(row=2, column=0, padx=10, pady=5)
    update_button = tk.Button(frame, text="Update Student", command=update_student)
    update_button.grid(row=2, column=1, padx=10, pady=5)
    delete_button = tk.Button(frame, text="Delete Student", command=delete_student)
    delete_button.grid(row=2, column=2, padx=10, pady=5)

    global tree
    tree_frame = tk.Frame(root)
    tree_frame.pack(padx=20, pady=10)
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, columns=("ID", "NAME", "MARKS", "Class", "Sec"), show="headings", height=10, yscrollcommand=tree_scroll.set)
    tree.pack()

    tree.heading("ID", text="ID")
    tree.heading("NAME", text="NAME")
    tree.heading("MARKS", text="MARKS")
    tree.heading("Class", text="Class")
    tree.heading("Sec", text="Sec")

    tree_scroll.config(command=tree.yview)
    refresh_table()

    root.mainloop()

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

def main_file_processor():
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
    import threading
    t1 = threading.Thread(target=main)
    t2 = threading.Thread(target=main_file_processor)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
