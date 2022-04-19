from random import randint

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

from prometheus_fastapi_instrumentator import Instrumentator  #type: ignore
Instrumentator().instrument(app).expose(app)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


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
    a = randint(0, 10)
    b = randint(0, 10)
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
    a = randint(0, 10)
    b = randint(0, 10)
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
    a = randint(0, 20)
    while (a + (b := randint(0, 20))) >= 20:
        pass

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
    a = randint(0, 20)
    while (b := randint(0, 20)) >= a:
        pass

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
    a = randint(0, 12)
    b = randint(0, 12)
    return templates.TemplateResponse('two_integers.html', {"request": request, "a": a,
                                                            "b": b,
                                                            "operator": multiplication_sign,
                                                            "append": equals_sign
                                                            })
