from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DynamicBase = declarative_base()


class User(DynamicBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    organization_id = Column(Integer, nullable=True)
