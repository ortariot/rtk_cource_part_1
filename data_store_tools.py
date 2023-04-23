from random import randint
from pprint import pprint

from sqlalchemy import create_engine, select, update, insert
from sqlalchemy.orm import Session, Load

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
                     )
        session.add(user)
        session.commit()


def crate_plan(engine, name, desc, price, service_id):
    with Session(engine) as session:
        plan = Plans(name=name,
                     service_id=service_id,
                     desc=desc,
                     price=price,
                     )
        session.add(plan)
        session.commit()


def create_service(engine, name):
    with Session(engine) as session:
        service = Services(name=name)
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
        query_service = select(Services).where(Services.name == service_name)
        query_service_result = session.execute(query_service)
        service = query_service_result.scalar_one()

        query_plan = select(Plans).options(Load(Plans)).where(Plans.name == plan_name,
                                                              Plans.service == service
                                                              )
        query_plan_result = session.execute(query_plan)
        plan = query_plan_result.scalar_one()

        query_tab = select(Tabs).options(Load(Tabs)).where(Tabs.id == tab_id)
        query_tab_result = session.execute(query_tab)
        tab = query_tab_result.scalar()

        ac_query = insert(Accommodation).values(service_id=service.id,
                                                addres=addres,
                                                tab_id=tab.id,
                                                plan_id=plan.id,
                                                )

        session.execute(ac_query)
        session.commit()


def update_plan(engine, tab_id, plan_id):
    '''
    4.	Написать функцию, которая позволяет изменить тариф услуги по ID ЛС.
    '''
    with Session(engine) as session:
        query_plan = select(Plans).options(
            Load(Plans)).where(Plans.id == plan_id)
        query_plan_result = session.execute(query_plan)
        plan = query_plan_result.scalar_one()

        if plan:
            query = update(Accommodation).where(
                Accommodation.tab_id == tab_id).values(plan_id=plan.id)

            session.execute(query)
        session.commit()


def block_service(engine, tab_id):
    """
    5.	Написать функцию, которая позволяет заблокировать услугу по ID ЛС.
    """
    with Session(engine) as session:
        query = update(Accommodation).where(
            Accommodation.tab_id == tab_id).values(status=False)
        session.execute(query)
        session.commit()


def about_user(engine, user_id):
    """
    6.	Написать функцию, которая по ID пользователя возвращает
    список всех активных ЛС, включая подключенные услуги и тарифы.  
    """
    with Session(engine) as session:

        query_tab = select(Tabs).options(
            Load(Tabs)).where(Tabs.user_id == user_id)
        query_tab_result = session.execute(query_tab)
        tabs = query_tab_result.scalars().all()

        res = {'user_id': user_id,
               'tabs': []}

        for tab in tabs:
            res['tabs'].append({'number': tab.number,
                                'name': tab.name,
                                'create date': tab.create_date,
                                'update date': tab.update_date,
                                }
                               )

            query_accommodation = select(Accommodation).options(
                Load(Accommodation)
            ).where(Accommodation.tab == tab)
            query_accommodation_res = session.execute(query_accommodation)
            accommodation = query_accommodation_res.scalars().first()
            print(accommodation)
            if accommodation:
                query_service = select(Services).where(
                    Services.id == accommodation.service_id)
                query_service_result = session.execute(query_service)
                service = query_service_result.scalar_one()

                query_plan = select(Plans).options(
                    Load(Plans)).where(Plans.id == accommodation.plan_id, Plans.service_id == accommodation.service_id)
                query_plan_result = session.execute(query_plan)
                plan = query_plan_result.scalar_one()

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
    print(about_user(engine, 1))
