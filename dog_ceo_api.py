import requests
import sqlite3

DB_NAME = "final_project.db"

def reset_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS DogImages")
    cur.execute("DROP TABLE IF EXISTS DogBreeds")
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogBreeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_name TEXT UNIQUE
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogImages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_id INTEGER,
            image_url TEXT UNIQUE,
            FOREIGN KEY (breed_id) REFERENCES DogBreeds(id)
        );
    ''')
    conn.commit()
    conn.close()

def parse_breed_from_url(url):
    parts = url.split("/")
    if "breeds" in parts:
        breed_info = parts[parts.index("breeds") + 1]
        breed = breed_info.replace("-", " ").capitalize()
        return breed
    return "Unknown"

def fetch_and_store_breeds():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for _ in range(25):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        if response.status_code != 200:
            continue

        image_url = response.json()["message"]
        breed_name = parse_breed_from_url(image_url)

        cur.execute('''
            INSERT OR IGNORE INTO DogBreeds (breed_name)
            VALUES (?)
        ''', (breed_name,))
        
        cur.execute('SELECT id FROM DogBreeds WHERE breed_name = ?', (breed_name,))
        breed_id = cur.fetchone()[0]

        cur.execute('''
            INSERT OR IGNORE INTO DogImages (breed_id, image_url)
            VALUES (?, ?)
        ''', (breed_id, image_url))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    reset_db()  # <-- Clear old tables
    init_db()   # <-- Create new ones
    fetch_and_store_breeds()  # <-- Populate them

