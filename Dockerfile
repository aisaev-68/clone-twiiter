FROM python:3.10

RUN apt-get update
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG INSTALL_ARGS="--no-root --no-dev"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install $INSTALL_ARGS

COPY app app
COPY migrations migrations
COPY .env alembic.ini initial_data.py ./
ENV PYTHONPATH=/code

# create a non-root user and switch to it, for security.
#RUN addgroup --system --gid 1001 "app-user"
#RUN adduser --system --uid 1001 "app-user"
#USER "app-user"
#ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
