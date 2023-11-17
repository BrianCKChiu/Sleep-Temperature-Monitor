import sqlite3


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("sensor_data.db")


def initialize_db():
    db = get_connection()
    cursor = db.cursor()
    # create table if it doesn't exists
    initialize_tables = """
      CREATE TABLE IF NOT EXISTS temp_sensor_data (
        id INTEGER PRIMARY KEY,
        hostname TEXT,
        dateTime DATETIME,
        temperature REAL
    );
    """

    cursor.execute(initialize_tables)
    db.commit()


def insert_temp_data(hostname, dateTime, temperature):
    db = get_connection()
    cursor = db.cursor()
    insert_query = """
        INSERT INTO temp_sensor_data (hostname, dateTime, temperature)
        VALUES (?, ?, ?);
    """
    cursor.execute(insert_query, (hostname, dateTime, temperature))
    db.commit()
