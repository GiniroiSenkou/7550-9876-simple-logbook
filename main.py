import sqlite3
import datetime
import re

# Connect to the database
conn = sqlite3.connect('logbook.db')
c = conn.cursor()

# Create a table to store the log entries
c.execute('''CREATE TABLE IF NOT EXISTS log_entries
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             sentence TEXT,
             date TEXT,
             time TEXT)''')

# Function to add an entry to the logbook
def add_entry(sentence):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    
    # Check if the sentence contains a time
    time_match = re.search(r'\d{2}:\d{2}:\d{2}', sentence)
    if time_match:
        time = time_match.group()
    else:
        time = now.strftime("%H:%M:%S")
    
    c.execute("INSERT INTO log_entries (sentence, date, time) VALUES (?, ?, ?)", (sentence, date, time))
    conn.commit()
    print("Added")

# Function to display the last three entries
def display_last_entries():
    c.execute("SELECT * FROM log_entries ORDER BY id DESC LIMIT 3")
    entries = c.fetchall()
    print("Last Three Entries:")
    for entry in entries:
        print(f"Date: {entry[2]}, Time: {entry[3]}, Sentence: {entry[1]}")

# Main program loop
while True:
    sentence = input("Enter a sentence (or 'q' to quit): ")
    if sentence.lower() == 'q':
        break
    elif 'l' in sentence.lower():
        display_last_entries()
    else:
        add_entry(sentence)

# Close the database connection
conn.close()
