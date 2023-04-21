from datetime import datetime
from random import randint
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import bcrypt

from config import SQLALCHEMY_DATABASE_URI
from models import Users, Plans, Tabs, Services, Accommodation


def crate_user(engine, name, phone, mail, login, password):
    """
    1.Написать функцию, которая принимает
    данные пользователя и создает его.
    """
    with Session(engine) as session:
        user = Users(name=name,
                     phone=phone,
                     mail=mail,
                     login=login,
                     password=bcrypt.hashpw(
                         password.encode(), bcrypt.gensalt()),
                     create_date=datetime.now(),
                     )
        session.add(user)
        session.commit()


def crate_plan(engine, name, desc, price, service_id):
    with Session(engine) as session:
        plan = Plans(name=name,
                     service_id=service_id,
                     desc=desc,
                     price=price,
                     create_date=datetime.now(),
                     )
        session.add(plan)
        session.commit()


def create_service(engine, name):
    with Session(engine) as session:
        service = Services(name=name,
                           create_date=datetime.now()
                           )
        session.add(service)
        session.commit()


def create_tab(engine, name, user_id):
    '''
    2.Написать функцию, которая принимает название ЛС,
    создает его и привязывает к определенному пользователю.
    Номер счета генерируется автоматически.
    '''
    with Session(engine) as session:
        tab = Tabs(number=randint(1000000, 9999999),
                   name=name,
                   user_id=user_id,
                   create_date=datetime.now()
                   )
        session.add(tab)
        session.commit()


def create_accommodation(engine, service_name, plan_name, tab_id, addres):
    """
    3.	Написать функцию, которая:
        Получает услугу из перечня по ее английскому наименованию (коду).
        Получает тариф услуги из перечня по его английскому
        наименованию (коду). Привязывает услугу с выбранным тарифом к
        определенному ЛС в статусе Активна.
    """

    with Session(engine) as session:
        service_id = session.query(Services).filter(
            Services.name == service_name).one().id
        plan_id = session.query(Plans).filter(Plans.name == plan_name,
                                              Plans.service_id == service_id
                                              ).one().id

        accommodation = Accommodation(service_id=service_id,
                                      addres=addres,
                                      tab_id=tab_id,
                                      plan_id=plan_id,
                                      create_date=datetime.now()
                                      )
        session.add(accommodation)
        session.commit()


def accept_servce(engine, service_name, plan_name, tab_name):
    pass


def update_plan(engine, tab_id, plan_id):
    '''
    4.	Написать функцию, которая позволяет изменить тариф услуги по ID ЛС.
    '''
    with Session(engine) as session:
        accommodation = session.query(Accommodation).filter(
            Accommodation.tab_id == tab_id).one()
        sevice_id = accommodation.service_id

        plan = session.query(Plans.id).filter(Plans.service_id == sevice_id,
                                              Plans.id == plan_id
                                              ).all()
        if plan:
            accommodation.plan_id = plan_id
            session.add(accommodation)
            session.commit()


def block_service(engine, tab_id):
    """
    5.	Написать функцию, которая позволяет заблокировать услугу по ID ЛС.
    """
    with Session(engine) as session:
        accommodation = session.query(Accommodation).filter(
            Accommodation.tab_id == tab_id).one()
        accommodation.status = False
        session.add(accommodation)
        session.commit()


def about_user(engine, user_id):
    """
    6.	Написать функцию, которая по ID пользователя возвращает
    список всех активных ЛС, включая подключенные услуги и тарифы.  
    """
    with Session(engine) as session:
        tabs = session.query(Tabs).filter(Tabs.user_id == user_id).all()

        res = {'user_id': user_id,
               'tabs': []}
        for tab in tabs:
            res['tabs'].append({'number': tab.number,
                                'name': tab.name,
                                'create date': tab.create_date,
                                'update date': tab.update_date,
                                }
                               )
            accommodation = session.query(Accommodation).filter(
                Accommodation.tab_id == tab.id).first()
            if accommodation:
                service = session.query(Services).filter(
                    Services.id == accommodation.service_id).one()
                plan = session.query(Plans).filter(
                    Plans.id == accommodation.plan_id,
                    Plans.service_id == accommodation.service_id
                ).one()

                res['tabs'][-1].update({'service': {'name': service.name,
                                                    'plan': plan.name,
                                                    'price': plan.price,
                                                    'description': plan.desc
                                                    }
                                        }
                                       )

        return res


if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    pprint(about_user(engine, 1))
