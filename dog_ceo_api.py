import requests
import sqlite3

DB_NAME = "final_project.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogBreeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_name TEXT,
            image_url TEXT UNIQUE
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

    for _ in range(25):  # Only 25 per run
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        if response.status_code != 200:
            continue

        image_url = response.json()["message"]
        breed_name = parse_breed_from_url(image_url)

        cur.execute('''
            INSERT OR IGNORE INTO DogBreeds (breed_name, image_url)
            VALUES (?, ?)
        ''', (breed_name, image_url))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    fetch_and_store_breeds()