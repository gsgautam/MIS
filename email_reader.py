# email_reader.py (Conceptual Example - Needs YOUR Email Details & Customization!)

import imaplib, email, sqlite3, os, re, time
from email.header import decode_header
from datetime import datetime

# =======================================================================
# === CONFIGURATION (!!! AAPKO YEH DETAILS BADALNI HONGi !!!) ===
# =======================================================================
# !! Password direct code mein likhna unsafe hai. Secure method use karein !!
EMAIL_ACCOUNT = "aapki_email_id@gmail.com"      # <-- Yahan apni Email ID daalein
EMAIL_PASSWORD = "AAPKA_APP_PASSWORD"           # <-- Yahan App Password (agar Gmail/Outlook hai aur 2FA on hai) ya normal password daalein
IMAP_SERVER = "imap.gmail.com"                # <-- Yahan apne email provider ka sahi IMAP server daalein (e.g., imap.gmail.com, outlook.office365.com)
# =======================================================================

# Database path (assuming email_reader.py is in the main project folder)
DB_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
DATABASE_PATH = os.path.join(DB_FOLDER, 'mis_database.db')

# --- Database Function ---
def add_lead_to_db(bank_name, prop_details, received_date_str, deadline_str):
    conn = None; success = False
    try:
        os.makedirs(DB_FOLDER, exist_ok=True)
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        print(f"DB Add: Bank={bank_name}, Details={prop_details}, Received={received_date_str}, Deadline={deadline_str}")
        cursor.execute('INSERT INTO leads (bank_name, property_details, received_date, deadline, status) VALUES (?, ?, ?, ?, ?)',
                       (bank_name, prop_details, received_date_str, deadline_str, 'New'))
        conn.commit(); print("DB Insert OK."); success = True
    except sqlite3.Error as e: print(f"DB Error: {e}")
    finally:
        if conn: conn.close()
    return success

# --- Email Parsing Functions ---
def get_email_body(msg):
    # ... (Code as provided before) ...
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type(); cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                try: body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore'); break
                except Exception as e: print(f"Err decode multi: {e}")
    else:
        ctype = msg.get_content_type()
        if ctype == 'text/plain':
            try: body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
            except Exception as e: print(f"Err decode single: {e}")
    return body

def parse_subject(subject_header):
    # ... (Code as provided before) ...
    subject = "No Subject"
    if subject_header:
        try:
            parts = []; decoded = decode_header(subject_header)
            for part, enc in decoded: parts.append(part.decode(enc or 'utf-8', 'ignore') if isinstance(part, bytes) else part)
            subject = "".join(parts)
        except Exception as e: print(f"Err decode subj: {e}"); subject = str(subject_header)
    return subject

# !!! --- CUSTOMIZE THIS FUNCTION HEAVILY BASED ON YOUR EMAILS --- !!!
def extract_info_from_email(subject, body, sender):
    # ... (Your custom logic using regex/string searching) ...
    # This is just a placeholder - REPLACE with your actual parsing logic
    print(f"\n--- Parsing Email --- From: {sender}, Subject: {subject}")
    bank_name = sender; prop_details = None; deadline_str = None
    received_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Example (MUST BE CHANGED)
    if body:
        match_prop = re.search(r"Property Address:\s*(.*?)(?:\n|$)", body, re.IGNORECASE | re.DOTALL)
        if match_prop: prop_details = match_prop.group(1).strip().replace('\r\n', ' ').replace('\n', ' ')[:400]
        match_date = re.search(r"Due Date:\s*(\d{4}-\d{2}-\d{2})", body, re.IGNORECASE)
        if match_date:
            try: datetime.strptime(match_date.group(1).strip(), '%Y-%m-%d'); deadline_str = match_date.group(1).strip()
            except ValueError: deadline_str = None
    print(f"Extraction: Bank={bank_name}, Details={prop_details}, Deadline={deadline_str}")
    if prop_details: return bank_name, prop_details, received_date_str, deadline_str
    else: print("Prop details not found."); return None, None, None, None

# --- Main Email Checking Logic ---
def check_emails():
    print(f"\n[{datetime.now()}] == Starting Email Check =="); added_count = 0; processed_ids = []
    try:
        # Check configuration placeholders
        if EMAIL_ACCOUNT == "your_email@example.com" or EMAIL_PASSWORD == "YOUR_APP_PASSWORD_OR_SECURE_TOKEN" or IMAP_SERVER == "imap.example.com":
             print("ERROR: Please update email credentials and server in the Configuration section of email_reader.py!")
             return 0 # Stop if config not updated

        print(f"Connecting to {IMAP_SERVER}..."); mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        print(f"Logging in as {EMAIL_ACCOUNT}..."); mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox"); print("Connected.")
        print("Searching unseen..."); status, messages = mail.search(None, "(UNSEEN)")
        if status == "OK":
            email_ids = messages[0].split(); print(f"Found {len(email_ids)} unseen.")
            for email_id in email_ids:
                current_email_id_str = email_id.decode(); print(f"\nProcessing ID: {current_email_id_str}"); processed_ids.append(email_id)
                res, msg_data = mail.fetch(email_id, "(RFC822)")
                if res == "OK":
                    for response in msg_data:
                        if isinstance(response, tuple):
                            try:
                                msg = email.message_from_bytes(response[1]); subject = parse_subject(msg["Subject"]); sender = email.utils.parseaddr(msg.get('From'))[1]
                                print(f"From: {sender}, Subject: {subject}"); body = get_email_body(msg)
                                if body:
                                    bank, prop, recv_date, deadline = extract_info_from_email(subject, body, sender)
                                    if prop and add_lead_to_db(bank, prop, recv_date, deadline): added_count += 1
                                else: print("No body found.")
                            except Exception as parse_err: print(f"Error parsing email ID {current_email_id_str}: {parse_err}")
                else: print(f"Fetch failed for ID: {current_email_id_str}")
            if processed_ids:
                 id_string = b','.join(processed_ids); print(f"\nMarking {len(processed_ids)} as read: {id_string.decode()}")
                 try: mail.store(id_string, '+FLAGS', '\\Seen')
                 except Exception as store_err: print(f"Error marking read: {store_err}")
        else: print(f"Search failed: {status}")
        mail.close(); mail.logout(); print("Logged out.")
    except imaplib.IMAP4.error as e: print(f"IMAP Error: {e}") # Specific IMAP errors
    except Exception as e: print(f"Unexpected error during email check: {e}")
    print(f"[{datetime.now()}] == Email Check Finished. Added: {added_count} ==")
    return added_count

# --- How to Run ---
if __name__ == "__main__":
     check_emails()
     # Use Task Scheduler / Cron to run this script periodically