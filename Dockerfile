FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.in-project true

RUN poetry install --no-root --no-interaction

RUN poetry run pip install -e .

ENTRYPOINT ["poetry", "run"]
