import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from app.adapters.db.session import async_session_maker
from app.entities.slide_template import SlideTemplateEntity
from sqlalchemy.future import select


async def seed_templates():
    async with async_session_maker() as session:
        templates = [
            SlideTemplateEntity(
                title="Список",
                slug="list",
                data={"list": []},
                data_structure="Список - несколько элементов текста",
            ),
            SlideTemplateEntity(
                title="Заголовок",
                slug="title_only",
                data={"title": None},
                data_structure="Заголовок",
            ),
            SlideTemplateEntity(
                title="Список с заголовком",
                slug="product_pitch",
                data={"title": None, "list": []},
                data_structure="Заголовок, список - несколько элементов текста",
            ),
            SlideTemplateEntity(
                title="Текстовый блок",
                slug="text_block",
                data={"text": None},
                data_structure="Текстовй блок",
            ),
            SlideTemplateEntity(
                title="Колонки",
                slug="columns",
                data={"columns": []},
                data_structure="Текст раббитый на 2 колонки",
            ),
        ]

        # Проверяем, существуют ли уже эти шаблоны
        stmt = select(SlideTemplateEntity).where(
            SlideTemplateEntity.slug.in_([t.slug for t in templates])
        )
        result = await session.execute(stmt)
        existing_slugs = {t.slug for t in result.scalars().all()}

        # Фильтруем, оставляя только новые записи
        new_templates = [t for t in templates if t.slug not in existing_slugs]

        if new_templates:
            session.add_all(new_templates)
            await session.commit()
            print(f"Добавлены новые шаблоны: {[t.slug for t in new_templates]}")
        else:
            print("Все шаблоны уже существуют. Ничего не изменено.")


if __name__ == "__main__":
    asyncio.run(seed_templates())
