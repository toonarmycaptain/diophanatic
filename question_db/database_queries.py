"""Utility db query functions"""
from database import get_db_connection


def get_operator(question_category: int) -> str:
    """Return str operator for given question category."""
    with get_db_connection() as connection:
        cursor = connection.cursor()
        operator, = cursor.execute(
            """
            SELECT text_operator FROM question_category
            WHERE id == ? 
            LIMIT 1;
            """, (question_category,)).fetchone()

    return operator
