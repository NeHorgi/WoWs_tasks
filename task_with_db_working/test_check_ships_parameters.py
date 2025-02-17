import pytest
from models import Ship, Weapon, Hull, Engine


def get_ship_data(session):
    ships = session.query(Ship).all()
    return {
        ship.id: {
            "weapon": ship.weapon,
            "hull": ship.hull,
            "engine": ship.engine
        }
        for ship in ships
    }


def get_component_data(session, model):
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
    randomized_data = get_ship_data(temp_db_session)

    for ship_id, original in original_data["ships"].items():
        randomized = randomized_data[ship_id]

        for component in ["weapon", "hull", "engine"]:
            assert original[component] == randomized[component], (
                f"Ship {ship_id}: {component}: "
                f"expected: {original[component]}, got: {randomized[component]}"
            )


@pytest.mark.parametrize("model, component_name", [
    (Weapon, "weapon"),
    (Hull, "hull"),
    (Engine, "engine"),
])
def test_component_parameters_change(original_data, temp_db_session, model, component_name):
    randomized_data = get_component_data(temp_db_session, model)

    for component_id, original_params in original_data[component_name + "s"].items():
        randomized_params = randomized_data[component_id]

        for param, original_value in original_params.items():
            assert original_value == randomized_params[param], (
                f"Component {component_name} {component_id}: {param}: "
                f"expected: {original_value}, got: {randomized_params[param]}"
            )
