#FROM python:3.9
#
#
#
##ENV PYTHONDONTWRITEBYTECODE 1
##ENV PYTHONUNBUFFERED 1
#
## Install poetry
#
#RUN curl -sSL https://install.python-poetry.org | python3 -
#ENV PATH="${PATH}:/root/.poetry/bin"
#
## temporary
#COPY pyproject.toml poetry.lock /
#
## Install dependecies.
#RUN bash -c poetry config virtualenvs.create false && bash - c poetry install --no-dev
#
#
#COPY . .
#
## Run
#WORKDIR ./app
#ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.10

COPY pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root
WORKDIR /app
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
