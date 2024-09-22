from fetcher import fetch_drivers_by_year, fetch_seasons_years
import fastf1 as ff1
from fastf1 import plotting


class Colors:
    _DRIVERS = []
    _TEAMS = []
    _DRIVERS_TO_TEAMS = {}

    _DRIVER_COLORS = {}

    def __init__(self, year: int, round: int = 1) -> None:
        self._year = year
        self._set_drivers_team_association(year=year)
        self._set_colors_to_drivers(year=year)

    def _set_drivers_team_association(self, year: int) -> None:
        colors = fetch_drivers_by_year(year)

        self._DRIVERS = colors["code"].unique()
        self._TEAMS = colors["name"].unique()

        for driver in self._DRIVERS:
            if not len(colors[colors["code"] == driver]["name"].unique()) == 1:
                print(
                    f"impossible to uniquely assign driver to a team. Multiple teams or not teams were found for driver {driver} in the {year} season"
                )
            else:
                self._DRIVERS_TO_TEAMS[driver] = colors[colors["code"] == driver][
                    "name"
                ].unique()[0]

    def _set_colors_to_drivers(self, year: int, round: int = 1) -> None:
        session = ff1.get_session(year, round, "R")
        session.load()
        for driver in self._DRIVERS:
            try:
                self._DRIVER_COLORS[driver] = ff1.plotting.get_driver_color(
                    driver, session
                )
            except Exception as e:
                self._DRIVER_COLORS[driver] = None
                print(f"Driver color not found for driver {driver}: {e} ")

    @classmethod
    def get_team_color(cls, team_name: str) -> str:
        return Exception

    @classmethod
    def get_driver_color(cls, driver: str) -> str:
        return cls._DRIVER_COLORS.get(driver, None)


if __name__ == "__main__":
    colors = Colors(2024)
    breakpoint()
    print(colors)
