import sqlite3
import bcrypt
from datetime import date

# Connect to the SQLite database
conn = sqlite3.connect('greythr.db')
cursor = conn.cursor()

# Employee data provided
employees_data = [
    ("Ashish", "Raina", "ashish.raina@tebillion.com", None, None, None, None, "Pass"),
    ("Amit", "Raina", "amit.raina@tebillion.com", None, None, None, None, "Pass"),
    ("Vedhagiri", "Damodaran", "vedhagiri.damodaran@tebillion.com", None, None, None, None, "Pass"),
    ("Laxman", "Amrale", "laxman.amrale@tebillion.com", None, None, None, None, "Pass"),
    ("Vikas", "Bare", "vikas.bare@tebillion.com", None, None, None, None, "Pass"),
    ("Anirudha", "Deskmukh", "anirudha.deskmukh@tebillion.com", None, None, 1, None, "Pass"),
    ("Shrisha", "Janga", "shrisha.janga@tebillion.com", None, None, 1, None, "Pass"),
    ("Sayoni", "Mukherjee", "sayoni.mukherjee@tebillion.com", None, None, 1, None, "Pass"),
    ("Nirmiti", "Gorate", "nirmiti.gorate@tebillion.com", None, None, 1, None, "Pass"),
    ("Kali", "Muthu", "kali.muthu@tebillion.com", None, None, 2, None, "Pass"),
    ("Arunaditya", "Mishra", "arunaditya.mishra@tebillion.com", None, None, 2, None, "Pass"),
    ("SrTech", "Support", "srtech.support@tebillion.com", None, None, 2, None, "Pass"),
    ("AsTech", "Support", "astech.support@tebillion.com", None, None, 2, None, "Pass"),
    ("Akash", "Rao", "akash.rao@tebillion.com", None, None, 3, None, "Pass"),
    ("Suraj", "Chaturvedi", "suraj.chaturvedi@tebillion.com", None, None, 3, None, "Pass"),
    ("SrSale", "Eng", "srsale.eng@tebillion.com", None, None, 3, None, "Pass"),
    ("AsSale", "Eng", "assale.eng@tebillion.com", None, None, 3, None, "Pass"),
    ("Ajay", "Pingle", "ajay.pingle@tebillion.com", None, None, 6, None, "Pass"),
    ("Janhavi", "Kamat", "janhavi.kamat@tebillion.com", None, None, 6, None, "Pass"),
    ("SrFin", "Eng", "srfin.eng@tebillion.com", None, None, 6, None, "Pass"),
    ("AsFin", "Eng", "asfin.eng@tebillion.com", None, None, 6, None, "Pass"),
    ("Sarfaraz", "Khan", "sarfaraz.khan@tebillion.com", None, None, 7, None, "Pass"),
    ("Vishal", "Bambarkar", "vishal.bambarkar@tebillion.com", None, None, 7, None, "Pass"),
    ("Hardik", "Salvi", "hardik.salvi@tebillion.com", None, None, 7, None, "Pass"),
    ("Samir", "Sakore", "samir.sakore@tebillion.com", None, None, 7, None, "Pass"),
    ("Ajit", "Yadav", "ajit.yadav@tebillion.com", None, None, 7, None, "Pass"),
    ("Harsda", "Salvi", "harsda.salvi@tebillion.com", None, None, 7, None, "Pass"),
    ("Yogesh", "Kale", "yogesh.kale@tebillion.com", None, None, 7, None, "Pass"),
    ("Vishram", "Sawant", "vishram.sawant@tebillion.com", None, None, 7, None, "Pass"),
    ("Surendra", "Manushare", "surendra.manushare@tebillion.com", None, None, 9, None, "Pass"),
    ("Deepa", "Mhatre", "deepa.mhatre@tebillion.com", None, None, 9, None, "Pass"),
    ("Kramit", "Meher", "kramit.meher@tebillion.com", None, None, 9, None, "Pass"),
    ("Pradip", "Kalukhe", "pradip.kalukhe@tebillion.com", None, None, 9, None, "Pass"),
    ("Salim", "Khan", "salim.khan@tebillion.com", None, None, 8, None, "Pass"),
    ("Nikhil", "Singh", "nikhil.singh@tebillion.com", None, None, 8, None, "Pass"),
    ("Kishan", "Panchal", "kishan.panchal@tebillion.com", None, None, 8, None, "Pass"),
    ("Karan", "Chinchpure", "karan.chinchpure@tebillion.com", None, None, 8, None, "Pass"),
]

# SQL INSERT statement (updated to include password)
insert_query = """
INSERT INTO employee (firstName, lastName, email, phone, hireDate, departmentID, managerID, password)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

try:
    # Set default hire date (today's date)
    default_hire_date = date.today().isoformat()  # Format: '2025-05-24'

    # Counter for inserted and skipped records
    inserted_count = 0
    skipped_count = 0

    for employee in employees_data:
        # Check if email already exists
        cursor.execute("SELECT email FROM employee WHERE email = ?", (employee[2],))
        if cursor.fetchone():
            print(f"Skipping duplicate email: {employee[2]}")
            skipped_count += 1
            continue

        # Hash the password
        hashed_password = bcrypt.hashpw(employee[7].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert the employee record
        cursor.execute(insert_query, (
            employee[0],  # firstName
            employee[1],  # lastName
            employee[2],  # email
            employee[3],  # phone
            default_hire_date if employee[4] is None else employee[4],  # hireDate
            employee[5],  # departmentID
            employee[6],  # managerID
            hashed_password  # password
        ))
        inserted_count += 1

    # Commit the transaction
    conn.commit()
    print(f"Inserted {inserted_count} employee records successfully. Skipped {skipped_count} duplicates.")

except sqlite3.Error as e:
    # Roll back in case of error
    conn.rollback()
    print(f"Error occurred: {str(e)}")

finally:
    # Close the connection
    conn.close()