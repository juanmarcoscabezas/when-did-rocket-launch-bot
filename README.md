# When did the rocket launch?


This is a Telegram bot, where we have a video of a rocket launch and we want to know at which frame exactly is the rocket launched using the binary search algorithm.

Let's play [Rocket launch bot](https://t.me/when_rocket_launch_bot)!

Or use the QR

<p align="center">
    <img src="./documentation/bot_qr.jpg"  width="207" height="270">
</p>

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

# Git pre-commit hooks

- [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
- [autopep8](https://github.com/pre-commit/mirrors-autopep8)
- [Flake8](https://github.com/pycqa/flake8)
- [mypy](https://github.com/pre-commit/mirrors-mypy)

# Architecture

The Rocket Launch Bot is built using Flask and Telebot. The Flask application renders HTML templates, handles user requests and telebot webhook, while Telebot handles incoming messages from users and sends the responses.

The code is organized into separate modules based on functionality, including:
```
app.py: The main Flask application module.

bot: A module that defines the bot message handlers.

db: A module that contains the database connection.

logs: A moduile that contains the decorators for methods logging

tests: A module that contains the tests

utils: A module that contains utility functions used throughout the code.
```

# Future Development
Potential future developments for the Rocket Launch Bot include:

- Increase test coverage
- Adding a feature to display statistics on how many users answered "yes" or "no" to each image.
- Adding type hints, this will help to increase the code quality
- Adding nginx and gunicorn Dockerfiles for production enviroment


# Considerations for writing maintainable code

- Organizing the code into modules: The code is separated into smaller, logical modules, because it makes easier to navigate and make changes without affecting other parts of the code.

- Adding documentation: This README file provides documentation that explains how to install and use the code, this helps to get up and running the project quickly.

- Using version control: We can track the code changes during the time.

- Writing tests: The project has tests that helps to ensure that the code works as expected and makes it easier to catch bugs early.

- Using best practices: The code follows best practices, such as naming conventions, code formatting standards, and design patterns. For example this project uses Singleton Pattern for database connection.


Made with ❤️ by Juan Marcos. If you would like to contribute, please contact:
- [Github](https://github.com/juanmarcoscabezas)
- [Linkedin](https://www.linkedin.com/in/juanmarcoscabezas/)
