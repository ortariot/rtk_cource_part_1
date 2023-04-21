from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Date, LargeBinary, Boolean, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()


class Users(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    create_date = Column(Date, nullable=False)
    update_date = Column(Date, default=datetime.now())


class Tabs(Base):
    __tablename__ = "tab"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    name = Column(String)
    balance = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    create_date = Column(Date, nullable=False)
    update_date = Column(Date, default=datetime.now())


class Plans(Base):
    __tablename__ = 'plan'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'))
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    create_date = Column(Date, nullable=False)
    update_date = Column(Date, default=datetime.now())


class Services(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    create_date = Column(Date, nullable=False)
    update_date = Column(Date, default=datetime.now())


class Accommodation(Base):
    __tablename__ = 'accommodation'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'))
    status = Column(Boolean, default=True)
    addres = Column(String, nullable=False)
    tab_id = Column(Integer, ForeignKey('tab.id'), nullable=True)
    plan_id = Column(Integer, ForeignKey("plan.id"), nullable=True)
    create_date = Column(Date, nullable=False)
    update_date = Column(Date, default=datetime.now())


if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
