# Project Readme: Data Management and Automation

## Overview
Welcome to the Data Management and Automation project, aimed at optimizing database operations and ensuring data integrity through Python scripts and Jupyter notebooks. This project integrates with SQL Server Management Studio (SSMS) and utilizes tkinter for creating interactive graphical interfaces.

## Files Description

| File Name                                      | Description                                                                 | Libraries Used                           | Features and Usage                                                                                                                                                                                                                                                                                                   |
|-------------------------------------------------|-----------------------------------------------------------------------------|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Names_data.xlsx**                             | Example dataset for SSMS import.                                            | None                                     | Import into SSMS to explore database functionality and schema.                                                                                                                                                                                                                                                        |
| **Schema_of_all_the_tables_and_stored_procedure.ipynb** | Detailed database schemas and stored procedures.                           | None                                     | Provides comprehensive insight into database structure and operations.                                                                                                                                                                                                                                               |
| **Sort_the_Table.ipynb**                        | Initial exploration of data sorting and tkinter GUI.                        | tkinter                                  | Develops a tkinter-based GUI for dynamic data sorting.                                                                                                                                                                                                                                                                |
| **Sorting_GUI.ipynb**                           | Interactive GUI for sorting names based on criteria.                        | tkinter                                  | Enables dynamic sorting of names through an intuitive tkinter interface.                                                                                                                                                                                                                                             |
| **csv_to_database.py**                          | Automated update of database from Excel sheets.                             | pandas, pyodbc                           | Updates database within 10 seconds, creates tables if necessary, and provides a dashboard with filtration count and stop button.                                                                                                                                                                                   |
| **data_type.py**                                | Identifies and validates data types in datasets.                            | pandas                                   | Helps understand data structure and types used in datasets.                                                                                                                                                                                                                                                            |
| **folder_validation.py**                        | Validates folder contents for Excel and CSV files.                          | os                                       | Ensures folder cleanliness by prompting deletion of non-essential files.                                                                                                                                                                                                                                             |
| **formula_management.py**                       | Manages formulas across multiple database tables.                            | pandas, pyodbc                           | Automates formula updates based on folder input, enhancing database functionality.                                                                                                                                                                                                                                    |
| **validation_check_excel.py**                   | Validates Excel data for integrity and consistency.                         | pandas                                   | Highlights discrepancies caused by manual data changes, aiding in data validation.                                                                                                                                                                                                                                     |

---

## Getting Started
To begin using the project:

1. **Clone the Repository**: Clone this repository to your local machine.
   
2. **Setup Environment**: Ensure Python and necessary libraries (like tkinter, pandas, pyodbc) are installed.

3. **Database Configuration**: Configure SQL Server connection details in scripts (`csv_to_database.py`, `formula_management.py`, etc.).

4. **Run Scripts and Notebooks**: Execute scripts and notebooks as needed to automate tasks and manage data effectively.

## Additional Notes
- Customize scripts and notebooks based on specific requirements.
- For issues or improvements, refer to the project repository or contact the project owner.
