FROM python:3.11-slim
RUN apt update && apt install git curl -y
RUN mkdir -p ~/bin
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /bin
ENV PATH=~/bin:$PATH

RUN pip install poetry
RUN mkdir /advent-of-code
WORKDIR /advent-of-code
ADD poetry.lock pyproject.toml /advent-of-code/
RUN poetry config virtualenvs.create false && poetry install
ADD . /advent-of-code/

ENTRYPOINT [ "sleep", "infinity" ]
