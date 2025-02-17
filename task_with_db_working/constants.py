import random


class Constants:
    db_path = "sqlite:///test_db.db"
    value_range = (1, 20)


constants = Constants()


def random_value():
    return random.randint(*constants.value_range)
