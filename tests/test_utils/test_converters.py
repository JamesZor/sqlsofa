import json
import pprint
from typing import List

import pytest  # type: ignore
import sofascrape.schemas.general as sofaschemas
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore

import sqlsofa.schema.sqlmodels as sqlschema
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


@pytest.fixture
def footballMatchLineup() -> sofaschemas.FootballLineupSchema:
    nbu = NotebookUtils(type=NoteBookType.FOOTBALL, web_on=False)
    raw_data = nbu.load(file_name="football_lineup_12436870")
    return sofaschemas.FootballLineupSchema.model_validate(raw_data)


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

    print("")


def test_football_statistics(footballMatchStatistics):
    print("=" * 30)
    print(footballMatchStatistics.model_dump_json(indent=8))

    print("+" * 30)
    stats_results = converter.football_stats(footballMatchStatistics)
    pprint.pprint(stats_results, indent=8, width=100)


def test_fixed_football_statistics(footballMatchStatistics):
    """Test the fixed converter to ensure relationships are maintained."""
    print("Testing Fixed Statistics Converter")
    print("=" * 50)

    # Convert using the fixed converter
    stats_results = converter.football_stats(footballMatchStatistics)

    # Check that relationships are properly set
    print(f"Total periods: {len(stats_results['statistic_periods'])}")
    print(f"Total groups: {len(stats_results['statistic_groups'])}")
    print(f"Total items: {len(stats_results['statistic_items'])}")
    print()

    # Verify relationships for each period
    for i, period in enumerate(stats_results["statistic_periods"]):
        print(f"\nPeriod {i+1}: {period.period}")
        print(f"  - Has {len(period.groups)} groups")
        print(f"  - Event: {'Set' if period.event else 'Not set'}")
        print(f"  - Event ID: {period.event_id}")

        # Check first group
        if period.groups:
            first_group = period.groups[0]
            print(f"\n  First Group: {first_group.groupName}")
            print(f"    - Has {len(first_group.statistics_items)} items")
            print(f"    - Linked to period: {first_group.statistic_period == period}")

            # Check first item
            if first_group.statistics_items:
                first_item = first_group.statistics_items[0]
                print(f"\n    First Item: {first_item.name}")
                print(f"      - Key: {first_item.key}")
                print(
                    f"      - Linked to group: {first_item.statistic_group == first_group}"
                )
                print(
                    f"      - Group has period: {first_item.statistic_group.statistic_period == period}"
                )

    print("\n" + "=" * 50)
    print("Relationship Verification:")

    # Verify all items have groups
    items_without_groups = [
        item
        for item in stats_results["statistic_items"]
        if item.statistic_group is None
    ]
    print(f"Items without groups: {len(items_without_groups)}")

    # Verify all groups have periods
    groups_without_periods = [
        group
        for group in stats_results["statistic_groups"]
        if group.statistic_period is None
    ]
    print(f"Groups without periods: {len(groups_without_periods)}")

    # Test with event linkage
    print("\n" + "=" * 50)
    print("Testing with Event linkage:")

    # Create a test event
    test_event = sqlschema.Event(
        id=12436870, slug="test-match", startTimestamp=1234567890
    )

    # Convert with event
    stats_with_event = converter.football_stats_with_event(
        footballMatchStatistics, test_event
    )

    # Check event linkage
    for period in stats_with_event["statistic_periods"]:
        print(f"\nPeriod {period.period}:")
        print(f"  - Linked to event: {period.event == test_event}")
        print(f"  - Event ID: {period.event_id}")

    return stats_results


