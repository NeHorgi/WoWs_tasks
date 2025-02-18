import pytest
from models import Ship, Weapon, Hull, Engine
from sqlalchemy.orm import Session


def get_ship_data(session: Session) -> dict[str, dict[str, str]]:
    """
    Get ships data from database by given session.

    Example:
        {'Ship-1': {'weapon': 'Weapon-7', 'hull': 'Hull-3', 'engine': 'Engine-5'}, ...}

    :param session: Database session.
    :return: Dict with ships data from database by given session.
    """
    ships = session.query(Ship).all()
    return {
        ship.id: {
            "weapon": ship.weapon,
            "hull": ship.hull,
            "engine": ship.engine
        }
        for ship in ships
    }


def get_component_data(session: Session, model: Weapon | Hull | Engine) -> dict[str, dict[str, str | int]]:
    """
    Get components data from database by given session.

    Example:
        {'Engine-6': {'name': 'Engine-6', 'power': 8, 'speed': 2}, ...}

    :param session: Database session.
    :param model: Current module of ship from database.
    :return: Dict with modules data from database by given session and current module.
    """
    records = session.query(model).all()
    return {
        record.id: {col.name: getattr(record, col.name) for col in model.__table__.columns if col.name != "id"}
        for record in records
    }


@pytest.fixture
def original_data(db_session):
    return {
        "ships": get_ship_data(db_session),
        "weapons": get_component_data(db_session, Weapon),
        "hulls": get_component_data(db_session, Hull),
        "engines": get_component_data(db_session, Engine),
    }


def test_ship_components_change(original_data, temp_db_session):
    errors = []
    randomized_data = get_ship_data(temp_db_session)

    for ship_id, original in original_data["ships"].items():
        randomized = randomized_data[ship_id]

        for component in ["weapon", "hull", "engine"]:
            if original[component] != randomized[component]:
                errors.append(f"Ship {ship_id}: {component}: "
                              f"expected: {original[component]}, got: {randomized[component]}")
    assert not errors


@pytest.mark.parametrize("model, component_name", [
    (Weapon, "weapon"),
    (Hull, "hull"),
    (Engine, "engine"),
])
def test_component_parameters_change(original_data, temp_db_session, model, component_name):
    errors = []
    randomized_data = get_component_data(temp_db_session, model)

    for component_id, original_params in original_data[component_name + "s"].items():
        randomized_params = randomized_data[component_id]

        for param, original_value in original_params.items():
            if original_value != randomized_params[param]:
                errors.append(f"Component {component_name} {component_id}: {param}: "
                              f"expected: {original_value}, got: {randomized_params[param]}")
    assert not errors
