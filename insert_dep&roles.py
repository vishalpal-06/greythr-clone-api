import sqlite3

# Connect to the existing SQLite database using the absolute path
conn = sqlite3.connect(r'greythr.db')
cursor = conn.cursor()

# --- Department Insertion ---
# List of departments to insert with their descriptions
departments = [
    ("Human Resources", "Manages employee relations and recruitment"),
    ("Tech Support", "Provides technical assistance to employees"),
    ("Sales", "Handles sales operations and client acquisition"),
    ("Marketing", "Manages branding and promotional activities"),
    ("Customer Support", "Assists customers with inquiries and issues"),
    ("Finance", "Oversees financial planning and accounting"),
    ("TEB", "Technology and Engineering Business unit"),
    ("Data", "Manages data analytics and insights"),
    ("MobileApp", "Develops and maintains mobile applications")
]

# Insert departments, skipping duplicates
try:
    # Check existing department names to avoid duplicates
    cursor.execute('SELECT departmentName FROM department')
    existing_depts = {row[0] for row in cursor.fetchall()}
    
    # Filter out departments that already exist
    new_depts = [dept for dept in departments if dept[0] not in existing_depts]
    
    if new_depts:
        cursor.executemany('''
            INSERT INTO department (departmentName, description)
            VALUES (?, ?)
        ''', new_depts)
        conn.commit()
        print(f"Inserted {len(new_depts)} new departments successfully.")
    else:
        print("No new departments to insert (all departments already exist).")

    # Verify inserted departments
    cursor.execute('SELECT departmentID, departmentName, description FROM department')
    print("\nAll departments in the table:")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}")

except sqlite3.Error as e:
    print(f"Error in department insertion: {e}")

# --- Role Insertion ---
# List of roles: CEO, CFO, CTO (organization-wide), VP, AVP, Manager, Lead, Sr, Associate for each department
roles = [
    # Organization-wide executive roles (only one VP and AVP here)
    ("CEO", "Chief Executive Officer overseeing the entire organization"),
    ("CFO", "Chief Financial Officer managing financial strategy"),
    ("CTO", "Chief Technology Officer overseeing tech initiatives"),
    ("VP", "Vice President overseeing overall strategy"),
    ("AVP", "Assistant Vice President supporting VP responsibilities"),

    # Departmental Roles (NO VPs or AVPs)
    ("HR Manager", "Manages HR operations and employee relations"),
    ("Lead HR", "Leads HR initiatives like recruitment and policy development"),
    ("Senior HR Specialist", "Handles complex HR tasks and compliance"),
    ("Associate HR Specialist", "Supports recruitment and employee data management"),

    ("Tech Support Manager", "Manages the tech support team and issue resolution"),
    ("Lead Tech Support", "Leads troubleshooting and technical assistance"),
    ("Senior Tech Support Specialist", "Resolves advanced technical issues"),
    ("Associate Tech Support Specialist", "Provides basic technical support"),

    ("Sales Manager", "Manages the sales team and performance metrics"),
    ("Lead Sales", "Leads sales initiatives and client acquisition"),
    ("Senior Sales Executive", "Manages key accounts and sales strategies"),
    ("Associate Sales Executive", "Supports lead generation and client outreach"),

    ("Marketing Manager", "Manages marketing operations and campaigns"),
    ("Lead Marketing", "Leads marketing initiatives like digital campaigns"),
    ("Senior Marketing Specialist", "Develops advanced marketing strategies"),
    ("Associate Marketing Specialist", "Supports marketing campaigns and research"),

    ("Customer Support Manager", "Manages the customer support team"),
    ("Lead Customer Support", "Leads customer inquiry and escalation handling"),
    ("Senior Customer Support Specialist", "Resolves complex customer issues"),
    ("Associate Customer Support Specialist", "Provides basic customer assistance"),

    ("Finance Manager", "Manages financial operations and payroll"),
    ("Lead Finance", "Leads financial planning and budgeting"),
    ("Senior Finance Analyst", "Conducts advanced financial analysis"),
    ("Associate Finance Analyst", "Assists with financial data and payroll"),

    ("TEB Manager", "Manages technology and engineering projects"),
    ("Lead TEB Engineer", "Leads engineering projects within TEB"),
    ("Senior TEB Engineer", "Handles complex engineering tasks"),
    ("Associate TEB Engineer", "Supports engineering and development tasks"),

    ("Data Manager", "Manages data operations and analytics"),
    ("Lead Data Engineer", "Leads data pipeline and analytics projects"),
    ("Senior Data Engineer", "Builds and optimizes data systems"),
    ("Associate Data Engineer", "Supports data processing and analysis"),

    ("MobileApp Manager", "Manages mobile app development team"),
    ("Lead MobileApp Developer", "Leads mobile app feature development"),
    ("Senior MobileApp Developer", "Develops and optimizes mobile apps"),
    ("Associate MobileApp Developer", "Supports mobile app development tasks")
]

# Insert roles, skipping duplicates
try:
    # Get existing role names
    cursor.execute('SELECT roleName FROM role')
    existing_roles = {row[0] for row in cursor.fetchall()}
    
    # Filter out roles that already exist
    new_roles = [role for role in roles if role[0] not in existing_roles]
    
    if new_roles:
        cursor.executemany('''
            INSERT INTO role (roleName, description)
            VALUES (?, ?)
        ''', new_roles)
        conn.commit()
        print(f"\nInserted {len(new_roles)} new roles successfully.")
    else:
        print("\nNo new roles to insert (all roles already exist).")

    # Verify inserted roles
    cursor.execute('SELECT roleID, roleName, description FROM role')
    print("\nAll roles in the table:")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}")

except sqlite3.Error as e:
    print(f"Error in role insertion: {e}")

finally:
    conn.close()