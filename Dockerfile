FROM python:3.12.1-slim-bullseye

WORKDIR /usr/src/tge-scraper

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    nano \
    curl \
    && rm -rf /var/lib/apt/lists/* 

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && echo "export PATH=\"$HOME/.local/bin:$PATH\"" >> $HOME/.bashrc
ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . .

EXPOSE 8000

ENTRYPOINT ["python", "./run.py"]

CMD ["--remote"]
