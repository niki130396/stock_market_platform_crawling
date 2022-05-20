FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev


COPY ./requirements/pytest_requirements.txt /requirements/pytest_requirements.txt
RUN pip install -r /requirements/pytest_requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

ENTRYPOINT ["pytest", "tests/test_spiders.py", "-s"]
