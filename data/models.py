from sqlalchemy import Column, Integer, BigInteger, String

from data.db_connect import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    user_name = Column(String(length=255), nullable=False)
    user_url = Column(String(length=255), nullable=True)


class Patient(BaseModel):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(length=255), nullable=False)
    user_id = Column(BigInteger, nullable=False, index=True, unique=True)
    phone = Column(String(length=255), nullable=False)


class Stock(BaseModel):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255), nullable=False)
    description = Column(String(length=255), nullable=True)
    price = Column(String(length=255), nullable=True)
    image = Column(String(length=255), nullable=True)
