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
    """
    return FootballStatisticItemResult(
        statistic_item=sqlschema.FootballStatisticItem(**item.model_dump())
    )


def statistic_group(
    group: sofaschema.StatisticGroupSchema,
    period_obj: sqlschema.FootballStatisticPeriod,
) -> StatisticGroupResult:
    """
    Convert statistic group with all its items, maintaining relationships.
    """
    # Create the group object
    group_data = group.model_dump(exclude={"statisticsItems"})
    group_obj = sqlschema.StatisticGroup(**group_data)

    # Set the relationship to the period (not just the ID)
    group_obj.statistic_period = period_obj

    # Convert all statistic items and link them to this group
    statistic_items = []
    for item_schema in group.statisticsItems:
        item_result = football_statistic_item(item_schema)
        item_obj = item_result["statistic_item"]

        # Set the relationship to the group (not just the ID)
        item_obj.statistic_group = group_obj

        statistic_items.append(item_obj)

    # Assign the items to the group's relationship
    group_obj.statistics_items = statistic_items

    return StatisticGroupResult(
        statistic_group=group_obj, statistic_items=statistic_items
    )


def football_statistic_period(
    period: sofaschema.FootballStatisticPeriodSchema,
) -> FootballStatisticPeriodResult:
    """
    Convert football statistic period maintaining nested structure.
    """
    # Create period with fixed ID
    period_data = period.model_dump(exclude={"groups"})
    period_obj = sqlschema.FootballStatisticPeriod(**period_data)

    # Convert all groups and maintain the hierarchy
    statistic_groups = []
    all_items = []

    for group_schema in period.groups:
        group_result = statistic_group(group_schema, period_obj)
        group_obj = group_result["statistic_group"]

        statistic_groups.append(group_obj)
        all_items.extend(group_result["statistic_items"])

    # Assign groups to the period's relationship
    period_obj.groups = statistic_groups

    return FootballStatisticPeriodResult(
        statistic_period=period_obj,
        statistic_groups=statistic_groups,
        statistic_items=all_items,
    )


def football_stats(stats: sofaschema.FootballStatsSchema) -> FootballStatsResult:
    """
    Convert complete football statistics with all periods, groups, and items.
    Maintains all relationships properly.
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


def football_stats_with_event(
    stats: sofaschema.FootballStatsSchema, event: sqlschema.Event
) -> FootballStatsResult:
    """
    Convert complete football statistics and link to an event.
    """
    # Convert all periods
    periods_results = []

    for period_schema in stats.statistics:
        # Create period object
        period_data = period_schema.model_dump(exclude={"groups"})
        period_obj = sqlschema.FootballStatisticPeriod(**period_data)

        # Link to event
        period_obj.event = event
        period_obj.event_id = event.id

        # Convert groups for this period
        statistic_groups = []
        all_items = []

        for group_schema in period_schema.groups:
            group_result = statistic_group(group_schema, period_obj)
            statistic_groups.append(group_result["statistic_group"])
            all_items.extend(group_result["statistic_items"])

        # Set the groups relationship
        period_obj.groups = statistic_groups

        periods_results.append(
            FootballStatisticPeriodResult(
                statistic_period=period_obj,
                statistic_groups=statistic_groups,
                statistic_items=all_items,
            )
        )

    # Flatten results
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


# Result Types
class LineupPlayerResult(TypedDict):
    """Result from lineup player conversion."""

    player: sqlschema.LineupPlayer
    country: Optional[sqlschema.Country]


class PlayerStatisticsResult(TypedDict):
    """Result from player statistics conversion."""

    statistics: sqlschema.PlayerStatistics


class LineupPlayerEntryResult(TypedDict):
    """Result from lineup player entry conversion."""

    player: sqlschema.LineupPlayer
    player_country: Optional[sqlschema.Country]
    statistics: Optional[sqlschema.PlayerStatistics]
    entry: sqlschema.LineupPlayerEntry


class PlayerColorResult(TypedDict):
    """Result from player color conversion."""

    player_color: sqlschema.PlayerColor


