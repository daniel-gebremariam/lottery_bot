from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String)
    phone = Column(String)


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    ticket_number = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_confirmed = Column(Boolean, default=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    screenshot_file_id = Column(String)
    status = Column(String, default="pending")
