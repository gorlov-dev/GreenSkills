FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Устанавливаем переменные окружения для Poetry
ENV POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Устанавливаем зависимости системы (при необходимости)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы для Poetry
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем Python-зависимости (без создания виртуального окружения)
RUN poetry install --no-root

# Копируем весь проект в контейнер
COPY . /app

# Открываем порт для uvicorn (не обязательно, но для наглядности)
EXPOSE 8000

# Команда запуска FastAPI-сервера
CMD ["uvicorn", "app.web_api.server:app", "--host", "0.0.0.0", "--port", "8000"]
