import os
from typing_extensions import Annotated

from sqlalchemy.schema import FetchedValue
from datetime import datetime
from sqlalchemy import func
from dotenv import load_dotenv
from sqlalchemy import String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(os.getenv("DB_URL"), echo=True)

Session = sessionmaker(bind=engine)

timestamp = Annotated[
    datetime,
    mapped_column(
        nullable=False, server_default=func.CURRENT_TIMESTAMP()
    ),  # todo confirmar on update
]


class Base(DeclarativeBase):  # todo Base = declarative_base()
    pass


class General(Base):
    __tablename__ = "general"

    id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("action.id"))
    # action: Mapped[
    #     "Action"
    # ] = (
    #     relationship()
    # )  # back_populates="Action", cascade="all, delete-orphan")  # todo not sure if should use
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    subcategory_id: Mapped[int] = mapped_column(
        ForeignKey("subcategory.id"), nullable=True
    )
    value: Mapped[float] = mapped_column(Float)
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp]

    def __repr__(self):
        return f"General(action_id={self.action.name}, value={self.value}"


class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))  # todo mudar de action para name
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp]

    def __repr__(self) -> str:
        return f"Action(id={self.id}, action={self.name})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))  # todo change in the code from 'user'
    chat_id: Mapped[str] = mapped_column(
        String(30)
    )  # todo change in the code from 'chat'
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp]


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(30)
    )  # todo changed in the code from 'category'
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp]


class Subcategory(Base):
    __tablename__ = "subcategory"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    name: Mapped[str] = mapped_column(
        String(30)
    )  # todo change in the code from 'subcategory'
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp]
