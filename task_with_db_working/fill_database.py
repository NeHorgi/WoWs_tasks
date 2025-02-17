import random
from database import create_database, get_session
from models import Ship, Weapon, Hull, Engine
from task_with_db_working.constants import random_value


def fill_database():
    create_database()
    session = get_session()

    weapons = [Weapon(id=f"Weapon-{i}", name=f"Weapon-{i}", damage=random_value(), range=random_value(),
                      reload_time=random_value()) for i in range(1, 21)]
    hulls = [Hull(id=f"Hull-{i}", name=f"Hull-{i}", armor=random_value(), capacity=random_value())
             for i in range(1, 6)]
    engines = [Engine(id=f"Engine-{i}", name=f"Engine-{i}", power=random_value(), speed=random_value())
               for i in range(1, 7)]

    session.add_all(weapons + hulls + engines)

    ships = [Ship(
        id=f"Ship-{i}",
        name=f"Ship-{i}",
        weapon=random.choice(weapons).id,
        hull=random.choice(hulls).id,
        engine=random.choice(engines).id
    ) for i in range(1, 201)]
    session.add_all(ships)

    session.commit()
    session.close()
    print("Database was successfully filled.")


if __name__ == "__main__":
    fill_database()
