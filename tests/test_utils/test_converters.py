import json
import pprint

import pytest  # type: ignore
import sofascrape.schemas.general as sofaschemas
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore

import sqlsofa.utils.converters as converter  # type: ignore


@pytest.fixture
def tournamentData() -> sofaschemas.TournamentData:
    nbu = NotebookUtils(type=NoteBookType.GENERAL, web_on=False)
    raw_data = nbu.load(file_name="tournament_1")
    return sofaschemas.TournamentData.model_validate(raw_data)


@pytest.fixture
def eventsListData() -> sofaschemas.EventsListSchema:
    nbu = NotebookUtils(type=NoteBookType.GENERAL, web_on=False)
    raw_data = nbu.load(file_name="events_season_61627")
    return sofaschemas.EventsListSchema.model_validate(raw_data)


@pytest.fixture
def seasonsList() -> sofaschemas.SeasonsListSchema:
    nbu = NotebookUtils(type=NoteBookType.GENERAL, web_on=False)
    raw_data = nbu.load(file_name="seasons_1")
    return sofaschemas.SeasonsListSchema.model_validate(raw_data)


## football
# base
@pytest.fixture
def footballBaseMatchEvent() -> sofaschemas.FootballDetailsSchema:
    nbu = NotebookUtils(type=NoteBookType.FOOTBALL, web_on=False)
    raw_data = nbu.load(file_name="football_base_match_12436870")
    return sofaschemas.FootballDetailsSchema.model_validate(raw_data)


@pytest.fixture
def footballMatchStatistics() -> sofaschemas.FootballStatsSchema:
    nbu = NotebookUtils(type=NoteBookType.FOOTBALL, web_on=False)
    raw_data = nbu.load(file_name="football_stats_12436870")
    return sofaschemas.FootballStatsSchema.model_validate(raw_data)


def test_tournament(tournamentData):
    print("")
    print("=" * 30)
    print(tournamentData.model_dump_json(indent=6))
    print(converter.tournament(tournamentData.tournament))


def test_seasons(seasonsList):
    print("")
    print("=" * 30)
    for s in seasonsList.seasons[:3]:
        print(s.model_dump_json(indent=2))

    seasons_sql = [converter.season(season=s) for s in seasonsList.seasons]
    print("+" * 30)
    for s in seasons_sql[:3]:
        pprint.pprint(s, indent=2, width=120)


def test_events(eventsListData):
    print("")
    print("=" * 30)
    for e in eventsListData.events[:2]:
        print(e.model_dump_json(indent=6))

    events_sql = [converter.event(event=event) for event in eventsListData.events]
    print("+" * 30)
    for e in events_sql[:2]:

        print(".." * 10)
        pprint.pprint(e, indent=4, width=120)  # Much more readable!


def test_events_sets(eventsListData):
    print("")
    print("=" * 30)
    events_sql = [converter.event(event=event) for event in eventsListData.events]
    print("+" * 30)
    sports = [event.get("sport") for event in events_sql]
    print(f"{len(sports)=}, {sports[0:3] =}")
    sports_set = set(sports)
    print(f"{len(sports_set)= }")
    print("+" * 30)
    hometeam = [event.get("home_team") for event in events_sql]
    awayteam = [event.get("away_team") for event in events_sql]
    teams = hometeam + awayteam
    print(f"{len(teams)=}, {teams[0:3] =}")
    teams_set = set(teams)
    print(f"{len(teams_set)= }")


def test_football_match_event(footballBaseMatchEvent):
    print("")
    print("=" * 30)
    print(footballBaseMatchEvent.model_dump_json(indent=8))

    print("+" * 30)
    football_event_results = converter.FootballEventResult(footballBaseMatchEvent.event)
    pprint.pprint(football_event_results, indent=8, width=100)


def test_football_statistics(footballMatchStatistics):
    print("")
    print("=" * 30)
    print(footballMatchStatistics.model_dump_json(indent=8))

    print("+" * 30)
    stats_results = converter.football_stats(footballMatchStatistics)
    pprint.pprint(stats_results, indent=8, width=100)
