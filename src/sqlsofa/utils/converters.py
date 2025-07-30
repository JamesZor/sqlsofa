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


def team(team_schema: sofaschema.TeamSchema) -> TeamResult:
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

    return TeamResult(
        sport=sport_obj,
        country=country_obj,
        team_colors=team_colors_obj,
        team=sqlschema.Team(**team_data),
    )


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
def country(country: sofaschema.CountrySchema) -> sqlschema.Country:
    """Convert country schema to SQLModel."""
    return sqlschema.Country(**country.model_dump())


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


########################################
## incidents
########################################
# Result Types
class CoordinatesResult(TypedDict):
    """Result from coordinates conversion."""

    coordinates: sqlschema.Coordinates


class PassingNetworkActionResult(TypedDict):
    """Result from passing network action conversion."""

    player: sqlschema.LineupPlayer
    coordinates: List[sqlschema.Coordinates]


class PeriodIncidentResult(TypedDict):
    """Result from period incident conversion."""

    incident: sqlschema.PeriodIncident


class InjuryTimeIncidentResult(TypedDict):
    """Result from injury time incident conversion."""

    incident: sqlschema.InjuryTimeIncident


class SubstitutionIncidentResult(TypedDict):
    """Result from substitution incident conversion."""

    incident: sqlschema.SubstitutionIncident
    player_in: sqlschema.LineupPlayer
    player_out: sqlschema.LineupPlayer


class CardIncidentResult(TypedDict):
    """Result from card incident conversion."""

    incident: sqlschema.CardIncident
    player: Optional[sqlschema.LineupPlayer]


class GoalIncidentResult(TypedDict):
    """Result from goal incident conversion."""

    incident: sqlschema.GoalIncident
    player: sqlschema.LineupPlayer
    assist1_player: Optional[sqlschema.LineupPlayer]
    assist2_player: Optional[sqlschema.LineupPlayer]
    passing_network: List[PassingNetworkActionResult]


class VarDecisionIncidentResult(TypedDict):
    """Result from VAR decision incident conversion."""

    incident: sqlschema.VarDecisionIncident
    player: Optional[sqlschema.LineupPlayer]


class TeamColorsIncidentResult(TypedDict):
    """Result from team colors conversion."""

    player_color: sqlschema.PlayerColor
    goalkeeper_color: sqlschema.PlayerColor


class FootballIncidentsResult(TypedDict):
    """Result from complete football incidents conversion."""

    incidents: List[sqlschema.Incident]
    period_incidents: List[sqlschema.PeriodIncident]
    injury_time_incidents: List[sqlschema.InjuryTimeIncident]
    substitution_incidents: List[sqlschema.SubstitutionIncident]
    card_incidents: List[sqlschema.CardIncident]
    goal_incidents: List[sqlschema.GoalIncident]
    var_decision_incidents: List[sqlschema.VarDecisionIncident]
    home_colors: TeamColorsIncidentResult
    away_colors: TeamColorsIncidentResult
    all_players: List[sqlschema.LineupPlayer]
    all_coordinates: List[sqlschema.Coordinates]


# Simple Converters
def coordinates(coord: sofaschema.CoordinatesSchema) -> CoordinatesResult:
    """Convert coordinates schema to SQLModel."""
    return CoordinatesResult(coordinates=sqlschema.Coordinates(**coord.model_dump()))


def lineup_player_from_incident(
    player: sofaschema.LineupPlayerSchema,
) -> sqlschema.LineupPlayer:
    """
    Convert lineup player from incident data.
    Similar to lineup converter but handles incident-specific fields.
    """
    # Prepare player data
    player_data = player.model_dump(
        exclude={"country", "proposedMarketValueRaw", "fieldTranslations"}
    )

    # Handle the marketValue from proposedMarketValueRaw
    if player.proposedMarketValueRaw:
        player_data["marketValue"] = player.proposedMarketValueRaw.value
        player_data["marketValueCurrency_raw"] = player.proposedMarketValueRaw.currency

    return sqlschema.LineupPlayer(**player_data)


def team_colors_incident(
    colors: sofaschema.TeamColorsIncidentSchema,
) -> TeamColorsIncidentResult:
    """Convert team colors from incidents."""
    player_color = sqlschema.PlayerColor(**colors.playerColor.model_dump())
    goalkeeper_color = sqlschema.PlayerColor(**colors.goalkeeperColor.model_dump())

    return TeamColorsIncidentResult(
        player_color=player_color, goalkeeper_color=goalkeeper_color
    )


# Incident Type Converters
def period_incident(
    incident: sofaschema.PeriodIncidentSchema, event: sqlschema.Event
) -> PeriodIncidentResult:
    """Convert period incident (HT, FT)."""
    incident_data = incident.model_dump(exclude={"incidentType"})
    incident_obj = sqlschema.PeriodIncident(**incident_data)
    incident_obj.event = event
    incident_obj.event_id = event.id

    return PeriodIncidentResult(incident=incident_obj)


