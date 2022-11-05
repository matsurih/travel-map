FROM python:3.10.8

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install


COPY . .
EXPOSE 7551


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7551"]
