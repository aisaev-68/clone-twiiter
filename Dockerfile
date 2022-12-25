FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-root
COPY . .
WORKDIR /app/app
#EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
