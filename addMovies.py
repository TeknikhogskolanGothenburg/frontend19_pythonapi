import csv
import sqlite3


def add_to_db(result):
    conn = sqlite3.connect("apidb.db")
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS movies (id integer  PRIMARY KEY AUTOINCREMENT, budget text, original_language text, original_title text, overview text, popularity text, poster_path, release_date text, revenue text, runtime text);")
        for movie in result:
            row = tuple([item for item in movie.values()])
            cursor.execute("INSERT INTO movies (budget, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", row)
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def main():
    with open("movies_metadata.csv", encoding="utf8") as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        indexes = [2, 7, 8, 9, 10, 11, 14, 15, 16]
        headings = next(reader)
        headings = [headings[i] for i in indexes]

        result = []
        for row in reader:
            if len(row) <= 17:
                continue
            row_items = [row[i] for i in indexes]

            out = {}
            for i in range(len(headings)):
                out[headings[i]] = row_items[i]

            result.append(out)

        add_to_db(result)

if __name__ == '__main__':
    main()