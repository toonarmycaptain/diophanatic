from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import (get_db_connection,
                      initiate_database,
                      Question,
                      )

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Initialise database
DATABASE_PATH = Path('database.db')  # get from env var set by helm later?
category: dict


@app.on_event("startup")
async def initialise_database(database_path: Path = DATABASE_PATH):
    initiate_database()


@app.get("/")
async def root(request: Request):
    return {"message": 'diophanatic question db API'}


@app.get('/question/addition', response_model=Question)
async def addition_ten(request: Request):
    from question import category
    question_cat_id = category['addition']
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_id, argument_1, argument_2, answer, cat = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ? AND answer <= 10
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat_id,)).fetchone()

    return {'question_id': question_id,
            'argument_1': argument_1,
            'argument_2': argument_2,
            'answer': answer,
            'category': question_cat_id,
            }


@app.get('/question/subtraction', response_model=Question)
async def subtraction_ten(request: Request):  # put application's code here
    from question import category
    question_cat_id = category['subtraction']
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_id, argument_1, argument_2, answer, cat = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ? AND argument_1 + argument_2 <= 10
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat_id,)).fetchone()

    return {'question_id': question_id,
            'argument_1': argument_1,
            'argument_2': argument_2,
            'answer': answer,
            'category': question_cat_id,
            }


@app.get('/question/addition_to_twenty', response_model=Question)
async def addition_twenty(request: Request):  # put application's code here
    from question import category
    question_cat_id = category['addition']
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_id, argument_1, argument_2, answer, cat = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ? AND answer <= 20
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat_id,)).fetchone()

    return {'question_id': question_id,
            'argument_1': argument_1,
            'argument_2': argument_2,
            'answer': answer,
            'category': question_cat_id,
            }


@app.get('/question/subtraction_to_twenty', response_model=Question)
async def subtraction_twenty(request: Request):  # put application's code here
    from question import category
    question_cat_id = category['subtraction']
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_id, argument_1, argument_2, answer, cat = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ? AND argument_1 - argument_2 <= 20
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat_id,)).fetchone()

    return {'question_id': question_id,
            'argument_1': argument_1,
            'argument_2': argument_2,
            'answer': answer,
            'category': question_cat_id,
            }


@app.get('/question/multiplication', response_model=Question)
def multiplication(request: Request):  # put application's code here
    from question import category
    question_cat_id = category['multiplication']
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_id, argument_1, argument_2, answer, cat = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ?
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat_id,)).fetchone()

    return {'question_id': question_id,
            'argument_1': argument_1,
            'argument_2': argument_2,
            'answer': answer,
            'category': question_cat_id,
            }
