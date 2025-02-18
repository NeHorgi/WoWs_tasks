import random


class Constants:
    db_path = "sqlite:///test_db.db"
    value_range = (1, 20)
    ships_count = 200
    weapons_count = 20
    hulls_count = 6
    engines_count = 7


constants = Constants()


def random_value():
    return random.randint(*constants.value_range)
