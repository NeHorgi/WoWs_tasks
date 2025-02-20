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
def original_data(db_session: Session) -> dict[str, dict]:
    """
    Get all data from original database.

    :return: Suitable dict with all data from original database for work with it.
    """
    return {
        "ships": get_ship_data(db_session),
        "weapons": get_component_data(db_session, Weapon),
        "hulls": get_component_data(db_session, Hull),
        "engines": get_component_data(db_session, Engine),
    }


def test_ship_components_change(original_data: dict[str, dict], temp_db_session: Session):
    """
    Test checks that all components of all ships from original database have the save value with ships
    from temporary database.
    If not an error collects in a list of errors with info of error.

    :param original_data: Data from original database.
    :param temp_db_session: Temporary database session.
    """
    errors = []
    randomized_data = get_ship_data(temp_db_session)

    for ship_id, data in original_data["ships"].items():
        randomized = randomized_data[ship_id]

        for component in ["weapon", "hull", "engine"]:
            if data[component] != randomized[component]:
                errors.append(f"Ship {ship_id}: {component}: "
                              f"expected: {data[component]}, got: {randomized[component]}")
    assert not errors, "\n".join(errors)


@pytest.mark.parametrize("model, component_name", [
    (Weapon, "weapon"),
    (Hull, "hull"),
    (Engine, "engine"),
])
def test_component_parameters_change(original_data: dict[str, dict],
                                     temp_db_session: Session,
                                     model: Weapon | Hull | Engine,
                                     component_name: str):
    """
    Test checks parameters of components (Weapon, Hull, Engine) from original database and their difference between
    data from temporary database.

    The scenario:
    1. Get component data from the temporary database.
    2. Compares component's parameters from original and temporary database.
    3. Collects errors if any parameter values have changed.
    4. Asserts that no discrepancies exist.

    :param original_data: Data from original database.
    :param temp_db_session: Temporary database session.
    :param model: Component type.
    :param component_name: Name of the component.
    """
    errors = []
    randomized_data = get_component_data(temp_db_session, model)

    for component_id, original_params in original_data[component_name + "s"].items():
        randomized_params = randomized_data[component_id]

        for param, original_value in original_params.items():
            if original_value != randomized_params[param]:
                errors.append(f"Component {component_name} {component_id}: {param}: "
                              f"expected: {original_value}, got: {randomized_params[param]}")
    assert not errors, "\n".join(errors)
