import requests
import sqlite3

DB_NAME = "final_project.db"

#Method init_db
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create category table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS FactLengthCategory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE
        );
    ''')

    categories = [("Short",), ("Medium",), ("Long",)]
    cur.executemany('INSERT OR IGNORE INTO FactLengthCategory (category_name) VALUES (?)', categories)

    # Create dog facts table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogFacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE,
            length INTEGER,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES FactLengthCategory(id)
        );
    ''')


    conn.commit()
    conn.close()

def categorize_length(length):
    if length <= 50:
        return "Short"
    elif length <= 100:
        return "Medium"
    else:
        return "Long"

def fetch_and_store_facts():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    response = requests.get("https://dogapi.dog/api/v2/facts?limit=25")
    if response.status_code != 200:
        print("Error fetching facts.")
        return

    facts = response.json().get("data", [])
    for item in facts:
        fact = item["attributes"]["body"]
        length = len(fact)
        category_name = categorize_length(length)

        cur.execute("SELECT id FROM FactLengthCategory WHERE category_name = ?", (category_name,))
        category_id = cur.fetchone()[0]

        cur.execute('''
            INSERT OR IGNORE INTO DogFacts (fact, length, category_id)
            VALUES (?, ?, ?)
        ''', (fact, length, category_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    fetch_and_store_facts()