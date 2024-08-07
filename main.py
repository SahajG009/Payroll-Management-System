# Importing Dependencies
import mysql.connector as ms
# used for connection checking
from connection import is_connected, get_database_connection
# used for payslip
from tabulate import tabulate

# Establishing Connection
flag = is_connected()
# print(flag)

# Database to be used
db = "CompanyManagementDB"
db_tables = ["employees","departments","projects","employee_project","salaries"]
print(f"Using {db} Database")
print(f"All actions will happen inside {db} database")

if flag:
    try:
        # Checking if connected
        connection = get_database_connection()
        cursor = connection.cursor()

        # Selecting the database
        cursor.execute(f"USE {db};")
        print(f"Database changed to {db}")

        # Sample query to test the connection
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables in the database:", tables)
        
        # Function to insert data into a table
        def insert_data():
            print("The table names are listed below")
            for i in range(len(db_tables)):
                print(i+1,'.',db_tables[i])
            table_name = input("Enter the table name to insert data into: ").lower()
            
            if table_name == "employees":
                emp_no = int(input("Enter employee number: "))
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                job_title = input("Enter job title: ")
                basic_salary = float(input("Enter basic salary: "))
                department_id = int(input("Enter department id: "))
                query = "INSERT INTO Employees (emp_no, first_name, last_name, job_title, basic_salary, department_id) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (emp_no, first_name, last_name, job_title, basic_salary, department_id)

            elif table_name == "departments":
                department_id = int(input("Enter department id: "))
                department_name = input("Enter department name: ")
                manager_id = int(input("Enter manager id: "))
                query = "INSERT INTO Departments (department_id, department_name, manager_id) VALUES (%s, %s, %s)"
                values = (department_id, department_name, manager_id)
                
            elif table_name == "projects":
                project_id = int(input("Enter project id: "))
                project_name = input("Enter project name: ")
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                department_id = int(input("Enter department id: "))
                query = "INSERT INTO Projects (project_id, project_name, start_date, end_date, department_id) VALUES (%s, %s, %s, %s, %s)"
                values = (project_id, project_name, start_date, end_date, department_id)
                
            elif table_name == "employee_project":
                emp_no = int(input("Enter employee number: "))
                project_id = int(input("Enter project id: "))
                hours_worked = float(input("Enter hours worked: "))
                query = "INSERT INTO Employee_Project (emp_no, project_id, hours_worked) VALUES (%s, %s, %s)"
                values = (emp_no, project_id, hours_worked)
                
            elif table_name == "salaries":
                emp_no = int(input("Enter employee number: "))
                salary_date = input("Enter salary date (YYYY-MM-DD): ")
                basic_salary = float(input("Enter basic salary: "))

                # da , hra Calculation
                print("Is the Employee's residence rented?(Y/N): ")
                ans = input().strip()
                if ans == 'Y':
                    fda,fhra = 0.5,0.4
                    da = fda * basic_salary
                    hra = fhra * basic_salary
                else:
                    da,hra = 0.5,0
                    da = fda * basic_salary
                    hra = fhra * basic_salary
                gross_salary = basic_salary + da + hra

                # Tax based on Indian tax slabs
                taxable_income = gross_salary - basic_salary
                if taxable_income <= 250000:
                    tax = 0
                elif taxable_income <= 500000:
                    tax = 0.05 * (taxable_income - 250000)
                elif taxable_income <= 1000000:
                    tax = 12500 + 0.2 * (taxable_income - 500000)
                else:
                    tax = 112500 + 0.3 * (taxable_income - 1000000)
                
                # net salary calculated
                net_salary = gross_salary - tax
                
                query = "INSERT INTO Salaries (emp_no, salary_date, basic_salary, da, hra, gross_salary, tax, net_salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (emp_no, salary_date, basic_salary, da, hra, gross_salary, tax, net_salary)
                
            else:
                print("Invalid table name.")
                return
            
            cursor.execute(query, values)
            connection.commit()
            print(f"Data inserted into {table_name} table successfully.")


        # Function to update data in a table
        def update_data():
            print("The table names are listed below")
            for i in range(len(db_tables)):
                print(i+1,'.',db_tables[i])
            table_name = input("Enter the table name to update data into: ").lower()
            
            if table_name == "employees":
                emp_no = int(input("Enter the employee number to update: "))
                column_name = input("Enter the column name to update: ")
                new_value = input("Enter the new value: ")
                query = f"UPDATE Employees SET {column_name} = %s WHERE emp_no = %s"
                values = (new_value, emp_no)

            elif table_name == "departments":
                department_id = int(input("Enter the department id to update: "))
                column_name = input("Enter the column name to update: ")
                new_value = input("Enter the new value: ")
                query = f"UPDATE Departments SET {column_name} = %s WHERE department_id = %s"
                values = (new_value, department_id)
                
            elif table_name == "projects":
                project_id = int(input("Enter the project id to update: "))
                column_name = input("Enter the column name to update: ")
                new_value = input("Enter the new value: ")
                query = f"UPDATE Projects SET {column_name} = %s WHERE project_id = %s"
                values = (new_value, project_id)
                
            elif table_name == "employee_project":
                emp_no = int(input("Enter the employee number to update: "))
                project_id = int(input("Enter the project id to update: "))
                column_name = input("Enter the column name to update: ")
                new_value = input("Enter the new value: ")
                query = f"UPDATE Employee_Project SET {column_name} = %s WHERE emp_no = %s AND project_id = %s"
                values = (new_value, emp_no, project_id)
                
            elif table_name == "salaries":
                emp_no = int(input("Enter the employee number to update: "))
                salary_date = input("Enter the salary date (YYYY-MM-DD) to update: ")
                column_name = input("Enter the column name to update: ")
                new_value = input("Enter the new value: ")
                query = f"UPDATE Salaries SET {column_name} = %s WHERE emp_no = %s AND salary_date = %s"
                values = (new_value, emp_no, salary_date)
                
            else:
                print("Invalid table name.")
                return
            
            cursor.execute(query, values)
            connection.commit()
            print(f"Data in {table_name} table updated successfully.")

        # Function to delete data from a table
        def delete_data():
            print("The table names are listed below")
            for i in range(len(db_tables)):
                print(i+1,'.',db_tables[i])
            table_name = input("Enter the table name to delete data from: ").lower()
            
            if table_name == "employees":
                emp_no = int(input("Enter the employee number to delete: "))
                query = "DELETE FROM Employees WHERE emp_no = %s"
                values = (emp_no,)

            elif table_name == "departments":
                department_id = int(input("Enter the department id to delete: "))
                query = "DELETE FROM Departments WHERE department_id = %s"
                values = (department_id,)
                
            elif table_name == "projects":
                project_id = int(input("Enter the project id to delete: "))
                query = "DELETE FROM Projects WHERE project_id = %s"
                values = (project_id,)
                
            elif table_name == "employee_project":
                emp_no = int(input("Enter the employee number to delete: "))
                project_id = int(input("Enter the project id to delete: "))
                query = "DELETE FROM Employee_Project WHERE emp_no = %s AND project_id = %s"
                values = (emp_no, project_id)
                
            elif table_name == "salaries":
                emp_no = int(input("Enter the employee number to delete: "))
                salary_date = input("Enter the salary date (YYYY-MM-DD) to delete: ")
                query = "DELETE FROM Salaries WHERE emp_no = %s AND salary_date = %s"
                values = (emp_no, salary_date)
                
            else:
                print("Invalid table name.")
                return
            
            cursor.execute(query, values)
            connection.commit()
            print(f"Data deleted from {table_name} table successfully.")

        # Function to generate a payslip for a particular employee
        def generate_payslip():
            emp_no = int(input("Enter the employee number: "))
            salary_date = input("Enter the salary date (YYYY-MM-DD): ")

            query = """
                SELECT emp_no, salary_date, basic_salary, da, hra, gross_salary, tax, net_salary
                FROM Salaries
                WHERE emp_no = %s AND salary_date = %s
            """
            values = (emp_no, salary_date)

            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                emp_no, salary_date, basic_salary, da, hra, gross_salary, tax, net_salary = result
                
                data = [
                    ["Employee Number:", emp_no],
                    ["Salary Date:", salary_date],
                    ["Basic Salary:", basic_salary],
                    ["DA:", da],
                    ["HRA:", hra],
                    ["Gross Salary:", gross_salary],
                    ["Tax:", tax],
                    ["Net Salary:", net_salary],
                ]
                
                print("\n" + "*" * 30)
                print("PAYSLIP")
                print("*" * 30)
                print(tabulate(data, tablefmt="pretty"))
                print("*" * 30)
            else:
                print("No payslip found for the given employee number and salary date.")

        # Function to display contents of a table
        def display_table_contents():
            print("The table names are listed below")
            for i in range(len(db_tables)):
                print(i+1,'.',db_tables[i])
            table_name = input("Enter the table name to display data: ").lower()

            query = f"SELECT * FROM {table_name}"
            
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if not rows:
                    print(f"No data found in {table_name} table.")
                    return
                
                # Get column names
                column_names = [i[0] for i in cursor.description]
                
                # Print table header
                print(f"\nContents of {table_name} Table:")
                print('-' * 80)
                print(tabulate(rows, headers=column_names, tablefmt="pretty"))
                print('-' * 80)
                
            except ms.Error as e:
                print(f"Error fetching data from {table_name} table: {e}")


        # Main menu
        def main_menu():
            print('\n' + '*'*95)
            print('\t\t\t\t MAIN MENU')
            print('*'*95)
            print('\t\t\t 1. Insert data into table')
            print('\t\t\t 2. Update data in table')
            print('\t\t\t 3. Delete data from table')
            print('\t\t\t 4. Generate Payslip')
            print('\t\t\t 5. Display table contents')
            print('\t\t\t 6. Exit')
            print("Enter your choice: ", end='')

        # Menu loop 
        while True:
            main_menu()
            choice = input().strip()

            if choice == '1':
                insert_data()
            elif choice == '2':
                update_data()
            elif choice == '3':
                delete_data()
            elif choice == '4':
                generate_payslip()
            elif choice == '5':
                display_table_contents()
            elif choice == '6':
                break
            else:
                print("Please choose a valid number")

    except ms.Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
else:
    print("Failed to connect to MySQL")
