FROM python:3.13-slim

# Required for poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_ANSI=1

# Set terminal colors
ENV RICH_FORCE_TERMINAL=1

# Base directory
WORKDIR /app

# Copy over project files
COPY pyproject.toml poetry.lock README.md ./
COPY vault_slicer ./vault_slicer

# Install Poetry
RUN pip install poetry
RUN poetry install --only main --quiet

# Create mount directories
RUN mkdir -p /vault /export
VOLUME ["/vault", "/export"]

# Set entrypoint
ENTRYPOINT ["vault-slicer"]