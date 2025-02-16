# Документация проекта "Евстигней"

**Евстигней** – проект, созданный в рамках хакатона для автоматической генерации презентаций на основе пользовательских запросов.

### **Цель проекта**

Разработать web-приложение, которое позволит пользователям быстро создавать презентации с помощью **нейросети**.

### **Основные задачи**

- Реализация **frontend** и **backend** для взаимодействия с пользователем.
- Интеграция **ИИ-модели** для генерации слайдов.
- Оптимизация процесса генерации и редактирования презентаций.
- Подготовка к демонстрации проекта на хакатоне.

Проект ориентирован на скорость разработки и качество демонстрации, что критично для успешного выступления на хакатоне.

## Содержание

1. [Введение](docs/intro/index.md)

- [Описание проекта](docs/intro/intro.md)
- [Цель и задачи](docs/intro/goal.md)

2. [Архитектура](docs/system/index.md)

- [Общее описание системы](docs/system/overview.md)
- [Backend (FastAPI)](docs/system/backend.md)
- [Frontend (Vue)](docs/system/frontend.md)
- [Взаимодействие с нейросетью](docs/system/ai_integration.md)
- [Версионирование данных](docs/system/versioning/index.md)
  - [Механизм версионирования](docs/system/versioning/versioning_mechanism.md)
  - [История изменений](docs/system/versioning/changelog.md)

3. [Модели данных](docs/models/index.md)

- [Пользователь](docs/models/user.md)
- [Презентация](docs/models/presentation.md)
- [Шаблон слайда](docs/models/slide_template.md)
- [Слайд](docs/models/slide.md)

4. [Пользовательские сценарии](docs/use_cases/index.md)

- [Создание презентации](docs/use_cases/create_presentation.md)
- [Редактирование презентации](docs/use_cases/edit_presentation.md)
- [Выбор шаблона](docs/use_cases/select_template.md)
- [Генерация слайдов](docs/use_cases/generate_slides.md)
- [Публикация презентации](docs/use_cases/publish_presentation.md)
- [Просмотр опубликованной презентации](docs/use_cases/view_presentation.md)

5. [API](docs/api/index.md)

- [Аутентификация](docs/api/authentication.md)

6. [WebSocket](docs/websocket/index.md)

- [Описание WebSocket](docs/websocket/description.md)

7. [Разработка и стандарты](docs/standards/index.md)

- [Чистая архитектура](docs/standards/clean_architecture.md)
- [Workflow разработки](docs/standards/workflow.md)
- [Git Flow](docs/standards/git_flow.md)
- [Кодстайл](docs/standards/codestyle.md)
