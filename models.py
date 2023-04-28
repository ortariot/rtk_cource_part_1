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
    id = Column(BigInteger, primary_key=True)
    create_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow)
    update_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Users(Base, BaseModelMixin):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)

    def __repr__(self):
        return (
            f'id: {self.id} name: {self.name} login: {self.login} '
            f'phone: {self.phone}, e-mail: {self.mail}'
        )


class Tabs(Base, BaseModelMixin):
    __tablename__ = "tabs"

    number = Column(Integer, nullable=False)
    name = Column(String)
    balance = Column(Integer, default=0)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    users = relationship('Users')

    def __repr__(self):
        return (
            f'id: {self.id} name: {self.name} number: {self.number} '
            f'balance: {self.balance} user_id: {self.user_id}'
        )


class Services(Base, BaseModelMixin):
    __tablename__ = 'services'

    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f'id: {self.id} name: {self.name}'


class Plans(Base, BaseModelMixin):
    __tablename__ = 'plans'

    service_id = Column(ForeignKey('services.id'), nullable=False)
    service = relationship('Services')
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f'id: {self.id} name: {self.name} description: {self.desc} '
            f'price: {self.price} service_id: {self.service_id}'
        )


class Accommodations(Base, BaseModelMixin):
    __tablename__ = 'accommodations'

    service_id = Column(ForeignKey('services.id'), nullable=False)
    service = relationship('Services')

    status = Column(Boolean, default=True)
    addres = Column(String, nullable=False)

    tab_id = Column(ForeignKey('tabs.id'), nullable=False, unique=True)
    tab = relationship('Tabs')
    plan_id = Column(ForeignKey('plans.id'), nullable=False)
    plan = relationship('Plans')

    def __repr__(self):
        return (
            f'id: {self.id} addres: {self.addres} status: {self.status} '
            f'tab_id: {self.tab_id} service_id: {self.service_id} '
            f'plan_id {self.plan_id}'
        )


if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
