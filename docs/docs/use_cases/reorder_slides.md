# Пользовательский сценарий: Смена порядка слайдов

## Описание
Данный сценарий описывает процесс изменения порядка слайдов в презентации. Пользователь передает идентификатор слайда и его новую позицию, система пересчитывает порядок всех слайдов в презентации и возвращает обновленную презентацию.

## Акторы
- **Пользователь** – инициирует изменение порядка слайдов.
- **Система** – обрабатывает изменение позиции слайда и обновляет порядок всех слайдов презентации.

## Предусловия
- Пользователь может изменять только презентации, которые принадлежат ему.
- Пользователь авторизован в системе.
- В системе существует презентация с слайдами.

## Основной поток
1. Пользователь передает **id** слайда и его новую **позицию**.
2. Система находит презентацию, к которой принадлежит данный слайд.
3. Система получает список всех слайдов данной презентации, отсортированных по текущей позиции.
4. Система обновляет позицию указанного слайда.
5. Система пересчитывает позиции остальных слайдов, чтобы сохранить непрерывную последовательность.
6. Система сохраняет обновленный порядок слайдов в базе данных.
7. Пользователь получает обновленный список слайдов в новой последовательности.

## Альтернативные потоки
- **Ошибка валидации**: если переданная позиция некорректна (отрицательное число, превышает количество слайдов и т. д.), система возвращает ошибку и предлагает корректные значения.
- **Слайд не найден**: если переданный **id** слайда не существует, система возвращает ошибку.
- **Конфликт изменений**: если слайды были изменены другим пользователем в процессе обновления, система уведомляет пользователя и предлагает повторить операцию.

## Постусловия
- Порядок слайдов в презентации обновлен и сохранен в системе.
- Пользователь видит актуальный порядок слайдов.

## Связанные файлы
- [Модель "Слайд"](../models/slide.md)
- [Модель "Презентация"](../models/presentation.md)
- [Редактирование презентации](edit_presentation.md)

