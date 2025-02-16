import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from app.adapters.db.session import async_session_maker
from app.entities.slide_template import SlideTemplateEntity
from sqlalchemy.future import select
from app.prompts.generate_slides import scenario_generate_presentation_slides


async def seed_templates():
    async with async_session_maker() as session:
        scenario_generate_presentation_slides("как корабли дороздят что-то")


if __name__ == "__main__":
    asyncio.run(seed_templates())
