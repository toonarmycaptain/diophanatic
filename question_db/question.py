from pydantic import BaseModel

from database import get_db_connection


class Question(BaseModel):
    question_id: int
    argument_1: int
    argument_2: int
    answer: int
    category: int | None = None  # use question_id or string?


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


category = {category: get_question_category_id(category) for category in categories}
print(f'Question categories: {category}')