class TeamLineupResult(TypedDict):
    """Result from team lineup conversion."""

    team_lineup: sqlschema.TeamLineup
    player_color: sqlschema.PlayerColor
    goalkeeper_color: sqlschema.PlayerColor
    player_entries: List[LineupPlayerEntryResult]
    missing_players: List[sqlschema.LineupPlayer]


class FootballLineupResult(TypedDict):
    """Result from complete football lineup conversion."""

    football_lineup: sqlschema.FootballLineup
    home_lineup: TeamLineupResult
    away_lineup: TeamLineupResult
    all_players: List[sqlschema.LineupPlayer]
    all_countries: List[sqlschema.Country]


# Simple Converters
def player_color(color: sofaschema.PlayerColorSchema) -> PlayerColorResult:
    """Convert player color schema to SQLModel."""
    return PlayerColorResult(player_color=sqlschema.PlayerColor(**color.model_dump()))


def player_statistics(
    stats: sofaschema.PlayerStatisticsSchema,
) -> PlayerStatisticsResult:
    """Convert player statistics schema to SQLModel."""
    # Remove ratingVersions as it's not in the SQLModel
    stats_data = stats.model_dump(exclude={"ratingVersions"})
    return PlayerStatisticsResult(statistics=sqlschema.PlayerStatistics(**stats_data))


def lineup_player(player: sofaschema.LineupPlayerSchema) -> LineupPlayerResult:
    """
    Convert lineup player with country relationship.
    """
    # Convert country if present
    country_obj = None
    if player.country:
        country_obj = country(player.country)

    # Prepare player data
    player_data = player.model_dump(
        exclude={"country", "proposedMarketValueRaw", "fieldTranslations"}
    )

    # Handle the marketValue from proposedMarketValueRaw
    if player.proposedMarketValueRaw:
        player_data["marketValue"] = player.proposedMarketValueRaw.value
        player_data["marketValueCurrency_raw"] = player.proposedMarketValueRaw.currency

    player_obj = sqlschema.LineupPlayer(**player_data)

    # Set country relationship if present
    if country_obj:
        player_obj.country = country_obj

    return LineupPlayerResult(player=player_obj, country=country_obj)


def lineup_player_entry(
    entry: sofaschema.LineupPlayerEntrySchema,
    team_lineup: sqlschema.TeamLineup,
    team: Optional[sqlschema.Team] = None,
) -> LineupPlayerEntryResult:
    """
    Convert lineup player entry with all relationships.
    """
    # Convert the player
    player_result = lineup_player(entry.player)
    player_obj = player_result["player"]

    # Convert statistics if present
    stats_obj = None
    if entry.statistics:
        stats_result = player_statistics(entry.statistics)
        stats_obj = stats_result["statistics"]

    # Create the entry
    entry_data = {
        "shirtNumber": entry.shirtNumber,
        "jerseyNumber": entry.jerseyNumber,
        "position": entry.position,
        "substitute": entry.substitute,
        "captain": getattr(entry, "captain", None),
    }

    entry_obj = sqlschema.LineupPlayerEntry(**entry_data)

    # Set relationships
    entry_obj.player = player_obj
    entry_obj.team_lineup = team_lineup
    if team:
        entry_obj.team = team
        entry_obj.team_id = team.id
    if stats_obj:
        entry_obj.statistics = stats_obj

    return LineupPlayerEntryResult(
        player=player_obj,
        player_country=player_result["country"],
        statistics=stats_obj,
        entry=entry_obj,
    )


def missing_player(missing: sofaschema.MissingPlayerSchema) -> sqlschema.LineupPlayer:
    """
    Convert missing player information.
    Note: We only store the player, not the missing reason/type.
    """
    player_result = lineup_player(missing.player)
    return player_result["player"]


