import json

import pytest  # type: ignore
import sofascrape.schemas.general as sofaschemas  # type: ignore
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore

from sqlsofa.football import EventFootballComponentConverter  # type: ignore


@pytest.fixture
def example_data() -> sofaschemas.FootballEventSchema:
    nbu = NotebookUtils(type=NoteBookType.FOOTBALL, web_on=False)
    raw_data = nbu.load(file_name="event_140_season_61627")
    return sofaschemas.FootballEventSchema.model_validate(raw_data)


def test_basic_setup(example_data):
    print()
    event_converter = EventFootballComponentConverter()
    print(example_data.model_dump_json(indent=6))

    event_converter.convert(example_data)
    print(event_converter.raw_data)
