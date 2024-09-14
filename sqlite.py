import sqlite3
from datetime import datetime

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS user_entries")

# Create the table with the new 'link' field
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_entries (
        userid INTEGER,
        timestamp TEXT,
        textfield TEXT,
        link TEXT,
        UNIQUE(userid, timestamp)
    )
''')
conn.commit()

def insert_entry(userid, timestamp, textfield, link):
    try:
        cursor.execute('''
            INSERT INTO user_entries (userid, timestamp, textfield, link)
            VALUES (?, ?, ?, ?)
        ''', (userid, timestamp, textfield, link))
        conn.commit()
        print("Entry inserted successfully")
    except sqlite3.IntegrityError:
        print("Error: This userid and timestamp combination already exists")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def check_user_and_get_links(userid, timestamp):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT timestamp, textfield, link
            FROM user_entries
            WHERE userid = ? AND timestamp < ?
            ORDER BY timestamp DESC
        ''', (userid, timestamp))

        results = cursor.fetchall()

        if results:
            print(f"Entries found for user {userid} before {timestamp}")
            return results
        else:
            print(f"No entries found for user {userid} before {timestamp}")
            return []
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()

# Example usage
# Insert some sample data
insert_entry(1, "2023-09-14T10:00:00", "First entry", "http://example.com/1")
insert_entry(1, "2023-09-14T11:00:00", "Second entry", "http://example.com/2")
insert_entry(2, "2023-09-14T12:00:00", "Entry for user 2", "http://example.com/3")

# Check for user entries and get link
userid_to_check = 1
timestamp_to_check = "2023-09-14T23:59:59"

entries = check_user_and_get_links(userid_to_check, timestamp_to_check)
if entries:
    for entry in entries:
        timestamp, textfield, link = entry
        print(f"Timestamp: {timestamp}")
        print(f"Text: {textfield}")
        print(f"Link: {link}")
        print("---")
else:
    print("No entries found")

# Close the connection when done
conn.close()
