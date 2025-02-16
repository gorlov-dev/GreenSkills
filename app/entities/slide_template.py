from sqlalchemy import Column, BigInteger, Text, JSON, String, DateTime, text

from app.adapters.db.base_model import BaseDbModel


class SlideTemplateEntity(BaseDbModel):
    __tablename__ = "slide_templates"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    title = Column(Text, nullable=False)
    slug = Column(String(20), unique=True, nullable=False)
    data_structure = Column(Text)
    data = Column(JSON, nullable=False)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
