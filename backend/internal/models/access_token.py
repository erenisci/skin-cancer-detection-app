from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccessToken(BaseModel):
    token: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    is_active: bool = True
