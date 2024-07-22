FROM python:3.12

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# Install poetry:
RUN pip install "poetry==$POETRY_VERSION"

# Python requirements install via poetry
WORKDIR /backend
COPY /backend/poetry.lock /backend/poetry.lock
COPY /backend/pyproject.toml /backend/pyproject.toml
RUN poetry install

COPY /backend/app /backend/app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0"]
