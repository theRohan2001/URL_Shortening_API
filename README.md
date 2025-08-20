# URL Shortening Service

A FastAPI URL Shortener API that helps shorten long URLs.

## Requirements
#Python
#FastAPI
#SQLAlchemy
#UV
#Alembic

## Clone Repository & Setup venv

Clone the repository with:

```bash
"git clone https://github.com//url_shortener.git"
```
### Install uv

```bash
pip install uv
```
## Create Virtual Environment
```cd``` into the url_shortener directory then create and activate a virtual environment:
```uv venv .venv```

## Intialize the project through uv

```bash
uv init
```

## Install all packages with the following:

```bash
uv pip install -r requirements.txt
```

## Alembic Migration

Initialize alembic with ```alembic init alembic```.
Update line 63 ```sqlalchemy.url = driver://user:pass@localhost/dbname``` in alembic.ini to use the sqlite driver:

``sqlite:///url_shortener.db``

In the env file in the newly created alembic directory, add the following code with the rest of the imports```from models.base import Base```.
Update line 23 to use the correct metadate: ```target_metadata = Base.metadata```

Then generate a new migration script and upgrade the head with the following:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

You should a new url_shortener.db file in the root directory.

## Start Server

Run server with: ```uv run fastapi dev app.py```

Root: <http://127.0.0.1:8000>
Documentation: <http://127.0.0.1:8000/docs> or <http://127.0.0.1:8000/redoc>
