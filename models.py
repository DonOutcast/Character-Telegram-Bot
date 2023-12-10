from sqlalchemy import Column, Integer,BigInteger, String, DateTime, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    time = Column(DateTime(timezone=True), server_default=func.now())


class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    message = Column(String)


class UserRequest(Base):
    __tablename__ = "user_request"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            ondelete="CASCADE"
        ),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    request = Column(String)
    response = Column(String, nullable=True)


