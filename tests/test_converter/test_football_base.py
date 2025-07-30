# tests/test_converter/test_football_base.py
import json
import pprint
from collections import defaultdict
from typing import Dict, List

import pytest  # type: ignore
import sofascrape.schemas.general as sofaschemas
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore

import sqlsofa.schema.sqlmodels as sqlschema

# import sqlsofa.utils.converters as converter  # type: ignore
from sqlsofa.converters import DetailsComponentBuilder, FootballMatchConverter


@pytest.fixture
def footballMatch() -> sofaschemas.FootballMatchResultDetailed:
    nbu = NotebookUtils(type=NoteBookType.FOOTBALL, web_on=False)
    raw_data: sofaschemas.FootballMatchResultDetailed = nbu.load_pickle(
        file_name="football_match_0"
    )
    return raw_data


def test_football_match_event(footballMatch):
    print("")
    print("=" * 30)
    print(footballMatch.match_id)
    print("+" * 30)

    #    details_builder = DetailsComponentBuilder()

    print("")


def test_details_component_builder(footballMatch):
    """Test the DetailsComponentBuilder through FootballMatchConverter"""
    print("")
    print("=" * 30)
    print(f"Testing match: {footballMatch.match_id}")
    print("+" * 30)

    # Create the converter (which initializes all builders)
    converter = FootballMatchConverter(footballMatch)

    # Test that the details builder was created
    assert "base" in converter.builders
    assert isinstance(converter.builders["base"], DetailsComponentBuilder)

    # Test that it can build
    assert converter.builders["base"].can_build(), "failed to build base"

    # Run just the base/details builder
    converter.builders["base"].build()

    # Check that entities were created in entity_map
    assert converter.entity_map["sport"] is not None
    assert converter.entity_map["tournament"] is not None
    assert converter.entity_map["home_team"] is not None
    assert converter.entity_map["away_team"] is not None
    #    assert converter.entity_map["event"] is not None

    # Check that entities were added to normalized collections
    assert len(converter.normalized_entities["sports"]) > 0
    assert len(converter.normalized_entities["teams"]) >= 2  # At least home and away

    print(f"Sport: {converter.entity_map['sport'].name}")
    print(f"Tournament: {converter.entity_map['tournament'].name}")

    print("+" * 30)
    pprint.pprint(converter.entity_map, indent=9, width=100)


#    print(f"Event: {converter.entity_map['event'].slug}")
