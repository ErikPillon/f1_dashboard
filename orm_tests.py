import pytest
from lap_ingestion import get_quali_data, get_race_id
from unittest.mock import patch, Mock


@pytest.fixture
def mock_ff1_session():
    with patch("fastf1.get_session") as mock_get_session:
        yield mock_get_session


@pytest.fixture
def mock_orm_races():
    with patch("orm.Races") as mock_Races:
        yield mock_Races


def test_get_quali_data(mock_ff1_session):
    year = 2022
    gp = 1
    mock_session = Mock()
    mock_ff1_session.return_value = mock_session

    result = get_quali_data(year, gp)

    mock_ff1_session.assert_called_once_with(year, gp, "Q")
    assert result == mock_session


def test_get_race_id(mock_orm_races):
    year = 2022
    gp = 1
    mock_race = Mock()
    mock_race.year = year
    mock_race.gp = gp
    mock_orm_races.query.filter_by.return_value.first.return_value = mock_race

    result = get_race_id(year, gp)

    mock_orm_races.query.filter_by.assert_called_once_with(year=year, gp=gp)
    assert result == mock_race.id


def test_get_quali_data_raises_error(mock_ff1_session):
    year = 2022
    gp = 1
    mock_ff1_session.side_effect = Exception("Mocked error")

    with pytest.raises(Exception):
        get_quali_data(year, gp)


def test_get_race_id_raises_error(mock_orm_races):
    year = 2022
    gp = 1
    mock_orm_races.query.filter_by.return_value.first.return_value = None

    with pytest.raises(Exception):
        get_race_id(year, gp)
