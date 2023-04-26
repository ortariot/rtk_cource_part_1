from datetime import datetime

from sqlalchemy import (
    Column, ForeignKey, Integer, LargeBinary, Boolean,
    String, DateTime, BigInteger, create_engine
)
from sqlalchemy.orm import declarative_base, declarative_mixin, relationship

from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()


@declarative_mixin
class BaseModelMixin:
    id: int = Column(BigInteger, primary_key=True)
    create_date: datetime = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    update_date: datetime = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Users(Base, BaseModelMixin):
    __tablename__ = "users"

    name: str = Column(String, nullable=False)
    phone: str = Column(String, unique=True, nullable=False)
    mail: str = Column(String, unique=True, nullable=False)
    login: str = Column(String, unique=True, nullable=False)
    password: LargeBinary = Column(LargeBinary, nullable=False)


class Tabs(Base, BaseModelMixin):
    __tablename__ = "tabs"

    number: int = Column(Integer, nullable=False)
    name: str = Column(String)
    balance: int = Column(Integer, default=0)
    user_id: int = Column(ForeignKey('users.id'), nullable=False)
    user: Users = relationship('Users')


class Services(Base, BaseModelMixin):
    __tablename__ = 'services'

    name = Column(String, nullable=False, unique=True)


class Plans(Base, BaseModelMixin):
    __tablename__ = 'plans'

    service_id: int = Column(ForeignKey('services.id'), nullable=False)
    service: Services = relationship('Services')
    name: str = Column(String, nullable=False)
    desc: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)


class Accommodations(Base, BaseModelMixin):
    __tablename__ = 'accommodations'

    service_id: int = Column(ForeignKey('services.id'), nullable=False)
    service: Services = relationship('Services')
    status: bool = Column(Boolean, default=True)
    addres: str = Column(String, nullable=False)
    tab_id: int = Column(ForeignKey('tabs.id'), nullable=False, unique=True)
    tab: Tabs = relationship('Tabs')
    plan_id: int = Column(ForeignKey('plans.id'), nullable=False)
    plan: Plans = relationship('Plans')


if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
