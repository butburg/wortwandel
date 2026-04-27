import sqlite3
import pandas as pd
import logging
import os.path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_db_connection(db_path):
    """Create a SQLite connection with sensible defaults for ETL workloads."""
    connection = sqlite3.connect(os.path.normpath(db_path))
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = NORMAL")
    return connection


def initialize_dwh_schema(connection):
    """
    Initialize the DWH schema using a hybrid key strategy:
    - Surrogate primary key: newspaper_id
    - Natural key uniqueness: newspaper_name + data_published
    """
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS newspapers (
            newspaper_id INTEGER PRIMARY KEY AUTOINCREMENT,
            newspaper_name TEXT NOT NULL,
            data_published TEXT NOT NULL,
            klima_mentions_count INTEGER NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS context (
            context_id INTEGER PRIMARY KEY AUTOINCREMENT,
            newspaper_id INTEGER NOT NULL,
            pre_context TEXT NOT NULL,
            post_context TEXT NOT NULL,
            prefix TEXT NOT NULL,
            suffix TEXT NOT NULL,
            FOREIGN KEY (newspaper_id) REFERENCES newspapers(newspaper_id)
        )
        """
    )

    try:
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS ux_newspapers_name_date
            ON newspapers(newspaper_name, data_published)
            """
        )
    except sqlite3.IntegrityError:
        logging.warning(
            "Could not create UNIQUE index ux_newspapers_name_date due to existing duplicates. "
            "ETL upsert logic will still prevent new duplicates."
        )

    # Keep repeated sentences within one newspaper-day if they genuinely occur on the page.
    # Idempotency is guaranteed by skipping already imported newspaper_name+date rows.
    connection.execute("DROP INDEX IF EXISTS ux_context_newspaper_text")

    connection.execute(
        "CREATE INDEX IF NOT EXISTS ix_context_newspaper_id ON context(newspaper_id)"
    )


def upsert_newspaper(cursor, newspaper_name, data_published, klima_mentions_count):
    """Insert one newspaper row if needed and return (newspaper_id, was_inserted)."""
    row = cursor.execute(
        """
        SELECT newspaper_id
        FROM newspapers
        WHERE newspaper_name = ? AND data_published = ?
        ORDER BY newspaper_id
        LIMIT 1
        """,
        (newspaper_name, data_published),
    ).fetchone()

    if row:
        newspaper_id = row[0]
        cursor.execute(
            """
            UPDATE newspapers
            SET klima_mentions_count = ?
            WHERE newspaper_id = ?
            """,
            (int(klima_mentions_count), int(newspaper_id)),
        )
        return int(newspaper_id), False

    cursor.execute(
        """
        INSERT INTO newspapers (newspaper_name, data_published, klima_mentions_count)
        VALUES (?, ?, ?)
        """,
        (str(newspaper_name), str(data_published), int(klima_mentions_count)),
    )
    return int(cursor.lastrowid), True


def insert_context_rows(cursor, newspaper_id, contexts):
    """Insert all context rows for a newly inserted newspaper_id."""
    if not contexts:
        return 0

    rows_to_insert = []
    for context in contexts:
        pre_context = "" if context.get("pre_context") is None else str(context.get("pre_context"))
        post_context = "" if context.get("post_context") is None else str(context.get("post_context"))
        prefix = "" if context.get("prefix") is None else str(context.get("prefix"))
        suffix = "" if context.get("suffix") is None else str(context.get("suffix"))
        rows_to_insert.append((int(newspaper_id), pre_context, post_context, prefix, suffix))

    if rows_to_insert:
        cursor.executemany(
            """
            INSERT INTO context (newspaper_id, pre_context, post_context, prefix, suffix)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows_to_insert,
        )

    return len(rows_to_insert)


def save_dataframe_to_db(df, table_name, db_path, if_exists="append"):
    """
    Save a pandas DataFrame to a SQLite table.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        table_name (str): The name of the table in the database.
        connection (sqlite3.Connection): SQLite connection object.
        if_exists (str): How to behave if the table already exists. Options are 'fail', 'replace', 'append'.

    Returns:
        None
    """
    connection = get_db_connection(db_path)
    try:
        df.to_sql(table_name, connection, if_exists=if_exists, index=False)
        logging.info(f"Data saved to table '{table_name}' in '{db_path}' successfully.")
    except Exception as e:
        logging.error(f"Error saving DataFrame to database: {e}")
        raise
    finally:
        connection.close()


def read_table_as_dataframe(table_name="data", db_path="dwh_data.db"):
    """
    Read a SQLite table into a pandas DataFrame.

    Parameters:
        table_name (str): The name of the table to read from the database.
        connection (sqlite3.Connection): SQLite connection object.

    Returns:
        pd.DataFrame: DataFrame containing the table data.
    """
    connection = get_db_connection(db_path)
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, connection)
        logging.info(f"Data read from table '{table_name}' in '{db_path}' successfully.")
        return df
    except Exception as e:
        logging.error(f"Error reading table '{table_name}': {e}")
        raise
    finally:
        connection.close()


# Example usage:
if __name__ == "__main__":
    # Example DataFrame
    data = {"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]}
    df = pd.DataFrame(data)

    # Save the DataFrame to a table
    save_dataframe_to_db(df, "example", db_path="example_handle_sqlite.db", if_exists="replace")

    # Read the table back into a DataFrame
    result_df = read_table_as_dataframe("example", db_path="example_handle_sqlite.db")
    print(result_df)
