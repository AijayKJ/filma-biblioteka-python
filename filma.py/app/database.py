import sqlite3

from app.config import DB_FAILS
def savienot():
    conn = sqlite3.connect(DB_FAILS)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def izveidot_datubazi():

    conn = savienot()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS directors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            birthday DATE,
            nationality VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS actors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            birthday DATE,
            nationality VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS studios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            country VARCHAR(100),
            founded_year INTEGER,
            website VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(150) NOT NULL,
            release_year INTEGER,
            genre_id INTEGER REFERENCES genres(id),
            director_id INTEGER REFERENCES directors(id),
            runtime_minutes INTEGER,
            synopsis TEXT,
            studio_id INTEGER REFERENCES studios(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS watchlist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, movie_id)
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 10),
            body TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, movie_id)
        );

        CREATE TABLE IF NOT EXISTS movie_cast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            actor_id INTEGER NOT NULL REFERENCES actors(id),
            character_name VARCHAR(100),
            billing_order INTEGER,
            UNIQUE(movie_id, actor_id, character_name)
        );

        CREATE TABLE IF NOT EXISTS movie_awards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            actor_id INTEGER REFERENCES actors(id),
            award_name VARCHAR(100) NOT NULL,
            category VARCHAR(100),
            award_year INTEGER,
            won BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Vecākas datubāzes pielāgošana jaunajai struktūrai
    movie_columns = {
        row[1] for row in conn.execute("PRAGMA table_info(movies)")
    }

    if "studio_id" not in movie_columns:
        conn.execute(
            "ALTER TABLE movies ADD COLUMN studio_id INTEGER REFERENCES studios(id)"
        )

    # Sākotnējie dati
    if conn.execute("SELECT COUNT(*) FROM genres").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO genres (name, description) VALUES (?, ?)",
            [
                ("Sci-Fi", "Zinātniskā fantastika"),
                ("Drāma", "Nopietni stāsti"),
                ("Action", "Asa sižeta filmas"),
                ("Comedy", "Komēdijas")
            ]
        )

    if conn.execute("SELECT COUNT(*) FROM directors").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO directors
            (name, birthday, nationality)
            VALUES (?, ?, ?)""",
            ("Christopher Nolan", "1970-07-30", "Lielbritānija")
        )

    if conn.execute("SELECT COUNT(*) FROM actors").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO actors
            (name, birthday, nationality)
            VALUES (?, ?, ?)""",
            ("Leonardo DiCaprio", "1974-11-11", "ASV")
        )

    if conn.execute("SELECT COUNT(*) FROM studios").fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO studios (name, country) VALUES (?, ?)",
            ("Warner Bros.", "ASV")
        )

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO users
            (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)""",
            ("janis", "janis@epasts.lv", "parole123", "Jānis Bērziņš")
        )

    if conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO movies
            (title, release_year, genre_id, director_id,
             runtime_minutes, synopsis, studio_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                "Inception", 2010, 1, 1,
                148, "Zagļi, kas iezogas sapņos.", 1
            )
        )

    conn.commit()
    conn.close()


# =====================================================
# GALVENĀ PROGRAMMA
# =====================================================
