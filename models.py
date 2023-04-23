from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Boolean, String, DateTime, BigInteger, create_engine
from sqlalchemy.orm import declarative_base, declarative_mixin, relationship

from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()


@declarative_mixin
class BaseModelMixin:
    id = Column(BigInteger, primary_key=True)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_date = Column(DateTime, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)


class Users(Base, BaseModelMixin):
    __tablename__ = "user"

    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)


class Tabs(Base, BaseModelMixin):
    __tablename__ = "tab"

    number = Column(Integer, nullable=False)
    name = Column(String)
    balance = Column(Integer, default=0)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    user = relationship('Users')


class Plans(Base, BaseModelMixin):
    __tablename__ = 'plan'

    service_id = Column(ForeignKey('service.id'), nullable=False)
    service = relationship('Services')
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    price = Column(Integer, nullable=False)


class Services(Base, BaseModelMixin):
    __tablename__ = 'service'

    name = Column(String, nullable=False)


class Accommodation(Base, BaseModelMixin):
    __tablename__ = 'accommodation'

    service_id = Column(ForeignKey('service.id'), nullable=False)
    service = relationship('Services')
    status = Column(Boolean, default=True)
    addres = Column(String, nullable=False)
    tab_id = Column(ForeignKey('tab.id'), nullable=False, unique=True)
    tab = relationship('Tabs')
    plan_id = Column(ForeignKey('plan.id'), nullable=False)
    plan = relationship('Plans')


if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
