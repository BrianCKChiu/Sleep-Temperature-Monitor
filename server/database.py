import sqlite3


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("sensor_data.db")


def initialize_db():
    db = get_connection()
    cursor = db.cursor()
    # create table if it doesn't exists
    initialize_tables = """
      CREATE TABLE IF NOT EXISTS temp_sensor_data (
        id INTEGER PRIMARY KEY AUTOINCRENENT,
        hostname TEXT,
        dateTime DATETIME,
        temperature REAL
    );
    """

    cursor.execute(initialize_tables)
    db.commit()
