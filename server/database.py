import sqlite3
from datetime import datetime, timedelta


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("sensor_data.db")


def initialize_db():
    db = get_connection()
    cursor = db.cursor()
    # create table if it doesn't exists
    initialize_tables = """

    CREATE TABLE IF NOT EXISTS movement_data (
        id INTEGER PRIMARY KEY,
        hostname TEXT,
        client_id TEXT,
        dateTime DATETIME,
        on_bed INTEGER,
        sleep_status INTEGER,
        overall_status INTEGER
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


def insert_movement_data(
    hostname, client_id, dateTime, on_bed, sleep_status, overall_status
):
    db = get_connection()
    cursor = db.cursor()
    insert_query = """
        INSERT INTO temp_sensor_data (hostname, client_id, dateTime, on_bed, sleep_status, overall_status)
        VALUES (?, ?, ?, ?);
    """
    cursor.execute(
        insert_query,
        (hostname, client_id, dateTime, on_bed, sleep_status, overall_status),
    )
    db.commit()


def get_past_five_min_movements():
    db = get_connection()
    cursor = db.cursor()

    # Define the time range (past ten minutes)
    current_time = datetime.now()
    five_minutes_ago = current_time - timedelta(minutes=5)

    # Execute the SELECT query
    query = "SELECT * FROM movement_data WHERE dateTime >= ?;"
    cursor.execute(query, (five_minutes_ago,))

    # Fetch the results
    rows = cursor.fetchall()
    return rows
