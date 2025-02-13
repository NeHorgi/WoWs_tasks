import pytest

parameters_for_test = [10 ** 7, 1.5 * 10 ** 7, 5 * 10 ** 7, 10 ** 8, 5 * 10 ** 8, 10 ** 9, 1.5 * 10 ** 9]


@pytest.mark.parametrize('parameter', parameters_for_test)
def test_parametrize_task_1(parameter, wiki_table_data):
    errors = []
    for table_row in wiki_table_data:
        if parameter > table_row.popularity:
            errors.append(f'{table_row.name} (Frontend:{table_row.front}|Backend:{table_row.back}) has '
                          f'{table_row.popularity} unique visitors per month. (Expected less than {parameter})')
    assert not errors, '\n'.join(errors)
