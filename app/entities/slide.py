from sqlalchemy import (
    JSON,
    Column,
    BigInteger,
    ForeignKey,
    Integer,
    DateTime,
    Text,
    text,
)
from sqlalchemy.orm import relationship

from app.adapters.db.base_model import BaseDbModel
from app.entities.slide_template import SlideTemplateEntity


class SlideEntity(BaseDbModel):
    __tablename__ = "slides"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    template_id = Column(Integer, ForeignKey("slide_templates.id"), nullable=False)
    presentation_id = Column(Integer, ForeignKey("presentations.id"), nullable=False)
    position = Column(Integer, nullable=False, default=1)
    data = Column(JSON, nullable=False)
    prompt = Column(Text)
    version = Column(Integer, nullable=False, default=1)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    template = relationship(SlideTemplateEntity, lazy="selectin")
