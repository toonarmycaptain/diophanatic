from pathlib import Path
from random import randint

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import get_db_connection, initiate_database

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Initialise database
DATABASE_PATH = Path('database.db')  # get from env var set by helm later?


@app.on_event("startup")
async def initialise_database(database_path: Path = DATABASE_PATH):
    initiate_database()


@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get('/two_ints/', response_class=HTMLResponse)
async def two_ints(request: Request):  # put application's code here

    a = randint(0, 10)
    b = randint(0, 10)
    return templates.TemplateResponse("two_integers.html", {"request": request, "a": a, "b": b})


@app.get('/three_digits', response_class=HTMLResponse)
def three_digits(request: Request):
    a = randint(0, 1000)
    return templates.TemplateResponse('single_integer.html', {"request": request, "a": a})


@app.get('/ten', response_class=HTMLResponse)
def ten(request: Request):  # put application's code here
    a = randint(0, 10)
    return templates.TemplateResponse('single_integer.html', {"request": request, "a": a})


@app.get('/addition', response_class=HTMLResponse)
async def addition_ten(request: Request):  # put application's code here
    addition_sign = '+'
    equals_sign = '='
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_cat, = cursor.execute(
            """
            SELECT id FROM question_category
            WHERE name = ?;
            """, ('addition',)).fetchone()
        q_id, a, b, *unused_cols = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ? AND answer <= 10
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat,)).fetchone()

    return templates.TemplateResponse("two_integers.html",
                                      {"request": request,
                                       "a": a, "b": b,
                                       "operator": addition_sign,
                                       "append": equals_sign
                                       })


@app.get('/subtraction', response_class=HTMLResponse)
async def subtraction_ten(request: Request):  # put application's code here
    subtraction_sign = '-'
    equals_sign = '='
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_cat, = cursor.execute(
            """
            SELECT id
            FROM question_category 
            WHERE name = ?;
            """, ('subtraction',)).fetchone()
        q_id, a, b, *unused_cols = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ? AND argument_1 + argument_2 <= 10
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat,)).fetchone()

    return templates.TemplateResponse("two_integers.html",
                                      {"request": request,
                                       "a": a, "b": b,
                                       "operator": subtraction_sign,
                                       "append": equals_sign
                                       })


@app.get('/addition_to_twenty', response_class=HTMLResponse)
async def addition_twenty(request: Request):  # put application's code here
    addition_sign = '+'
    equals_sign = '='
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_cat, = cursor.execute(
            """
            SELECT id FROM question_category
            WHERE name = ?;
            """, ('subtraction',)).fetchone()
        q_id, a, b, *unused_cols = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ? AND argument_1 + argument_2 <= 20
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat,)).fetchone()

    return templates.TemplateResponse("two_integers.html",
                                      {"request": request,
                                       "a": a, "b": b,
                                       "operator": addition_sign,
                                       "append": equals_sign
                                       })


@app.get('/subtraction_to_twenty', response_class=HTMLResponse)
async def subtraction_twenty(request: Request):  # put application's code here
    subtraction_sign = '-'
    equals_sign = '='
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_cat, = cursor.execute(
            """
            SELECT id 
            FROM question_category
            WHERE name = ?;
            """, ('subtraction',)).fetchone()
        q_id, a, b, *unused_cols = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ?
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat,)).fetchone()

    return templates.TemplateResponse("two_integers.html",
                                      {"request": request,
                                       "a": a, "b": b,
                                       "operator": subtraction_sign,
                                       "append": equals_sign
                                       })


@app.get('/multiplication', response_class=HTMLResponse)
def multiplication(request: Request):  # put application's code here
    multiplication_sign = '×'
    equals_sign = '='
    with get_db_connection() as connection:
        cursor = connection.cursor()
        question_cat, = cursor.execute(
            """
            SELECT id FROM question_category
            WHERE name = ?;
            """, ('multiplication',)).fetchone()
        q_id, a, b, *unused_cols = cursor.execute(
            """
            SELECT * FROM question 
            WHERE question_category = ?
            ORDER BY RANDOM() 
            LIMIT 1;
            """, (question_cat,)).fetchone()

    return templates.TemplateResponse('two_integers.html', {"request": request, "a": a,
                                                            "b": b,
                                                            "operator": multiplication_sign,
                                                            "append": equals_sign
                                                            })
