from __future__ import annotations

# atguigu/models/dialogue_state.py

from atguigu.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TEXT, String


class DialogueStateRecord(Base):
    __tablename__ = "dialogue_states"
    sender_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    state_json: Mapped[str] = mapped_column(TEXT, nullable=False, default="{}")  # 数据库长文本类型
