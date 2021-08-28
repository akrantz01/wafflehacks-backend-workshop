FROM python:3.8-slim as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1


## Get the requirements from poetry
## Feel free to ignore this as it is only useful if you want to use poetry
FROM base as export-dependencies

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy dependencies
COPY poetry.lock pyproject.toml ./

# Export to requirements.txt format
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes


## This will actually run the app
FROM base

# Import all the project files
ENV APP_HOME /app
WORKDIR ${APP_HOME}
COPY ./better_todos ./better_todos

# Install dependencies
COPY --from=export-dependencies /requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the server
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 better_todos:app
