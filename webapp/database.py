"""
Schema:

table question_category - id, name of category
table questions - id, argument 1, argument 2, answer, question_category (foreign key, index by this?)
"""

import sqlite3

from datetime import datetime
from pathlib import Path

DATABASE_PATH: Path = Path('database.db')


def initiate_database(db_path: Path = DATABASE_PATH) -> None:
    """
    Create db if it doesn't exist, check it is correct if it does.

    Recreate db if db invalid, after copying bad db for later analysis.
    """
    if not db_path.exists():
        create_db()
    else:
        try:
            check_db(db_path)
            print('db checked out')
            return
        except sqlite3.OperationalError as error:
            db_path.rename(f"broken_database_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.db")
            print('sqlite error:', error)
        except AssertionError:
            db_path.rename(f"invalid_schema_database_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.db")
            print('bad schema')
        create_db()


def get_db_connection(db_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    # Ensure foreign key constraint enforcement.
    connection.cursor().execute("""PRAGMA foreign_keys=ON;""")
    return connection


def create_db(db_path: Path = DATABASE_PATH) -> None:
    # create tables
    # questions

    with get_db_connection(db_path) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS question_category(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            );
            """)

    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS question(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            argument_1 INTEGER NOT NULL,
            argument_2 INTEGER NOT NULL,
            answer INTEGER NOT NULL,
            question_category INTEGER,
            FOREIGN KEY (question_category) REFERENCES question_category(id)
            );
            """)

    # Populate tables

    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("""INSERT INTO question_category(name) VALUES('addition');""")
        addition_cat_id = cursor.lastrowid
        addition_data = [(x, y, x + y, addition_cat_id) for x in range(11) for y in range(11)]
        cursor.executemany(
            """INSERT INTO question(argument_1, argument_2, answer, question_category) VALUES(?,?,?,?);""",
            addition_data)

    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("""INSERT INTO question_category(name) VALUES('subtraction');""")
        subtraction_cat_id = cursor.lastrowid
        subtraction_data = [(x, y, x - y, subtraction_cat_id) for x in range(21) for y in range(21) if x - y >= 0]
        cursor.executemany(
            """INSERT INTO question(argument_1, argument_2, answer, question_category) VALUES(?,?,?,?);""",
            subtraction_data)

    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("""INSERT INTO question_category(name) VALUES('multiplication');""")
        multiplication_cat_id = cursor.lastrowid
        multiplication_data = [(x, y, x * y, multiplication_cat_id) for x in range(13) for y in range(13)]
        cursor.executemany(
            """INSERT INTO question(argument_1, argument_2, answer, question_category) VALUES(?,?,?,?);""",
            multiplication_data)


def check_db(db_path: Path = DATABASE_PATH) -> bool:
    """
    Check db has correct schema.

    returns True if db checks out.
    Does not catch errors, caller to handle:
        AssertionError if db schema does not match
        sqlite3.OperationalError if there is a db error.
    """
    with get_db_connection(db_path) as connection:
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM question_category""")
        assert ['id', 'name'] == [description[0] for description in cursor.description]

        cursor.execute("""SELECT * FROM question""")
        assert ['id', 'argument_1', 'argument_2', 'answer', 'question_category'] == [description[0] for description in
                                                                                     cursor.description]
    return True
