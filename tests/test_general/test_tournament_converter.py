import json

import pytest  # type: ignore
import sofascrape.schemas.general as sofaschemas
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore

from sqlsofa.general import TournamentComponentConverter  # Fixed: added missing 'r'


@pytest.fixture
def example_data() -> sofaschemas.TournamentData:
    nbu = NotebookUtils(type=NoteBookType.GENERAL, web_on=False)
    raw_data = nbu.load(file_name="tournament_1")
    return sofaschemas.TournamentData.model_validate(raw_data)


def test_basic_setup(example_data):
    tournamentConveter = TournamentComponentConverter()
    tournamentConveter.convert(example_data)

    print("")
    print("=" * 30)
    print(example_data.model_dump_json(indent=6))

    if tournamentConveter.data:
        for x in tournamentConveter.data:
            print(repr(x))