def team_lineup(
    lineup: sofaschema.TeamLineupSchema,
    is_home: bool,
    football_lineup: sqlschema.FootballLineup,
    team: Optional[sqlschema.Team] = None,
) -> TeamLineupResult:
    """
    Convert team lineup with all players and colors.
    """
    # Convert colors
    player_color_obj = None
    if lineup.playerColor:
        player_color_result = player_color(lineup.playerColor)
        player_color_obj = player_color_result["player_color"]

    goalkeeper_color_obj = None
    if lineup.goalkeeperColor:
        goalkeeper_color_result = player_color(lineup.goalkeeperColor)
        goalkeeper_color_obj = goalkeeper_color_result["player_color"]

    # Create team lineup
    lineup_data = {"formation": lineup.formation, "is_home": is_home}

    team_lineup_obj = sqlschema.TeamLineup(**lineup_data)

    # Set relationships
    team_lineup_obj.football_lineup = football_lineup
    team_lineup_obj.player_color = player_color_obj
    team_lineup_obj.goalkeeper_color = goalkeeper_color_obj
    if team:
        team_lineup_obj.team = team

    # Convert all player entries
    player_entries = []
    for entry_schema in lineup.players:
        entry_result = lineup_player_entry(entry_schema, team_lineup_obj, team)
        player_entries.append(entry_result)

    # Set the players relationship
    team_lineup_obj.players = [result["entry"] for result in player_entries]

    # Convert missing players
    missing_players = [missing_player(m) for m in lineup.missingPlayers]

    return TeamLineupResult(
        team_lineup=team_lineup_obj,
        player_color=player_color_obj,
        goalkeeper_color=goalkeeper_color_obj,
        player_entries=player_entries,
        missing_players=missing_players,
    )


def football_lineup(
    lineup: sofaschema.FootballLineupSchema,
    event: sqlschema.Event,
    home_team: Optional[sqlschema.Team] = None,
    away_team: Optional[sqlschema.Team] = None,
) -> FootballLineupResult:
    """
    Convert complete football lineup with all teams and players.
    """
    # Create football lineup
    lineup_obj = sqlschema.FootballLineup(confirmed=lineup.confirmed)
    lineup_obj.event = event
    lineup_obj.event_id = event.id

    # Convert home and away lineups
    home_result = team_lineup(lineup.home, True, lineup_obj, home_team)
    away_result = team_lineup(lineup.away, False, lineup_obj, away_team)

    # Set the lineups relationship
    lineup_obj.lineups = [home_result["team_lineup"], away_result["team_lineup"]]

    # Collect all unique players and countries
    all_players = []
    all_countries = []

    # From home team
    for entry_result in home_result["player_entries"]:
        all_players.append(entry_result["player"])
        if entry_result["player_country"]:
            all_countries.append(entry_result["player_country"])
    all_players.extend(home_result["missing_players"])

    # From away team
    for entry_result in away_result["player_entries"]:
        all_players.append(entry_result["player"])
        if entry_result["player_country"]:
            all_countries.append(entry_result["player_country"])
    all_players.extend(away_result["missing_players"])

    return FootballLineupResult(
        football_lineup=lineup_obj,
        home_lineup=home_result,
        away_lineup=away_result,
        all_players=all_players,
        all_countries=all_countries,
    )


# Standalone version without event/team linking
def football_lineup_standalone(
    lineup: sofaschema.FootballLineupSchema,
) -> FootballLineupResult:
    """
    Convert football lineup without linking to event or teams.
    Useful for converting lineups before you have the event/team objects.
    """
    # Create football lineup
    lineup_obj = sqlschema.FootballLineup(confirmed=lineup.confirmed)

    # Convert home and away lineups without team references
    home_result = team_lineup(lineup.home, True, lineup_obj, None)
    away_result = team_lineup(lineup.away, False, lineup_obj, None)

    # Set the lineups relationship
    lineup_obj.lineups = [home_result["team_lineup"], away_result["team_lineup"]]

    # Collect all unique players and countries
    all_players = []
    all_countries = []

    # From home team
    for entry_result in home_result["player_entries"]:
        all_players.append(entry_result["player"])
        if entry_result["player_country"]:
            all_countries.append(entry_result["player_country"])
    all_players.extend(home_result["missing_players"])

    # From away team
    for entry_result in away_result["player_entries"]:
        all_players.append(entry_result["player"])
        if entry_result["player_country"]:
            all_countries.append(entry_result["player_country"])
    all_players.extend(away_result["missing_players"])

    return FootballLineupResult(
        football_lineup=lineup_obj,
        home_lineup=home_result,
        away_lineup=away_result,
        all_players=all_players,
        all_countries=all_countries,
    )
