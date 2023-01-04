from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

class User:
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(25), unique=True, nullable=False)
    api_token: str = Column(Text(), nullable=False)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())



async def add_new_user(user: Dict):
    u = User(*user)