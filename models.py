from datetime import datetime

from sqlalchemy import Column, Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, Date, LargeBinary, Boolean
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import bcrypt

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


tabs_services = Table('tabs_services',
                      Base.metadata,
                      Column('tab_id', Integer(), ForeignKey('tab.id')),
                      Column('service_id', Integer(), ForeignKey('service.id'))
                      )

class Plans(Base):
    __tablename__ = 'plan'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    create_date = Column(Date, nullable=False)
    update_date = Column(Date, default=datetime.now())


class Services(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(Boolean, default=True)
    addres = Column(String, nullable=False)
    tab_id = relationship('Tabs',
                          secondary=tabs_services,
                          backref='service'
                          )
    plan_id = Column(Integer, ForeignKey("plan.id"), nullable=False)
    create_date = Column(Date, nullable=False)
    update_date = Column(Date, default=datetime.now())



def crate_user(engine, name, phone, mail, login, password):
    with Session(engine) as session:
        user_one = Users(name=name,
                         phone=phone,
                         mail=mail,
                         login=login,
                         password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                         create_date = datetime.now(),
                        )
        session.add(user_one)
        session.commit()



if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    crate_user(engine,
               name='Igor Kozlov',
               phone='+7999-324-56-17',
               mail='igorok@mail.ru',
               login='igor',
               password='12345'
               )
    # password = 'aaa'
    # hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # print(hashAndSalt)

    # with Session(engine) as session:
    #     user_one = Users(name = 'Igor Kozlov',
    #                     phone = '+788-433-28-24',
    #                     mail = 'kozlov@mail.ru',
    #                     login = 'igoek',
    #                     password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
    #                     create_date = datetime.now(),
    #                     update_date = datetime.now()
    #                     )
    #     session.add(user_one)
    #     session.commit()