import sqlite3

from models.movie import make_movie

database = "apidb.db"

def does_user_exist(email):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    result = False
    cursor.execute(f"CREATE TABLE IF NOT EXISTS users (id text PRIMARY KEY, name text NOT NULL, email text NOT NULL, password text NOT NULL);")

    cursor.execute("SELECT count(*) FROM users WHERE email=?", (email,))

    if cursor.fetchone()[0] == 1:
        result = True
    conn.commit()
    conn.close()

    return result

def get_user_password(email):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email = ? ;", (email, ))
    conn.commit()

    return cursor.fetchone()[0]

def check_api_key(key):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    result = False
    #cursor.execute(f"CREATE TABLE IF NOT EXISTS users (id text PRIMARY KEY, name text NOT NULL, email text NOT NULL, password text NOT NULL);")
    cursor.execute("SELECT count(*) FROM users WHERE id=?", (key,))

    if cursor.fetchone()[0] == 1:
        result = True

    conn.commit()
    conn.close()
    return result


def get_api_key(email):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=?", (email,))

    conn.commit()

    return cursor.fetchone()[0]

def create_user(name, email, uuid, pwd):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    #cursor.execute(f"CREATE TABLE IF NOT EXISTS users (id text PRIMARY KEY, name text NOT NULL, email text NOT NULL, password text NOT NULL);")
    cursor.execute("INSERT INTO users (id, name, email, password) VALUES (?,?,?, ?);", (str(uuid), name, email, pwd))
    conn.commit()

    conn.close()
    return True


def get_all_movies():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("Select * FROM movies")
    conn.commit()
    rv = cursor.fetchall()
    result = [make_movie(movie_data) for movie_data in rv]
    conn.close()
    return result

def get_movie_by_id(id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("Select * FROM movies WHERE id = ?", (id, ))
    conn.commit()
    result = cursor.fetchone()
    conn.close()
    return make_movie(result)

def get_movies_partial(partial):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    partial += "%"
    cursor.execute("Select id, original_title FROM movies WHERE original_title LIKE ? LIMIT 100;", (partial, ))
    conn.commit()
    rv = cursor.fetchall()
    return rv