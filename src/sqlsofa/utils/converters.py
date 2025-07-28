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


class VenueResult(TypedDict):
    venue: sqlschema.Venue
    city: sqlschema.Country
    venueCoordinates: sqlschema.VenueCoordinates
    stadium: sqlschema.Stadium
    country: sqlschema.Country


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


class FootballEventResult(TypedDict):
    # Tournament chain
    sport: sqlschema.Sport
    category: sqlschema.Category
    tournament: sqlschema.Tournament

    # Season
    season: sqlschema.Season

    # Teams and related
    home_team: sqlschema.Team
    away_team: sqlschema.Team
    home_team_colors: Optional[sqlschema.TeamColors]
    away_team_colors: Optional[sqlschema.TeamColors]
    home_country: Optional[sqlschema.Country]
    away_country: Optional[sqlschema.Country]

    # Event details
    status: sqlschema.Status
    round_info: sqlschema.RoundInfo
    time_football: Optional[sqlschema.TimeFootball]
    home_score: Optional[sqlschema.Score]
    away_score: Optional[sqlschema.Score]

    # Football-specific
    venue: Optional[sqlschema.Venue]
    venue_city: Optional[sqlschema.City]
    venue_stadium: Optional[sqlschema.Stadium]
    referee: Optional[sqlschema.Referee]

    # Main event
    event: sqlschema.Event


class RefereeResult(TypedDict):
    """Result from referee conversion with all dependencies."""

    sport: sqlschema.Sport
    country: sqlschema.Country
    referee: sqlschema.Referee


class FootballStatisticItemResult(TypedDict):
    """Result from football statistic item conversion."""

    statistic_item: sqlschema.FootballStatisticItem


class StatisticGroupResult(TypedDict):
    """Result from statistic group conversion with all items."""

    statistic_group: sqlschema.StatisticGroup
    statistic_items: List[sqlschema.FootballStatisticItem]


class FootballStatisticPeriodResult(TypedDict):
    """Result from football statistic period conversion with all groups and items."""

    statistic_period: sqlschema.FootballStatisticPeriod
    statistic_groups: List[sqlschema.StatisticGroup]
    statistic_items: List[sqlschema.FootballStatisticItem]


class FootballStatsResult(TypedDict):
    """Result from complete football stats conversion."""

    statistic_periods: List[sqlschema.FootballStatisticPeriod]
    statistic_groups: List[sqlschema.StatisticGroup]
    statistic_items: List[sqlschema.FootballStatisticItem]


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


def city(city: sofaschema.CitySchema) -> sqlschema.City:
    return sqlschema.City(**city.to_sql_dict())


def venueCoordinates(
    venue_coordinates: sofaschema.VenueCoordinatesSchema,
) -> sqlschema.VenueCoordinates:
    return sqlschema.VenueCoordinates(**venue_coordinates.to_sql_dict())


def stadium(
    stadium: sofaschema.StadiumSchema,
) -> sqlschema.Stadium:
    return sqlschema.Stadium(**stadium.to_sql_dict())


##############################
# Composite Converters
##############################


def venue(venue: sofaschema.VenueSchema) -> VenueResult:
    """
    Convert category with all dependencies.
    Returns: dict with 'city', venueCoordinates, country, stadium keys
    """
    city_results = city(venue.city)
    venueCoordinates_results = venueCoordinates(venue.venueCoordinates)
    country_results = country(venue.country)
    stadium_results = stadium(venue.stadium)

    return VenueResult(
        venue=sqlschema.Venue(**venue.to_sql_dict()),
        city=city_results,
        venueCoordinates=venueCoordinates_results,
        stadium=stadium_results,
        country=country_results,
    )


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


def referee(referee: sofaschema.RefereeSchema) -> RefereeResult:
    """
    Convert referee with all dependencies.
    Returns: dict with 'sport', 'country', and 'referee' keys
    """
    # Convert dependencies
    sport_result = sport(referee.sport)
    country_result = country(referee.country)

    return RefereeResult(
        sport=sport_result,
        country=country_result,
        referee=sqlschema.Referee(**referee.to_sql_dict()),
    )


def event_football(event: sofaschema.FootballEventSchema) -> FootballEventResult:
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

    # Football
    venue_result = venue(event.venue) if event.venue else None
    referee_result = referee(event.referee) if event.referee else None

    return FootballEventResult(
        # Tournament chain
        sport=tournament_result["sport"],
        category=tournament_result["category"],
        tournament=tournament_result["tournament"],
        # Season
        season=season_result,
        # Teams and related (football-specific)
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
        # Football-specific objects
        venue=venue_result["venue"] if venue_result else None,
        venue_city=venue_result["city"] if venue_result else None,
        venue_stadium=venue_result["stadium"] if venue_result else None,
        referee=referee_result["referee"] if referee_result else None,
        # Main event (with all football-specific fields)
        event=sqlschema.Event(**event.to_sql_dict()),
    )


##############################
# Statistics Component Entities
##############################


def football_statistic_item(
    item: sofaschema.FootballStatisticItemSchema,
) -> FootballStatisticItemResult:
    """
    Convert individual football statistic item.
    Returns: dict with 'statistic_item' key
    """
    return FootballStatisticItemResult(
        statistic_item=sqlschema.FootballStatisticItem(**item.to_sql_dict())
    )


def statistic_group(group: sofaschema.StatisticGroupSchema) -> StatisticGroupResult:
    """
    Convert statistic group with all its items.
    Returns: dict with 'statistic_group' and 'statistic_items' keys
    """
    # Convert all statistic items
    items_results = [football_statistic_item(item) for item in group.statisticsItems]
    statistic_items = [result["statistic_item"] for result in items_results]

    return StatisticGroupResult(
        statistic_group=sqlschema.StatisticGroup(**group.to_sql_dict()),
        statistic_items=statistic_items,
    )


def football_statistic_period(
    period: sofaschema.FootballStatisticPeriodSchema,
) -> FootballStatisticPeriodResult:
    """
    Convert football statistic period with all groups and items.
    Returns: dict with 'statistic_period', 'statistic_groups', and 'statistic_items' keys
    """
    # Convert all groups (which includes their items)
    groups_results = [statistic_group(group) for group in period.groups]

    # Extract groups and flatten all items
    statistic_groups = [result["statistic_group"] for result in groups_results]
    statistic_items = []
    for result in groups_results:
        statistic_items.extend(result["statistic_items"])

    return FootballStatisticPeriodResult(
        statistic_period=sqlschema.FootballStatisticPeriod(**period.to_sql_dict()),
        statistic_groups=statistic_groups,
        statistic_items=statistic_items,
    )


def football_stats(stats: sofaschema.FootballStatsSchema) -> FootballStatsResult:
    """
    Convert complete football statistics with all periods, groups, and items.
    Returns: dict with 'statistic_periods', 'statistic_groups', and 'statistic_items' keys
    """
    # Convert all periods (which includes their groups and items)
    periods_results = [football_statistic_period(period) for period in stats.statistics]

    # Extract periods and flatten all groups and items
    statistic_periods = [result["statistic_period"] for result in periods_results]
    statistic_groups = []
    statistic_items = []

    for result in periods_results:
        statistic_groups.extend(result["statistic_groups"])
        statistic_items.extend(result["statistic_items"])

    return FootballStatsResult(
        statistic_periods=statistic_periods,
        statistic_groups=statistic_groups,
        statistic_items=statistic_items,
    )
