from colors import Colors

# tests/test_colors.py
import pytest


def test_colors_init():
    colors = Colors(2024)
    assert colors._session is not None


def test_get_driver_color():
    colors = Colors(2024)
    driver_color = colors.get_driver_color("HAM")
    assert driver_color is not None


def test_get_driver_colors():
    colors = Colors(2024)
    driver_colors = colors.get_driver_colors()
    assert isinstance(driver_colors, dict)


def test_get_team_color():
    colors = Colors(2024)
    team_color = colors.get_team_color("Mercedes")
    assert team_color is not None


def test_get_team_colors():
    colors = Colors(2024)
    team_colors = colors.get_team_colors()
    assert isinstance(team_colors, dict)


def test_set_colors_to_drivers():
    colors = Colors(2024)
    colors._set_colors_to_drivers()
    assert colors._DRIVER_COLORS != {}


def test_set_colors_to_teams():
    colors = Colors(2024)
    colors._set_colors_to_teams()
    assert colors._TEAM_COLORS != {}


def test_set_drivers_team_association():
    colors = Colors(2024)
    colors._set_drivers_team_association(year=2024)
    assert colors._DRIVERS_TO_TEAMS != {}


@pytest.mark.parametrize("year", [2020, 2021, 2022, 2023, 2024])
def test_colors_init_with_different_years(year):
    colors = Colors(year)
    assert colors._session is not None


def test_colors_init_with_invalid_year():
    with pytest.raises(ValueError):
        _ = Colors(2025)


def test_get_driver_color_with_invalid_driver():
    colors = Colors(2024)
    assert colors.get_driver_color("Invalid Driver") is None


def test_get_team_color_with_invalid_team():
    colors = Colors(2024)
    assert colors.get_team_color("Invalid Team") is None
