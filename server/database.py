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
        client_id TEXT,
        dateTime DATETIME,
        temperature REAL
    );
    """

    cursor.execute(initialize_tables)
    db.commit()


def insert_temp_data(hostname, client_id, dateTime, temperature):
    db = get_connection()
    cursor = db.cursor()
    insert_query = """
        INSERT INTO temp_sensor_data (hostname,client_id, dateTime, temperature)
        VALUES (?, ?, ?, ?);
    """
    cursor.execute(insert_query, (hostname, client_id, dateTime, temperature))
    db.commit()
