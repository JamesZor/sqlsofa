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
