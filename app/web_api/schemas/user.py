from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    login: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

