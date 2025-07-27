import json

import pytest  # type: ignore
import sofascrape.schemas.general as sofaschemas  # type: ignore
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore

from sqlsofa.general import SeasonsComponentConverter  # type: ignore


@pytest.fixture
def example_data():
    nbu = NotebookUtils(type=NoteBookType.GENERAL, web_on=False)
    raw_data = nbu.load(file_name="seasons_1")
    return sofaschemas.SeasonsListSchema.model_validate(raw_data)


def test_basic_setup(example_data):
    print("")
    seasonsConvertor = SeasonsComponentConverter()
    for s in example_data.seasons[:3]:
        print(s)

    seasonsConvertor.convert(example_data)

    for s in seasonsConvertor.raw_data[:3]:
        print(s)

    seasonsConvertor.normilise()

    for s in seasonsConvertor.data:
        print(s)
