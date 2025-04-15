import sqlite3

# Connects to database
conn = sqlite3.connect("final_project.db")
cur = conn.cursor()

# Count of facts by length category
print("Dog Facts by Length Category:")
cur.execute('''
    SELECT category_name, COUNT(*) 
    FROM DogFacts 
    JOIN FactLengthCategory 
    ON DogFacts.category_id = FactLengthCategory.id 
    GROUP BY category_name;
''')
for row in cur.fetchall():
    print(f"{row[0]}: {row[1]}")

print("\nTop 5 Most Frequent Dog Breeds in Images:")
# Most common breeds from DogBreeds table
cur.execute('''
    SELECT breed_name, COUNT(*) 
    FROM DogBreeds 
    GROUP BY breed_name 
    ORDER BY COUNT(*) DESC 
    LIMIT 5;
''')
for row in cur.fetchall():
    print(f"{row[0]}: {row[1]}")

cur.execute("SELECT COUNT(*) FROM DogFacts")
total_facts = cur.fetchone()[0]
print(f"\nTotal dog facts stored: {total_facts}")
# Done
conn.close()