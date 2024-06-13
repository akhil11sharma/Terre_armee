import mysql.connector
import csv
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123"
)
cursor = mydb.cursor()
cursor.execute("USE emprec")
cursor.execute("""
    CREATE TABLE Emprec_Records (
        EmpID INT PRIMARY KEY,
        Empname VARCHAR(255),
        Empage INT,
        EmpDept VARCHAR(255)
    )
""")
filename = "test_data.csv"
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader) 
    for row in csvreader:
        EmpID = int(row[0])
        Empname = row[1]
        Empage = int(row[2])
        EmpDept = row[3]
        sql = "INSERT INTO Emprec_Records (EmpID, Empname, Empage, EmpDept) VALUES (%s, %s, %s, %s)"
        val = (EmpID, Empname, Empage, EmpDept)
        cursor.execute(sql, val)
mydb.commit()
cursor.close()
mydb.close()

print("Data has been inserted successfully.")
