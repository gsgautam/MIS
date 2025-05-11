# instance/config.py
# This file contains your secret configurations.
# It WILL BE IGNORED by Git if 'instance/' is in your .gitignore file.

# MySQL Database Configuration
MYSQL_CONFIG = {
    'user': 'root',         # Replace with your MySQL username
    'password': 'Password@12345',     # Replace with your MySQL password
    'host': 'localhost',                   # Replace if your DB is not on localhost
    'database': 'office_mb_db',            # Your database name
    'raise_on_warnings': True
}

# Admin Signup Secret Code
ADMIN_SIGNUP_SECRET = "R"  # Choose a strong secret

# Email Account for Fetching Leads
EMAIL_ACCOUNT = "your_email_address@example.com"  # Your MIS email
EMAIL_PASSWORD = "your_email_app_password"        # For Gmail, use an App Password
IMAP_SERVER = "imap.example.com"                  # e.g., "imap.gmail.com"