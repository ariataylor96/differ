FROM python:latest

RUN apt-get update
RUN apt-get install git

RUN pip install --upgrade poetry

RUN mkdir /code
WORKDIR /code

RUN mkdir ./differ

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root

COPY differ ./differ/

RUN poetry install

ENV PYTHON_UNBUFFERED=1

CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "differ.main:app"]
