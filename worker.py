from config import SQLALCHEMY_DATABASE_URI
from data_store_tools import DataStoreTools


if __name__ == '__main__':
    tools = DataStoreTools(SQLALCHEMY_DATABASE_URI)

    user = tools.crate_user("user two",
                            '+1981-345-21-17',
                            'admin2@mail.ru',
                            'admin2',
                            '123',
                            )

    tab = tools.create_tab('home_internet', user.id)

    service = tools.create_service('s_internet', '12412442')

    tools.create_plan('s_start', '50 mbps', 450, service.id)
    acc = tools.create_accommodation(
        's_internet', 's_start', tab.id, 'nsk'
    )
    print(tools.about_user(user.id))
