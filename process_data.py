import sqlite3
import matplotlib.pyplot as plt

DB_NAME = "final_project.db"

def calculate_and_write_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get average fact length
    cur.execute("SELECT AVG(length) FROM DogFacts")
    avg_length = cur.fetchone()[0]

    # Count how many facts are in each category
    cur.execute('''
        SELECT FactLengthCategory.category_name, COUNT(DogFacts.id)
        FROM DogFacts
        JOIN FactLengthCategory ON DogFacts.category_id = FactLengthCategory.id
        GROUP BY DogFacts.category_id
    ''')
    category_counts = cur.fetchall()

    # Count number of unique dog breeds
    cur.execute("SELECT COUNT(*) FROM DogBreeds")
    total_breeds = cur.fetchone()[0]

    # Save results to a .txt file
    with open("calculated_results.txt", "w") as f:
        f.write(f"Average dog fact length: {avg_length:.2f} characters\n\n")
        f.write("Fact count by length category:\n")
        for category, count in category_counts:
            f.write(f"- {category}: {count} facts\n")
        f.write(f"\nTotal dog breeds collected: {total_breeds}\n")

    conn.close()
    return category_counts

def create_bar_chart(category_counts):
    categories = [item[0] for item in category_counts]
    counts = [item[1] for item in category_counts]

    plt.figure(figsize=(8, 5))
    plt.bar(categories, counts)
    plt.xlabel("Fact Length Category")
    plt.ylabel("Number of Facts")
    plt.title("Number of Dog Facts by Length Category")
    plt.savefig("fact_length_bar_chart.png")
    plt.show()

def create_histogram():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT length FROM DogFacts")
    lengths = [row[0] for row in cur.fetchall()]
    conn.close()

    plt.figure(figsize=(8, 5))
    plt.hist(lengths, bins=10, edgecolor="black")
    plt.xlabel("Fact Length (characters)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Dog Fact Lengths")
    plt.savefig("fact_length_histogram.png")
    plt.show()

if __name__ == "__main__":
    counts = calculate_and_write_stats()
    create_bar_chart(counts)
    create_histogram()