FROM python:3.10

COPY pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root
WORKDIR /app
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
