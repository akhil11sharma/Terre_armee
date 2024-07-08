# Terre_armee Internship Project

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Files and Scripts](#files-and-scripts)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This repository contains the work done during the Terre_armee internship. The primary objective is to transfer data from Excel files to a MySQL server. The project includes scripts for manually and automatically transferring data, updating MySQL tables based on Excel file changes, and creating JSON objects from Excel sheets to post to a local API.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/akhil11sharma/Terre_armee.git
    cd Terre_armee/Internship
    ```

2. Install the required libraries:
    ```bash
    pip install pandas mysql-connector-python
    ```

3. Ensure you have MySQL server installed and running.

## Usage
### Table_area.py
This script allows users to select Excel files through a Tkinter dialog box and transfer the data to a MySQL server. The table is created based on the file's base name.

To run the script:
```bash
python Table_area.py
```

### automatic.py
This script automatically transfers data from a specified folder to the MySQL server every 30 seconds. It detects changes in the Excel/CSV files and updates the corresponding MySQL tables.

To run the script:
```bash
python automatic.py
```

### excel_to_mysql.py
A basic script for testing the transfer of data from Excel to MySQL without any automation or UI.

To run the script:
```bash
python excel_to_mysql.py
```

### json_API.ipynb
A Jupyter notebook to generate JSON objects from Excel sheets and post them to a local API.

To run the notebook, open it in Jupyter:
```bash
jupyter notebook json_API.ipynb
```

### main.py
Initial script to test data transfer from Excel to MySQL, focusing on columns and headers.

To run the script:
```bash
python main.py
```

## Features
- Interactive UI using Tkinter to select and transfer Excel files to MySQL.
- Automatic data transfer and update detection.
- JSON object generation from Excel sheets for API posting.

## Files and Scripts
- **Table_area.py**: Interactive script for selecting and transferring Excel files.
- **automatic.py**: Automated script for periodic data transfer and update detection.
- **excel_to_mysql.py**: Basic script for manual data transfer testing.
- **json_API.ipynb**: Jupyter notebook for JSON object creation and API posting.
- **main.py**: Initial data transfer script with column and header management.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
