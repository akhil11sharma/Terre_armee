# Import necessary libraries
import mysql.connector
import datetime
import csv

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",
    database="payment"
)
cursor = mydb.cursor()

# Define the CSV file name to read data from
filename = "payment.csv"

# Open the CSV file and create a CSV reader object
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Read the header row (first line) of the CSV file
    a = next(csvreader)
    
    # Iterate over each row in the CSV file
    for row in csvreader:
        print(row)
        
        # Extract values from each column in the row
        Payment_id = int(row[0])
        Date_of_Transaction = str(row[1])
        Donar_ID = int(row[2])
        Donar_name = row[3]
        Amount = int(row[4])
        Transaction_ID = row[5]
       
        # Define the SQL query to insert data into the PaymentDetails table
        sql = "INSERT INTO PaymentDetails (Payment_id, Date_of_transaction, Donar_ID, Donar_name, Amount, Transaction_ID) VALUES (%s, %s, %s, %s, %s, %s)"
        
        # Define the values to be inserted
        val = (Payment_id, Date_of_Transaction, Donar_ID, Donar_name, Amount, Transaction_ID)
        
        # Execute the SQL query with the given values
        cursor.execute(sql, val)

# Commit the transaction to save the changes to the database
mydb.commit()