def test_football_lineup(footballMatchLineup):
    print("")
    print("=" * 30)
    print(footballMatchLineup.model_dump_json(indent=8))

    # Create a test event (in real usage, this would come from event conversion)
    test_event = sqlschema.Event(
        id=12436870, slug="manchester-united-vs-fulham", startTimestamp=1234567890
    )

    # Create test teams (in real usage, these would come from event conversion)
    home_team = sqlschema.Team(
        id=35,
        name="Manchester United",
        slug="manchester-united",
        shortName="Man Utd",
        nameCode="MUN",
        gender="M",
    )

    away_team = sqlschema.Team(
        id=43,
        name="Fulham",
        slug="fulham",
        shortName="Fulham",
        nameCode="FUL",
        gender="M",
    )
    lineup_schema = footballMatchLineup
    # Convert lineup with event and team links
    result = converter.football_lineup(lineup_schema, test_event, home_team, away_team)

    print("+" * 30)
    pprint.pprint(result, indent=8, width=100)
    # Print summary
    print("Lineup Conversion Summary")
    print("=" * 50)
    print(f"Confirmed: {result['football_lineup'].confirmed}")
    print(f"Event ID: {result['football_lineup'].event_id}")
    print()

    # Home team summary
    home = result["home_lineup"]
    print(f"Home Team: {home_team.name}")
    print(f"  Formation: {home['team_lineup'].formation}")
    print(f"  Total players: {len(home['player_entries'])}")
    print(
        f"  Starting XI: {sum(1 for e in home['player_entries'] if not e['entry'].substitute)}"
    )
    print(
        f"  Substitutes: {sum(1 for e in home['player_entries'] if e['entry'].substitute)}"
    )
    print(f"  Missing players: {len(home['missing_players'])}")

    # Print starting XI
    print("\n  Starting XI:")
    for entry_result in home["player_entries"]:
        entry = entry_result["entry"]
        player = entry_result["player"]
        if not entry.substitute:
            captain = " (C)" if entry.captain else ""
            print(
                f"    #{entry.jerseyNumber} {player.name} - {entry.position}{captain}"
            )

    # Away team summary
    print()
    away = result["away_lineup"]
    print(f"Away Team: {away_team.name}")
    print(f"  Formation: {away['team_lineup'].formation}")
    print(f"  Total players: {len(away['player_entries'])}")
    print(
        f"  Starting XI: {sum(1 for e in away['player_entries'] if not e['entry'].substitute)}"
    )
    print(
        f"  Substitutes: {sum(1 for e in away['player_entries'] if e['entry'].substitute)}"
    )

    # Check relationships
    print("\n" + "=" * 50)
    print("Relationship Verification:")

    # Check lineup relationships
    football_lineup_obj = result["football_lineup"]
    print(f"Football lineup has {len(football_lineup_obj.lineups)} team lineups")

    # Check team lineup relationships
    home_lineup = result["home_lineup"]["team_lineup"]
    print(f"Home lineup has {len(home_lineup.players)} player entries")
    print(
        f"Home lineup linked to football lineup: {home_lineup.football_lineup == football_lineup_obj}"
    )

    # Check player entry relationships
    first_player_entry = home_lineup.players[0] if home_lineup.players else None
    if first_player_entry:
        print(
            f"First player entry linked to team lineup: {first_player_entry.team_lineup == home_lineup}"
        )
        print(
            f"First player has statistics: {first_player_entry.statistics is not None}"
        )

    # Get unique players and countries
    unique_players = get_unique_players(result)
    unique_countries = get_unique_countries(result)

    print(f"\nTotal unique players: {len(unique_players)}")
    print(f"Total unique countries: {len(unique_countries)}")

    return result


def get_unique_players(lineup_result: dict) -> List[sqlschema.LineupPlayer]:
    """Get unique players from lineup result."""
    seen_ids = set()
    unique_players = []

    for player in lineup_result["all_players"]:
        if player.id not in seen_ids:
            seen_ids.add(player.id)
            unique_players.append(player)

    return unique_players


def get_unique_countries(lineup_result: dict) -> List[sqlschema.Country]:
    """Get unique countries from lineup result."""
    seen_alpha3 = set()
    unique_countries = []

    for country in lineup_result["all_countries"]:
        if country.alpha3 not in seen_alpha3:
            seen_alpha3.add(country.alpha3)
            unique_countries.append(country)

    return unique_countries


def print_player_statistics_example(lineup_result: dict):
    """Print example of player statistics."""
    print("\n" + "=" * 50)
    print("Player Statistics Example:")

    # Find players with statistics
    for entry_result in lineup_result["home_lineup"]["player_entries"]:
        if entry_result["statistics"]:
            player = entry_result["player"]
            stats = entry_result["statistics"]
            print(f"\n{player.name} Statistics:")
            print(f"  Minutes played: {stats.minutesPlayed}")
            print(f"  Rating: {stats.rating}")
            print(f"  Total passes: {stats.totalPass}")
            print(f"  Accurate passes: {stats.accuratePass}")
            print(f"  Touches: {stats.touches}")
            if stats.goals:
                print(f"  Goals: {stats.goals}")
            if stats.goalAssist:
                print(f"  Assists: {stats.goalAssist}")
            break  # Just show one example
