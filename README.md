# When did the rocket launch?

This is a Telegram bot, where we have a video of a rocket launch and we want to know at which frame exactly is the rocket launched using the binary search algorithm.

## Installation

### Install with Docker

```
$ docker-compose up
```

### Install with pip and venv:

```
$ python3 -m venv .venv
$ source .venv/binary/activate
$ pip install -r requirements.txt
```

### Enviroment variables
```
BOT_TOKEN=
BOT_POLLING=False | True
NGROK_TOKEN=
SERVER_HOST=
SERVER_PORT=5000
DATABASE_HOST=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
ENV=dev | prod
FLASK_DEBUG=1 | 0
```


## Application Structure
```
.
when-did-rocket-launch-bot
├─ .gitignore
├─ .pre-commit-config.yaml
├─ README.md
├─ app
│  ├─ Dockerfile
│  ├─ app.py
│  ├─ bot
│  │  ├─ __init__.py
│  │  ├─ handlers.py
│  │  ├─ keyboard.py
│  │  └─ utils.py
│  ├─ db
│  │  ├─ __init__.py
│  │  └─ database.py
│  ├─ logs
│  │  ├─ __init__.py
│  │  └─ app_logger.py
│  ├─ requirements.txt
│  ├─ tests
│  └─ utils
│     ├─ __init__.py
│     ├─ ngrok.py
│     └─ texts.py
└─ docker-compose.yml
```

## HTTP Methods

```http
GET http://127.0.0.1:5000/
Expect: HTML response


POST http://127.0.0.1:8000/
Content-Type: application/json
Expect: 200, OK
```


# Bisection Algorithm

The bisection algorithm, also known as the binary search algorithm, is a numerical method used to find the root of a function within a given interval. The basic idea behind the bisection algorithm is to repeatedly divide the interval in half and then determine which half of the interval contains the root. This process is repeated until the desired level of accuracy is achieved.

```python
"""
Algorithm example
"""
def bisection(f, a, b, tolerance):
    """
    Find the root of the function f within the interval [a, b] with a tolerance.
    """
    while (b - a) / 2 > tolerance:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2
```

# Tests

For tests execute

```
$ cd app/
$ python3 -m unittest
```
