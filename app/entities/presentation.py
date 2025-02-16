from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    Integer,
    String,
    DateTime,
    text,
    Text,
)
from sqlalchemy.orm import relationship

from app.adapters.db.base_model import BaseDbModel
from app.entities.slide import SlideEntity


class PresentationEntity(BaseDbModel):
    __tablename__ = "presentations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(Text)
    prompt = Column(Text)
    version = Column(Integer, nullable=False, default=1)
    publication_code = Column(String(20), unique=True)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    slides = relationship(SlideEntity, lazy="selectin")
