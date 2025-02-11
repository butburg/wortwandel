import sqlite3
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def save_dataframe_to_db(df, table_name="data", db_path="dwh_data.db", if_exists="append"):
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
    connection = sqlite3.connect(db_path)
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
    connection = sqlite3.connect(db_path)
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
