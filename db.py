import sqlite3

DB_NAME = "game.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance INTEGER DEFAULT 100,
            score INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drinks (
            drink_id INTEGER PRIMARY KEY AUTOINCREMENT,
            drink_name TEXT NOT NULL UNIQUE,
            price INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            drink_name TEXT NOT NULL,
            success INTEGER NOT NULL,
            reward INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (player_id)
            REFERENCES players(player_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            day INTEGER DEFAULT 1,
            starting_balance INTEGER,
            ending_balance INTEGER,
            total_score INTEGER DEFAULT 0,

            FOREIGN KEY (player_id)
            REFERENCES players(player_id)
        )
    """)

    conn.commit()
    conn.close()


def create_player(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO players (name, balance, score)
        VALUES (?, 100, 0)
    """, (name,))

    player_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return player_id


def get_player(player_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_id, name, balance, score
        FROM players
        WHERE player_id = ?
    """, (player_id,))

    player = cursor.fetchone()

    conn.close()

    return player


def update_balance(player_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE players
        SET balance = balance + ?
        WHERE player_id = ?
    """, (amount, player_id))

    conn.commit()
    conn.close()
