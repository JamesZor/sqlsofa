import json

import pytest  # type: ignore
import sofascrape.schemas.general as sofaschemas  # type: ignore
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore

from sqlsofa.general import EventsComponentConverter  # type: ignore


@pytest.fixture
def example_data() -> sofaschemas.EventsListSchema:
    nbu = NotebookUtils(type=NoteBookType.GENERAL, web_on=False)
    raw_data = nbu.load(file_name="events_season_61627")
    return sofaschemas.EventsListSchema.model_validate(raw_data)


def test_basic_setup(example_data):
    print("")

    for event in example_data.events[:1]:
        print("+" * 40)
        print(event.model_dump_json(indent=8))

    eventsConverter = EventsComponentConverter()
    eventsConverter.convert(example_data)

    for ev in eventsConverter.data[:3]:
        print("-" * 40)
        print(ev.model_dump_json(indent=8))
