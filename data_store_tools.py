from random import randint
from typing import Optional

from sqlalchemy import create_engine, select, update, insert
from sqlalchemy.orm import Session, Load, sessionmaker
from sqlalchemy.exc import NoResultFound
import bcrypt

from config import SQLALCHEMY_DATABASE_URI
from models import Users, Plans, Tabs, Services, Accommodations


class DataStoreTools():

    def __init__(self, uri: str) -> None:
        self.engine = create_engine(uri)

    def session_executor(proc):
        def wrapper(*args, **kwargs):
            self = args[0]
            engine = self.engine
            sesion_factory = sessionmaker(
                engine,
                expire_on_commit=False
            )
            with sesion_factory() as session:
                with session.begin():
                    try:
                        res = proc(*args, **kwargs, session=session)
                    except NoResultFound as e:
                        print(f'error  - {e}')
                        return None
            return res
        return wrapper

    @session_executor
    def crate_user(
        self, name: str, phone: str, mail: str,
        login: str, password: str, session: Session
    ) -> None:
        """
        1.Написать функцию, которая принимает
        данные пользователя и создает его
        """
        user = Users(
            name=name,
            phone=phone,
            mail=mail,
            login=login,
            password=bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()),
        )
        session.add(user)

    @session_executor
    def create_plan(
        self, name: str, desc: str, price: int,
        service_id: int, session: Session
    ) -> None:
        plan = Plans(
            name=name,
            service_id=service_id,
            desc=desc,
            price=price
        )
        session.add(plan)

    @session_executor
    def create_service(self, name: str, session: Session) -> None:
        service = Services(name=name)
        session.add(service)

    @session_executor
    def create_tab(self, name: str, user_id: int, session: Session) -> None:
        '''
        2.Написать функцию, которая принимает название ЛС,
        создает его и привязывает к определенному пользователю.
        Номер счета генерируется автоматически
        '''
        tab = Tabs(
            number=randint(1000000, 9999999),
            name=name,
            user_id=user_id,
        )
        session.add(tab)

    @session_executor
    def create_accommodation(
        self, service_name: str, plan_name: str,
        tab_id: int, addres: str, session: Session
    ) -> None:
        """
        3.	Написать функцию, которая:
            Получает услугу из перечня по ее английскому наименованию (коду).
            Получает тариф услуги из перечня по его английскому
            наименованию (коду). Привязывает услугу с выбранным тарифом к
            определенному ЛС в статусе Активна
        """

        service = self.get_service(service_name=service_name)
        plan = self.get_plan(service_id=service.id, plan_name=plan_name)
        tab = self.get_tab(tab_id=tab_id)

        try:
            ac_query = insert(Accommodations).values(
                service_id=service.id,
                addres=addres,
                tab_id=tab.id,
                plan_id=plan.id,
            )
        except AttributeError as e:
            print(f'error  - {e}')
            return None

        session.execute(ac_query)

    @session_executor
    def update_plan(
        self, tab_id: int, plan_id: int, session: Session
    ) -> None:
        '''
        4. Написать функцию, которая позволяет изменить тариф услуги по ID ЛС
        '''
        query_plan = select(Plans).options(
            Load(Plans)).where(Plans.id == plan_id)
        query_plan_result = session.execute(query_plan)
        plan = query_plan_result.scalar_one()

        if plan:
            query = update(Accommodations).where(
                Accommodations.tab_id == tab_id).values(plan_id=plan.id)

            session.execute(query)
            session.commit()

    @session_executor
    def block_service(self, tab_id: int, session: Session) -> None:
        """
        5.	Написать функцию, которая позволяет заблокировать услугу по ID ЛС
        """
        query = update(Accommodations).where(
            Accommodations.tab_id == tab_id).values(status=False)
        session.execute(query)

    @session_executor
    def get_tab(
        self, user_id: Optional[int] = None,
        tab_id: Optional[int] = None, one: bool = True,
        session: Optional[Session] = None
    ) -> Tabs:

        query_tab = select(Tabs).options(
            Load(Tabs)).where(
            Tabs.user_id == user_id if user_id else Tabs.id == tab_id
        )
        query_tab_result = session.execute(query_tab)
        if one:
            tabs = query_tab_result.scalar_one()
        else:
            tabs = query_tab_result.scalars().all()

        return tabs

    @session_executor
    def get_accommodation(self, tab: Tabs, session: Session):

        query_accommodation = select(Accommodations).options(
            Load(Accommodations)
        ).where(Accommodations.tab == tab)
        query_accommodation_res = session.execute(query_accommodation)
        accommodation = query_accommodation_res.scalars().first()

        return accommodation

    @session_executor
    def get_service(
        self, service_id: Optional[int] = None,
        service_name: Optional[str] = None,
        session: Session = None
    ) -> Services:

        query_service = select(Services).where(
            Services.id == service_id if service_id
            else Services.name == service_name
        )
        query_service_result = session.execute(query_service)
        service = query_service_result.scalar_one()

        return service

    @session_executor
    def get_plan(
        self, service_id: int,
        plan_id: Optional[int] = None,
        plan_name: Optional[str] = None,
        session: Optional[Session] = None
    ) -> Plans:

        query_plan = select(Plans).options(
            Load(Plans)).where(
                Plans.id == plan_id if plan_id
            else Plans.name == plan_name,
                Plans.service_id == service_id
        )

        query_plan_result = session.execute(query_plan)
        plan = query_plan_result.scalar_one()
        return plan

    def about_user(self, user_id: int) -> dict:
        """
        6.	Написать функцию, которая по ID пользователя возвращает
        список всех активных ЛС, включая подключенные услуги и тарифы.
        """

        tabs = self.get_tab(user_id, one=False)
        tabs = tabs if tabs else []

        res = {'user_id': user_id if tabs else "unknown_user",
               'tabs': []}

        for tab in tabs:
            res['tabs'].append(
                {'number': tab.number,
                    'name': tab.name,
                    'create_date': tab.create_date,
                    'update_date': tab.update_date,
                 }
            )

            accommodation = self.get_accommodation(tab)

            if accommodation:

                service = self.get_service(accommodation.service_id)
                plan = self.get_plan(
                    accommodation.service_id,
                    accommodation.plan_id
                )

                try:
                    res['tabs'][-1].update(
                        {'service': {'name': service.name,
                                     'plan': plan.name,
                                     'price': plan.price,
                                     'description': plan.desc
                                     }
                         }
                    )
                except AttributeError as e:
                    print(f'error  - {e}')
                    return None

        return res
