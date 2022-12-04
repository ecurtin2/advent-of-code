FROM python:3.11.0-alpine3.17
RUN apk add git bash just
RUN pip install poetry
RUN mkdir /advent-of-code
WORKDIR /advent-of-code
ADD poetry.lock pyproject.toml /advent-of-code/
RUN poetry config virtualenvs.create false && poetry install
ADD . /advent-of-code/

ENTRYPOINT [ "sleep", "infinity" ]
