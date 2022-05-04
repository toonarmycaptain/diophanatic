from pathlib import Path
from random import randint

import httpx

from fastapi import (Cookie,
                     FastAPI,
                     Form,
                     Request,
                     )
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get('/two_ints/', response_class=HTMLResponse)
async def two_ints(request: Request):  # put application's code here

    a = randint(0, 10)
    b = randint(0, 10)
    return templates.TemplateResponse("two_integers.html", {"request": request,
                                                            "a": a, "b": b,
                                                            "next_text": "Next pair",
                                                            })


@app.get('/three_digits', response_class=HTMLResponse)
def three_digits(request: Request):
    a = randint(0, 1000)
    return templates.TemplateResponse('single_integer.html', {"request": request,
                                                              "a": a,
                                                              "next_text": "Next integer",
                                                              })


@app.get('/ten', response_class=HTMLResponse)
def ten(request: Request):  # put application's code here
    a = randint(0, 10)
    return templates.TemplateResponse('single_integer.html', {"request": request,
                                                              "a": a,
                                                              "next_text": "Next integer",
                                                              })


@app.get('/addition', response_class=HTMLResponse)
async def addition_ten(request: Request,
                       previous_question_answer: str | None = Cookie(None),
                       previous_question_grade: bool | None = Cookie(None),
                       ):
    addition_sign = '+'
    equals_sign = '='
    question = httpx.get("http://diophanatic-question-database-service:1742/question/addition").json()

    response = templates.TemplateResponse("two_integers.html",
                                          {"request": request,
                                           "title": "addition",
                                           "a": question['argument_1'], "b": question['argument_2'],
                                           "question": question,
                                           "operator": addition_sign,
                                           "append": equals_sign,
                                           "next_text": "Next question",
                                           "previous_question_answer": previous_question_answer,
                                           "previous_question_grade": previous_question_grade
                                           })
    response.set_cookie(key="question_id", value=question['question_id'])
    # Delete obsolete cookie values:
    response.delete_cookie(key="previous_question_answer")
    response.delete_cookie(key="previous_question_grade")

    return response


@app.post('/addition', response_class=HTMLResponse)
async def ten(request: Request, answer: str = Form(...)):
    # Ascertain correct/incorrect, then post to db:
    question = httpx.get(f"http://localhost:1742/question/id/{request.cookies['question_id']}").json()
    answer = int(answer)
    question_answer = f"{question['argument_1']} + {question['argument_2']} = {answer}"
    question_grade = question['argument_1'] + question['argument_2'] == answer
    # Set cookie values to pass to GET
    response = RedirectResponse(url='/addition', status_code=303)
    response.set_cookie(key="previous_question_answer", value=question_answer)
    response.set_cookie(key="previous_question_grade", value=question_grade)
    return response


@app.get('/subtraction', response_class=HTMLResponse)
async def subtraction_ten(request: Request):  # put application's code here
    subtraction_sign = '-'
    equals_sign = '='
    question = httpx.get("http://diophanatic-question-database-service:1742/question/subtraction").json()

    return templates.TemplateResponse("two_integers.html",
                                      {"request": request,
                                       "title": "subtraction",
                                       "a": question['argument_1'], "b": question['argument_2'],
                                       "operator": subtraction_sign,
                                       "append": equals_sign,
                                       "next_text": "Next question",
                                       })


@app.get('/addition_to_twenty', response_class=HTMLResponse)
async def addition_twenty(request: Request):  # put application's code here
    addition_sign = '+'
    equals_sign = '='
    question = httpx.get("http://diophanatic-question-database-service:1742/question/addition_to_twenty").json()

    return templates.TemplateResponse("two_integers.html",
                                      {"request": request,
                                       "title": "addition",
                                       "a": question['argument_1'], "b": question['argument_2'],
                                       "operator": addition_sign,
                                       "append": equals_sign,
                                       "next_text": "Next question",
                                       })


@app.get('/subtraction_to_twenty', response_class=HTMLResponse)
async def subtraction_twenty(request: Request):  # put application's code here
    subtraction_sign = '-'
    equals_sign = '='
    question = httpx.get("http://diophanatic-question-database-service:1742/question/subtraction_to_twenty").json()

    return templates.TemplateResponse("two_integers.html",
                                      {"request": request,
                                       "title": "subtraction",
                                       "a": question['argument_1'], "b": question['argument_2'],
                                       "operator": subtraction_sign,
                                       "append": equals_sign,
                                       "next_text": "Next question",
                                       })


@app.get('/multiplication', response_class=HTMLResponse)
def multiplication(request: Request):  # put application's code here
    multiplication_sign = '×'
    equals_sign = '='
    question = httpx.get("http://diophanatic-question-database-service:1742/question/multiplication").json()

    return templates.TemplateResponse('two_integers.html', {"request": request,
                                                            "title": "multiplication",
                                                            "a": question['argument_1'], "b": question['argument_2'],
                                                            "operator": multiplication_sign,
                                                            "append": equals_sign,
                                                            "next_text": "Next question",
                                                            })
