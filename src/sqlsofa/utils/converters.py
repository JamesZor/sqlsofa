from typing import Any, Dict, List, Optional, TypedDict, Union

import sofascrape.schemas.general as sofaschema  # type: ignore

import sqlsofa.schema.sqlmodels as sqlschema

##############################
# Type Definitions for Return Values
##############################


class CategoryResult(TypedDict):
    """Result from category conversion with all dependencies."""

    sport: sqlschema.Sport
    category: sqlschema.Category


class TournamentResult(TypedDict):
    """Result from tournament conversion with all dependencies."""

    sport: sqlschema.Sport
    category: sqlschema.Category
    tournament: sqlschema.Tournament


class SeasonResult(TypedDict):
    """Result from season conversion."""

    season: sqlschema.Season


class TeamResult(TypedDict):
    """Result from team conversion with all dependencies."""

    sport: sqlschema.Sport
    country: sqlschema.Country
    team_colors: sqlschema.TeamColors
    team: sqlschema.Team


class EventResult(TypedDict):
    """Result from event conversion with all dependencies."""

    # Tournament chain
    sport: sqlschema.Sport
    category: sqlschema.Category
    tournament: sqlschema.Tournament
    # Season
    season: sqlschema.Season
    # Teams
    home_team: sqlschema.Team
    away_team: sqlschema.Team
    home_team_colors: sqlschema.TeamColors
    away_team_colors: sqlschema.TeamColors
    home_country: sqlschema.Country
    away_country: sqlschema.Country
    # Event details
    status: sqlschema.Status
    round_info: sqlschema.RoundInfo
    time_football: Optional[sqlschema.TimeFootball]
    home_score: Optional[sqlschema.Score]
    away_score: Optional[sqlschema.Score]
    # Main event
    event: sqlschema.Event


##############################
# Simple Converters
##############################


def sport(sport: sofaschema.SportSchema) -> sqlschema.Sport:
    """Convert single sport schema to SQLModel."""
    return sqlschema.Sport(**sport.to_sql_dict())


def country(country: sofaschema.CountrySchema) -> sqlschema.Country:
    """Convert single country schema to SQLModel."""
    return sqlschema.Country(**country.to_sql_dict())


def team_colors(colors: sofaschema.TeamColorsSchema) -> sqlschema.TeamColors:
    """Convert team colors schema to SQLModel."""
    return sqlschema.TeamColors(**colors.to_sql_dict())


def season(season: sofaschema.SeasonSchema) -> sqlschema.Season:
    """Convert season schema to SQLModel."""
    return sqlschema.Season(**season.to_sql_dict())


def status(status: sofaschema.StatusSchema) -> sqlschema.Status:
    """Convert status schema to SQLModel."""
    return sqlschema.Status(**status.to_sql_dict())


def round_info(round_info: sofaschema.RoundInfoSchema) -> sqlschema.RoundInfo:
    """Convert round info schema to SQLModel."""
    return sqlschema.RoundInfo(**round_info.to_sql_dict())


def time_football(
    time: sofaschema.TimeFootballSchema,
) -> sqlschema.TimeFootball:
    """Convert time football schema to SQLModel."""
    return sqlschema.TimeFootball(**time.to_sql_dict())


def score(score: sofaschema.ScoreFootballSchema) -> sqlschema.Score:
    """Convert score schema to SQLModel."""
    return sqlschema.Score(**score.to_sql_dict())


##############################
# Composite Converters
##############################


def category(category: sofaschema.CategorySchema) -> CategoryResult:
    """
    Convert category with all dependencies.
    Returns: dict with 'sport' and 'category' keys
    """
    return CategoryResult(
        sport=sport(category.sport),
        category=sqlschema.Category(**category.to_sql_dict()),
    )


def tournament(tournament: sofaschema.TournamentSchema) -> TournamentResult:
    """
    Convert tournament with all dependencies.
    Returns: dict with 'sport', 'category', and 'tournament' keys
    """
    category_result = category(tournament.category)

    return TournamentResult(
        sport=category_result["sport"],
        category=category_result["category"],
        tournament=sqlschema.Tournament(**tournament.to_sql_dict()),
    )


def team(team_schema: sofaschema.TeamSchema) -> Dict[str, Any]:
    """
    Enhanced version of your team converter with foreign keys.
    Returns all team-related objects with proper relationships.
    """
    # Convert dependencies first
    sport_obj = sport(team_schema.sport)
    country_obj = country(team_schema.country)
    team_colors_obj = team_colors(team_schema.teamColors)

    # Get team data and add foreign keys
    team_data = team_schema.to_sql_dict()

    # Add foreign keys using source IDs (since no DB yet)
    team_data.update(
        {
            "sport_id": sport_obj.id,
            # For country, you might need to handle this differently if countries don't have IDs
            # 'country_id': country_obj.id,  # Uncomment if countries have IDs
            # 'team_colors_id': team_colors_obj.id,  # Will be None since colors don't have source IDs
        }
    )

    return {
        "sport": sport_obj,
        "country": country_obj,
        "team_colors": team_colors_obj,
        "team": sqlschema.Team(**team_data),
    }


def event(event: sofaschema.EventSchema) -> EventResult:
    """
    Convert complete event with ALL dependencies.
    Returns: dict with all related objects
    """
    # Convert tournament chain
    tournament_result = tournament(event.tournament)

    # Convert season
    season_result = season(event.season)

    # Convert teams
    home_team_result = team(event.homeTeam)
    away_team_result = team(event.awayTeam)

    # Convert event-specific objects
    status_result = status(event.status)
    round_info_result = round_info(event.roundInfo)

    # Optional objects
    time_result = time_football(event.time) if event.time else None
    home_score_result = score(event.homeScore) if event.homeScore else None
    away_score_result = score(event.awayScore) if event.awayScore else None

    return EventResult(
        # Tournament chain
        sport=tournament_result["sport"],
        category=tournament_result["category"],
        tournament=tournament_result["tournament"],
        # Season
        season=season_result,
        # Teams and related
        home_team=home_team_result["team"],
        away_team=away_team_result["team"],
        home_team_colors=home_team_result["team_colors"],
        away_team_colors=away_team_result["team_colors"],
        home_country=home_team_result["country"],
        away_country=away_team_result["country"],
        # Event details
        status=status_result,
        round_info=round_info_result,
        time_football=time_result,
        home_score=home_score_result,
        away_score=away_score_result,
        # Main event
        event=sqlschema.Event(**event.to_sql_dict()),
    )
