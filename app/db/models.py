from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Первичный ключ
    username = Column(String, unique=True, index=True)  # Юзернейм
    password = Column(String)  # Hashed password


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # Первичный ключ
    title = Column(String, index=True)  # Заголовок задачи
    description = Column(Text, nullable=True)  # Описание задачи
    is_completed = Column(Boolean, default=False)  # Статус задачи
    created_at = Column(DateTime, server_default=func.now())  # Время создания
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Пользователь внешний ключ
