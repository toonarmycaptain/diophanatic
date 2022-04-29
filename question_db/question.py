from database import get_db_connection

categories = ['addition', 'subtraction', 'multiplication']


def get_question_category_id(category_string: str) -> int:
    """Get question category to prime category dict."""
    with get_db_connection() as connection:
        cursor = connection.cursor()
        category_int, = cursor.execute(
            """
            SELECT id FROM question_category
            WHERE name = ?;
            """, (category_string,)).fetchone()
    return category_int


# This only runs once, on first request, as seen by app log output.
category = {category: get_question_category_id(category) for category in categories}
print(f'Question categories: {category}')