def injury_time_incident(
    incident: sofaschema.InjuryTimeIncidentSchema, event: sqlschema.Event
) -> InjuryTimeIncidentResult:
    """Convert injury time incident."""
    incident_data = incident.model_dump(exclude={"incidentType"})
    incident_obj = sqlschema.InjuryTimeIncident(**incident_data)
    incident_obj.event = event
    incident_obj.event_id = event.id

    return InjuryTimeIncidentResult(incident=incident_obj)


def substitution_incident(
    incident: sofaschema.SubstitutionIncidentSchema, event: sqlschema.Event
) -> SubstitutionIncidentResult:
    """Convert substitution incident."""
    # Convert players
    player_in = lineup_player_from_incident(incident.playerIn)
    player_out = lineup_player_from_incident(incident.playerOut)

    # Create incident
    incident_data = incident.model_dump(
        exclude={"incidentType", "playerIn", "playerOut"}
    )
    incident_obj = sqlschema.SubstitutionIncident(**incident_data)

    # Set relationships
    incident_obj.event = event
    incident_obj.event_id = event.id
    incident_obj.player_in = player_in
    incident_obj.player_out = player_out

    return SubstitutionIncidentResult(
        incident=incident_obj, player_in=player_in, player_out=player_out
    )


def card_incident(
    incident: sofaschema.CardIncidentSchema, event: sqlschema.Event
) -> CardIncidentResult:
    """Convert card incident."""
    # Convert player if present
    player_obj = None
    if incident.player:
        player_obj = lineup_player_from_incident(incident.player)

    # Create incident
    incident_data = incident.model_dump(exclude={"incidentType", "player"})
    incident_obj = sqlschema.CardIncident(**incident_data)

    # Set relationships
    incident_obj.event = event
    incident_obj.event_id = event.id
    if player_obj:
        incident_obj.player = player_obj

    return CardIncidentResult(incident=incident_obj, player=player_obj)


def passing_network_action(
    action: sofaschema.PassingNetworkActionSchema,
) -> PassingNetworkActionResult:
    """Convert passing network action from goal incident."""
    # Convert player
    player = lineup_player_from_incident(action.player)

    # Convert all coordinates
    coords = []
    if action.playerCoordinates:
        coords.append(sqlschema.Coordinates(**action.playerCoordinates.model_dump()))
    if action.passEndCoordinates:
        coords.append(sqlschema.Coordinates(**action.passEndCoordinates.model_dump()))
    if action.gkCoordinates:
        coords.append(sqlschema.Coordinates(**action.gkCoordinates.model_dump()))
    if action.goalShotCoordinates:
        coords.append(sqlschema.Coordinates(**action.goalShotCoordinates.model_dump()))
    if action.goalMouthCoordinates:
        coords.append(sqlschema.Coordinates(**action.goalMouthCoordinates.model_dump()))

    return PassingNetworkActionResult(player=player, coordinates=coords)


def goal_incident(
    incident: sofaschema.GoalIncidentSchema, event: sqlschema.Event
) -> GoalIncidentResult:
    """Convert goal incident with passing network."""
    # Convert main player
    player = lineup_player_from_incident(incident.player)

    # Convert assist players if present
    assist1_player = None
    if incident.assist1:
        assist1_player = lineup_player_from_incident(incident.assist1)

    assist2_player = None
    if incident.assist2:
        assist2_player = lineup_player_from_incident(incident.assist2)

    # Convert passing network if present
    passing_network = []
    if incident.footballPassingNetworkAction:
        for action in incident.footballPassingNetworkAction:
            passing_network.append(passing_network_action(action))

    # Create incident
    incident_data = incident.model_dump(
        exclude={
            "incidentType",
            "player",
            "assist1",
            "assist2",
            "footballPassingNetworkAction",
        }
    )
    incident_obj = sqlschema.GoalIncident(**incident_data)

    # Set relationships
    incident_obj.event = event
    incident_obj.event_id = event.id
    incident_obj.player = player
    if assist1_player:
        incident_obj.assist1_player = assist1_player
    if assist2_player:
        incident_obj.assist2_player = assist2_player

    return GoalIncidentResult(
        incident=incident_obj,
        player=player,
        assist1_player=assist1_player,
        assist2_player=assist2_player,
        passing_network=passing_network,
    )


def var_decision_incident(
    incident: sofaschema.VarDecisionIncidentSchema, event: sqlschema.Event
) -> VarDecisionIncidentResult:
    """Convert VAR decision incident."""
    # Convert player if present
    player_obj = None
    if incident.player:
        player_obj = lineup_player_from_incident(incident.player)

    # Create incident
    incident_data = incident.model_dump(exclude={"incidentType", "player"})
    incident_obj = sqlschema.VarDecisionIncident(**incident_data)

    # Set relationships
    incident_obj.event = event
    incident_obj.event_id = event.id
    if player_obj:
        incident_obj.player = player_obj

    return VarDecisionIncidentResult(incident=incident_obj, player=player_obj)


def process_incident(
    incident: Union[
        sofaschema.PeriodIncidentSchema,
        sofaschema.InjuryTimeIncidentSchema,
        sofaschema.SubstitutionIncidentSchema,
        sofaschema.CardIncidentSchema,
        sofaschema.GoalIncidentSchema,
        sofaschema.VarDecisionIncidentSchema,
    ],
    event: sqlschema.Event,
) -> Union[
    PeriodIncidentResult,
    InjuryTimeIncidentResult,
    SubstitutionIncidentResult,
    CardIncidentResult,
    GoalIncidentResult,
    VarDecisionIncidentResult,
]:
    """Process a single incident based on its type."""
    if isinstance(incident, sofaschema.PeriodIncidentSchema):
        return period_incident(incident, event)
    elif isinstance(incident, sofaschema.InjuryTimeIncidentSchema):
        return injury_time_incident(incident, event)
    elif isinstance(incident, sofaschema.SubstitutionIncidentSchema):
        return substitution_incident(incident, event)
    elif isinstance(incident, sofaschema.CardIncidentSchema):
        return card_incident(incident, event)
    elif isinstance(incident, sofaschema.GoalIncidentSchema):
        return goal_incident(incident, event)
    elif isinstance(incident, sofaschema.VarDecisionIncidentSchema):
        return var_decision_incident(incident, event)
    else:
        raise ValueError(f"Unknown incident type: {type(incident)}")


def football_incidents(
    incidents: sofaschema.FootballIncidentsSchema, event: sqlschema.Event
) -> FootballIncidentsResult:
    """
    Convert complete football incidents with all types.
    """
    # Convert team colors
    home_colors = team_colors_incident(incidents.home)
    away_colors = team_colors_incident(incidents.away)

    # Process all incidents
    all_incidents = []
    period_incidents = []
    injury_time_incidents = []
    substitution_incidents = []
    card_incidents = []
    goal_incidents = []
    var_decision_incidents = []
    all_players = []
    all_coordinates = []

    for incident_schema in incidents.incidents:
        result = process_incident(incident_schema, event)
        result_type = type(result)

        # Add to appropriate lists based on type
        if result_type == PeriodIncidentResult:
            period_incidents.append(result["incident"])
            all_incidents.append(result["incident"])
        elif result_type == InjuryTimeIncidentResult:
            injury_time_incidents.append(result["incident"])
            all_incidents.append(result["incident"])
        elif result_type == SubstitutionIncidentResult:
            substitution_incidents.append(result["incident"])
            all_incidents.append(result["incident"])
            all_players.extend([result["player_in"], result["player_out"]])
        elif result_type == CardIncidentResult:
            card_incidents.append(result["incident"])
            all_incidents.append(result["incident"])
            if result["player"]:
                all_players.append(result["player"])
        elif result_type == GoalIncidentResult:
            goal_incidents.append(result["incident"])
            all_incidents.append(result["incident"])
            all_players.append(result["player"])
            if result["assist1_player"]:
                all_players.append(result["assist1_player"])
            if result["assist2_player"]:
                all_players.append(result["assist2_player"])
            # Collect players and coordinates from passing network
            for action in result["passing_network"]:
                all_players.append(action["player"])
                all_coordinates.extend(action["coordinates"])
        elif result_type == VarDecisionIncidentResult:
            var_decision_incidents.append(result["incident"])
            all_incidents.append(result["incident"])
            if result["player"]:
                all_players.append(result["player"])

    # Create generic Incident objects for the main relationship
    generic_incidents = []
    for inc in all_incidents:
        generic_inc = sqlschema.Incident(
            incidentType=type(inc).__name__.replace("Incident", "").lower(),
            time=getattr(inc, "time", None),
            addedTime=getattr(inc, "addedTime", None),
            isHome=getattr(inc, "isHome", None),
            event=event,
            event_id=event.id,
        )
        generic_incidents.append(generic_inc)

    return FootballIncidentsResult(
        incidents=generic_incidents,
        period_incidents=period_incidents,
        injury_time_incidents=injury_time_incidents,
        substitution_incidents=substitution_incidents,
        card_incidents=card_incidents,
        goal_incidents=goal_incidents,
        var_decision_incidents=var_decision_incidents,
        home_colors=home_colors,
        away_colors=away_colors,
        all_players=all_players,
        all_coordinates=all_coordinates,
    )


# Standalone version without event linking
def football_incidents_standalone(
    incidents: sofaschema.FootballIncidentsSchema,
) -> FootballIncidentsResult:
    """
    Convert football incidents without linking to event.
    Useful for converting incidents before you have the event object.
    """
    # Create a dummy event for now (will be replaced later)
    dummy_event = sqlschema.Event(id=0, slug="temp", startTimestamp=0)

    # Use the main converter
    result = football_incidents(incidents, dummy_event)

    # Clear the event references
    for inc in result["incidents"]:
        inc.event = None
        inc.event_id = None
    for inc in result["period_incidents"]:
        inc.event = None
        inc.event_id = None
    for inc in result["injury_time_incidents"]:
        inc.event = None
        inc.event_id = None
    for inc in result["substitution_incidents"]:
        inc.event = None
        inc.event_id = None
    for inc in result["card_incidents"]:
        inc.event = None
        inc.event_id = None
    for inc in result["goal_incidents"]:
        inc.event = None
        inc.event_id = None
    for inc in result["var_decision_incidents"]:
        inc.event = None
        inc.event_id = None

    return result
