from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

##############################
# Base/Core Entities
##############################


class Sport(SQLModel, table=True):  # type: ignore
    __tablename__ = "sports"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    categories: List["Category"] = Relationship(back_populates="sport")
    teams: List["Team"] = Relationship(back_populates="sport")
    referees: List["Referee"] = Relationship(back_populates="sport")


class Country(SQLModel, table=True):  # type: ignore
    __tablename__ = "countries"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    slug: str = Field(unique=True)
    alpha2: str = Field(max_length=2)
    alpha3: str = Field(max_length=3, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    venues: List["Venue"] = Relationship(back_populates="country")
    teams: List["Team"] = Relationship(back_populates="country")
    managers: List["Manager"] = Relationship(back_populates="country")
    referees: List["Referee"] = Relationship(back_populates="country")
    players: List["LineupPlayer"] = Relationship(back_populates="country")


class Category(SQLModel, table=True):  # type: ignore
    __tablename__ = "categories"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    sport_id: Optional[int] = Field(default=None, foreign_key="sports.id")

    # Relationships
    sport: Optional[Sport] = Relationship(back_populates="categories")
    tournaments: List["Tournament"] = Relationship(back_populates="category")


class Tournament(SQLModel, table=True):  # type: ignore
    __tablename__ = "tournaments"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    competitionType: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")

    # Relationships
    category: Optional[Category] = Relationship(back_populates="tournaments")
    events: List["Event"] = Relationship(back_populates="tournament")


class Season(SQLModel, table=True):  # type: ignore
    __tablename__ = "seasons"

    id: int = Field(primary_key=True)
    name: str
    year: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    events: List["Event"] = Relationship(back_populates="season")


##############################
# Location/Venue Entities
##############################


class City(SQLModel, table=True):  # type: ignore
    __tablename__ = "cities"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    venues: List["Venue"] = Relationship(back_populates="city")


class Stadium(SQLModel, table=True):  # type: ignore
    __tablename__ = "stadiums"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    capacity: int
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    venues: List["Venue"] = Relationship(back_populates="stadium")


class VenueCoordinates(SQLModel, table=True):  # type: ignore
    __tablename__ = "venue_coordinates"

    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    venues: List["Venue"] = Relationship(back_populates="venue_coordinates")


class Venue(SQLModel, table=True):  # type: ignore
    __tablename__ = "venues"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    capacity: int
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    city_id: Optional[int] = Field(default=None, foreign_key="cities.id")
    country_id: Optional[int] = Field(default=None, foreign_key="countries.id")
    stadium_id: Optional[int] = Field(default=None, foreign_key="stadiums.id")
    venue_coordinates_id: Optional[int] = Field(
        default=None, foreign_key="venue_coordinates.id"
    )

    # Relationships
    city: Optional[City] = Relationship(back_populates="venues")
    country: Optional[Country] = Relationship(back_populates="venues")
    stadium: Optional[Stadium] = Relationship(back_populates="venues")
    venue_coordinates: Optional[VenueCoordinates] = Relationship(
        back_populates="venues"
    )
    teams: List["Team"] = Relationship(back_populates="venue")
    events: List["Event"] = Relationship(back_populates="venue")


##############################
# Team/Player Entities
##############################


class TeamColors(SQLModel, table=True):  # type: ignore
    __tablename__ = "team_colors"

    id: Optional[int] = Field(default=None, primary_key=True)
    primary: str
    secondary: str
    text: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    teams: List["Team"] = Relationship(back_populates="team_colors")


class Manager(SQLModel, table=True):  # type: ignore
    __tablename__ = "managers"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    shortName: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    country_id: Optional[int] = Field(default=None, foreign_key="countries.id")

    # Relationships
    country: Optional[Country] = Relationship(back_populates="managers")
    teams: List["Team"] = Relationship(back_populates="manager")


class Team(SQLModel, table=True):  # type: ignore
    __tablename__ = "teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    slug: str = Field(unique=True)
    shortName: str
    nameCode: str = Field(max_length=3)
    gender: str = Field(max_length=1)
    fullName: Optional[str] = None
    class_: Optional[int] = Field(None, alias="class")
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    sport_id: Optional[int] = Field(default=None, foreign_key="sports.id")
    country_id: Optional[int] = Field(default=None, foreign_key="countries.id")
    team_colors_id: Optional[int] = Field(default=None, foreign_key="team_colors.id")
    manager_id: Optional[int] = Field(default=None, foreign_key="managers.id")
    venue_id: Optional[int] = Field(default=None, foreign_key="venues.id")

    # Relationships
    sport: Optional[Sport] = Relationship(back_populates="teams")
    country: Optional[Country] = Relationship(back_populates="teams")
    team_colors: Optional[TeamColors] = Relationship(back_populates="teams")
    manager: Optional[Manager] = Relationship(back_populates="teams")
    venue: Optional[Venue] = Relationship(back_populates="teams")
    home_events: List["Event"] = Relationship(
        back_populates="home_team",
        sa_relationship_kwargs={"foreign_keys": "[Event.home_team_id]"},
    )
    away_events: List["Event"] = Relationship(
        back_populates="away_team",
        sa_relationship_kwargs={"foreign_keys": "[Event.away_team_id]"},
    )
    team_lineups: List["TeamLineup"] = Relationship(back_populates="team")


class LineupPlayer(SQLModel, table=True):  # type: ignore
    __tablename__ = "lineup_players"

    id: int = Field(primary_key=True)
    name: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    slug: Optional[str] = None
    shortName: Optional[str] = None
    position: Optional[str] = None
    jerseyNumber: Optional[str] = None
    height: Optional[int] = None
    userCount: Optional[int] = None
    sofascoreId: Optional[str] = None
    marketValueCurrency: Optional[str] = None
    dateOfBirthTimestamp: Optional[int] = None
    marketValue: Optional[int] = None
    marketValueCurrency_raw: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    country_id: Optional[int] = Field(default=None, foreign_key="countries.id")

    # Relationships
    country: Optional[Country] = Relationship(back_populates="players")
    lineup_entries: List["LineupPlayerEntry"] = Relationship(back_populates="player")
    goal_incidents: List["GoalIncident"] = Relationship(
        back_populates="player",
        sa_relationship_kwargs={"foreign_keys": "[GoalIncident.player_id]"},
    )
    assist1_incidents: List["GoalIncident"] = Relationship(
        back_populates="assist1_player",
        sa_relationship_kwargs={"foreign_keys": "[GoalIncident.assist1_player_id]"},
    )
    assist2_incidents: List["GoalIncident"] = Relationship(
        back_populates="assist2_player",
        sa_relationship_kwargs={"foreign_keys": "[GoalIncident.assist2_player_id]"},
    )
    card_incidents: List["CardIncident"] = Relationship(back_populates="player")
    substitution_in_incidents: List["SubstitutionIncident"] = Relationship(
        back_populates="player_in",
        sa_relationship_kwargs={"foreign_keys": "[SubstitutionIncident.player_in_id]"},
    )
    substitution_out_incidents: List["SubstitutionIncident"] = Relationship(
        back_populates="player_out",
        sa_relationship_kwargs={"foreign_keys": "[SubstitutionIncident.player_out_id]"},
    )


##############################
# Match/Event Core Entities
##############################


class Status(SQLModel, table=True):  # type: ignore
    __tablename__ = "statuses"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: int = Field(unique=True)
    description: str
    type: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    events: List["Event"] = Relationship(back_populates="status")


class TimeFootball(SQLModel, table=True):  # type: ignore
    __tablename__ = "time_football"

    id: Optional[int] = Field(default=None, primary_key=True)
    injuryTime1: int = 0
    injuryTime2: int = 0
    currentPeriodStartTimestamp: int
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    events: List["Event"] = Relationship(back_populates="time")


class Score(SQLModel, table=True):  # type: ignore
    __tablename__ = "scores"

    id: Optional[int] = Field(default=None, primary_key=True)
    current: int = 0
    display: int = 0
    period1: int = 0
    period2: int = 0
    normaltime: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    home_events: List["Event"] = Relationship(
        back_populates="home_score",
        sa_relationship_kwargs={"foreign_keys": "[Event.home_score_id]"},
    )
    away_events: List["Event"] = Relationship(
        back_populates="away_score",
        sa_relationship_kwargs={"foreign_keys": "[Event.away_score_id]"},
    )


class RoundInfo(SQLModel, table=True):  # type: ignore
    __tablename__ = "round_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    round: int
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    events: List["Event"] = Relationship(back_populates="round_info")


class Referee(SQLModel, table=True):  # type: ignore
    __tablename__ = "referees"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    yellowCards: int = 0
    redCards: int = 0
    yellowRedCards: int = 0
    games: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    sport_id: Optional[int] = Field(default=None, foreign_key="sports.id")
    country_id: Optional[int] = Field(default=None, foreign_key="countries.id")

    # Relationships
    sport: Optional[Sport] = Relationship(back_populates="referees")
    country: Optional[Country] = Relationship(back_populates="referees")
    events: List["Event"] = Relationship(back_populates="referee")


##############################
# Main Event Entity
##############################


class Event(SQLModel, table=True):  # type: ignore
    __tablename__ = "events"

    id: int = Field(primary_key=True)
    slug: str = Field(unique=True)
    startTimestamp: int
    winnerCode: Optional[int] = None
    hasGlobalHighlights: bool = False
    hasXg: bool = False
    hasEventPlayerStatistics: bool = False
    hasEventPlayerHeatMap: bool = False
    attendance: Optional[int] = None
    defaultPeriodCount: Optional[int] = None
    defaultPeriodLength: Optional[int] = None
    defaultOvertimeLength: Optional[int] = None
    currentPeriodStartTimestamp: Optional[int] = None
    fanRatingEvent: Optional[bool] = None
    seasonStatisticsType: Optional[str] = None
    showTotoPromo: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    status_id: Optional[int] = Field(default=None, foreign_key="statuses.id")
    time_id: Optional[int] = Field(default=None, foreign_key="time_football.id")
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournaments.id")
    season_id: Optional[int] = Field(default=None, foreign_key="seasons.id")
    round_info_id: Optional[int] = Field(default=None, foreign_key="round_info.id")
    home_score_id: Optional[int] = Field(default=None, foreign_key="scores.id")
    away_score_id: Optional[int] = Field(default=None, foreign_key="scores.id")
    home_team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    away_team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    venue_id: Optional[int] = Field(default=None, foreign_key="venues.id")
    referee_id: Optional[int] = Field(default=None, foreign_key="referees.id")

    # Relationships
    status: Optional[Status] = Relationship(back_populates="events")
    time: Optional[TimeFootball] = Relationship(back_populates="events")
    tournament: Optional[Tournament] = Relationship(back_populates="events")
    season: Optional[Season] = Relationship(back_populates="events")
    round_info: Optional[RoundInfo] = Relationship(back_populates="events")
    home_score: Optional[Score] = Relationship(
        back_populates="home_events",
        sa_relationship_kwargs={"foreign_keys": "[Event.home_score_id]"},
    )
    away_score: Optional[Score] = Relationship(
        back_populates="away_events",
        sa_relationship_kwargs={"foreign_keys": "[Event.away_score_id]"},
    )
    home_team: Optional[Team] = Relationship(
        back_populates="home_events",
        sa_relationship_kwargs={"foreign_keys": "[Event.home_team_id]"},
    )
    away_team: Optional[Team] = Relationship(
        back_populates="away_events",
        sa_relationship_kwargs={"foreign_keys": "[Event.away_team_id]"},
    )
    venue: Optional[Venue] = Relationship(back_populates="events")
    referee: Optional[Referee] = Relationship(back_populates="events")

    # Component relationships
    football_lineups: List["FootballLineup"] = Relationship(back_populates="event")
    football_stats: List["FootballStatisticPeriod"] = Relationship(
        back_populates="event"
    )
    incidents: List["Incident"] = Relationship(back_populates="event")
    graph_points: List["GraphPoint"] = Relationship(back_populates="event")


##############################
# Lineup Component Entities
##############################


class PlayerStatistics(SQLModel, table=True):  # type: ignore
    __tablename__ = "player_statistics"

    id: Optional[int] = Field(default=None, primary_key=True)
    # Passing stats
    totalPass: Optional[int] = None
    accuratePass: Optional[int] = None
    totalLongBalls: Optional[int] = None
    accurateLongBalls: Optional[int] = None
    goalAssist: Optional[int] = None
    totalCross: Optional[int] = None
    accurateCross: Optional[int] = None
    keyPass: Optional[int] = None

    # Defending stats
    aerialLost: Optional[int] = None
    aerialWon: Optional[int] = None
    duelLost: Optional[int] = None
    duelWon: Optional[int] = None
    challengeLost: Optional[int] = None
    totalContest: Optional[int] = None
    wonContest: Optional[int] = None
    totalClearance: Optional[int] = None
    outfielderBlock: Optional[int] = None
    interceptionWon: Optional[int] = None
    totalTackle: Optional[int] = None

    # General stats
    wasFouled: Optional[int] = None
    fouls: Optional[int] = None
    totalOffside: Optional[int] = None
    minutesPlayed: Optional[int] = None
    touches: Optional[int] = None
    rating: Optional[float] = None
    dispossessed: Optional[int] = None
    possessionLostCtrl: Optional[int] = None

    # Advanced stats
    expectedGoals: Optional[float] = None
    expectedAssists: Optional[float] = None

    # Goalkeeper stats
    goodHighClaim: Optional[int] = None
    savedShotsFromInsideTheBox: Optional[int] = None
    saves: Optional[int] = None
    totalKeeperSweeper: Optional[int] = None
    accurateKeeperSweeper: Optional[int] = None
    goalsPrevented: Optional[float] = None
    errorLeadToAShot: Optional[int] = None
    punches: Optional[int] = None

    # Attacking stats
    bigChanceCreated: Optional[int] = None
    bigChanceMissed: Optional[int] = None
    shotOffTarget: Optional[int] = None
    onTargetScoringAttempt: Optional[int] = None
    blockedScoringAttempt: Optional[int] = None
    goals: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    lineup_entries: List["LineupPlayerEntry"] = Relationship(
        back_populates="statistics"
    )


class LineupPlayerEntry(SQLModel, table=True):  # type: ignore
    __tablename__ = "lineup_player_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    shirtNumber: Optional[int] = None
    jerseyNumber: Optional[str] = None
    position: Optional[str] = None
    substitute: bool = False
    captain: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    player_id: Optional[int] = Field(default=None, foreign_key="lineup_players.id")
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    statistics_id: Optional[int] = Field(
        default=None, foreign_key="player_statistics.id"
    )
    team_lineup_id: Optional[int] = Field(default=None, foreign_key="team_lineups.id")

    # Relationships
    player: Optional[LineupPlayer] = Relationship(back_populates="lineup_entries")
    team: Optional[Team] = Relationship()
    statistics: Optional[PlayerStatistics] = Relationship(
        back_populates="lineup_entries"
    )
    team_lineup: Optional["TeamLineup"] = Relationship(back_populates="players")


class PlayerColor(SQLModel, table=True):  # type: ignore
    __tablename__ = "player_colors"

    id: Optional[int] = Field(default=None, primary_key=True)
    primary: Optional[str] = None
    number: Optional[str] = None
    outline: Optional[str] = None
    fancyNumber: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    team_lineups_player: List["TeamLineup"] = Relationship(
        back_populates="player_color",
        sa_relationship_kwargs={"foreign_keys": "[TeamLineup.player_color_id]"},
    )
    team_lineups_goalkeeper: List["TeamLineup"] = Relationship(
        back_populates="goalkeeper_color",
        sa_relationship_kwargs={"foreign_keys": "[TeamLineup.goalkeeper_color_id]"},
    )


class TeamLineup(SQLModel, table=True):  # type: ignore
    __tablename__ = "team_lineups"

    id: Optional[int] = Field(default=None, primary_key=True)
    formation: Optional[str] = None
    is_home: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    player_color_id: Optional[int] = Field(default=None, foreign_key="player_colors.id")
    goalkeeper_color_id: Optional[int] = Field(
        default=None, foreign_key="player_colors.id"
    )
    football_lineup_id: Optional[int] = Field(
        default=None, foreign_key="football_lineups.id"
    )

    # Relationships
    team: Optional[Team] = Relationship(back_populates="team_lineups")
    player_color: Optional[PlayerColor] = Relationship(
        back_populates="team_lineups_player",
        sa_relationship_kwargs={"foreign_keys": "[TeamLineup.player_color_id]"},
    )
    goalkeeper_color: Optional[PlayerColor] = Relationship(
        back_populates="team_lineups_goalkeeper",
        sa_relationship_kwargs={"foreign_keys": "[TeamLineup.goalkeeper_color_id]"},
    )
    football_lineup: Optional["FootballLineup"] = Relationship(back_populates="lineups")
    players: List[LineupPlayerEntry] = Relationship(back_populates="team_lineup")


class FootballLineup(SQLModel, table=True):  # type: ignore
    __tablename__ = "football_lineups"

    id: Optional[int] = Field(default=None, primary_key=True)
    confirmed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")

    # Relationships
    event: Optional[Event] = Relationship(back_populates="football_lineups")
    lineups: List[TeamLineup] = Relationship(back_populates="football_lineup")


##############################
# Statistics Component Entities
##############################


class FootballStatisticItem(SQLModel, table=True):  # type: ignore
    __tablename__ = "football_statistic_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    name: str
    home: str
    away: str
    compareCode: int
    statisticsType: str  # "positive", "negative"
    valueType: str  # "event", "team"
    homeValue: float
    awayValue: float
    renderType: int
    homeTotal: Optional[int] = None
    awayTotal: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    statistic_group_id: Optional[int] = Field(
        default=None, foreign_key="statistic_groups.id"
    )

    # Relationships
    statistic_group: Optional["StatisticGroup"] = Relationship(
        back_populates="statistics_items"
    )


class StatisticGroup(SQLModel, table=True):  # type: ignore
    __tablename__ = "statistic_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    groupName: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    statistic_period_id: Optional[int] = Field(
        default=None, foreign_key="football_statistic_periods.id"
    )

    # Relationships
    statistic_period: Optional["FootballStatisticPeriod"] = Relationship(
        back_populates="groups"
    )
    statistics_items: List[FootballStatisticItem] = Relationship(
        back_populates="statistic_group"
    )


class FootballStatisticPeriod(SQLModel, table=True):  # type: ignore
    __tablename__ = "football_statistic_periods"

    id: Optional[int] = Field(default=None, primary_key=True)
    period: str  # "ALL", "1ST", "2ND"
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")

    # Relationships
    event: Optional[Event] = Relationship(back_populates="football_stats")
    groups: List[StatisticGroup] = Relationship(back_populates="statistic_period")


##############################
# Incident Component Entities
##############################


class Coordinates(SQLModel, table=True):  # type: ignore
    __tablename__ = "coordinates"

    id: Optional[int] = Field(default=None, primary_key=True)
    x: float
    y: float
    created_at: datetime = Field(default_factory=datetime.now)


class Incident(SQLModel, table=True):  # type: ignore
    __tablename__ = "incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    incidentType: str
    time: Optional[int] = None
    addedTime: Optional[int] = None
    reversedPeriodTime: Optional[int] = None
    reversedPeriodTimeSeconds: Optional[int] = None
    timeSeconds: Optional[int] = None
    periodTimeSeconds: Optional[int] = None
    isHome: Optional[bool] = None
    isLive: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")

    # Relationships
    event: Optional[Event] = Relationship(back_populates="incidents")


# Specific incident types (inheriting from Incident concept)
class GoalIncident(SQLModel, table=True):  # type: ignore
    __tablename__ = "goal_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    homeScore: int
    awayScore: int
    incidentClass: str
    time: int
    reversedPeriodTime: int
    isHome: bool
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")
    player_id: Optional[int] = Field(default=None, foreign_key="lineup_players.id")
    assist1_player_id: Optional[int] = Field(
        default=None, foreign_key="lineup_players.id"
    )
    assist2_player_id: Optional[int] = Field(
        default=None, foreign_key="lineup_players.id"
    )

    # Relationships
    event: Optional[Event] = Relationship()
    player: Optional[LineupPlayer] = Relationship(
        back_populates="goal_incidents",
        sa_relationship_kwargs={"foreign_keys": "[GoalIncident.player_id]"},
    )
    assist1_player: Optional[LineupPlayer] = Relationship(
        back_populates="assist1_incidents",
        sa_relationship_kwargs={"foreign_keys": "[GoalIncident.assist1_player_id]"},
    )
    assist2_player: Optional[LineupPlayer] = Relationship(
        back_populates="assist2_incidents",
        sa_relationship_kwargs={"foreign_keys": "[GoalIncident.assist2_player_id]"},
    )


class CardIncident(SQLModel, table=True):  # type: ignore
    __tablename__ = "card_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    incidentClass: Optional[str] = None  # "yellow", "red"
    playerName: Optional[str] = None
    reason: Optional[str] = None
    rescinded: Optional[bool] = None
    time: Optional[int] = None
    reversedPeriodTime: Optional[int] = None
    isHome: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")
    player_id: Optional[int] = Field(default=None, foreign_key="lineup_players.id")

    # Relationships
    event: Optional[Event] = Relationship()
    player: Optional[LineupPlayer] = Relationship(back_populates="card_incidents")


class SubstitutionIncident(SQLModel, table=True):  # type: ignore
    __tablename__ = "substitution_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    incidentClass: str
    time: int
    addedTime: Optional[int] = None
    injury: bool
    isHome: bool
    reversedPeriodTime: int
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")
    player_in_id: Optional[int] = Field(default=None, foreign_key="lineup_players.id")
    player_out_id: Optional[int] = Field(default=None, foreign_key="lineup_players.id")

    # Relationships
    event: Optional[Event] = Relationship()
    player_in: Optional[LineupPlayer] = Relationship(
        back_populates="substitution_in_incidents",
        sa_relationship_kwargs={"foreign_keys": "[SubstitutionIncident.player_in_id]"},
    )
    player_out: Optional[LineupPlayer] = Relationship(
        back_populates="substitution_out_incidents",
        sa_relationship_kwargs={"foreign_keys": "[SubstitutionIncident.player_out_id]"},
    )


class PeriodIncident(SQLModel, table=True):  # type: ignore
    __tablename__ = "period_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str  # "HT", "FT"
    homeScore: int
    awayScore: int
    isLive: bool
    time: int
    addedTime: int
    timeSeconds: int
    reversedPeriodTime: int
    reversedPeriodTimeSeconds: int
    periodTimeSeconds: int
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")

    # Relationships
    event: Optional[Event] = Relationship()


class InjuryTimeIncident(SQLModel, table=True):  # type: ignore
    __tablename__ = "injury_time_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    length: int
    time: int
    addedTime: int
    reversedPeriodTime: int
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")

    # Relationships
    event: Optional[Event] = Relationship()


class VarDecisionIncident(SQLModel, table=True):  # type: ignore
    __tablename__ = "var_decision_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    confirmed: Optional[bool] = None
    decision: Optional[str] = None
    reason: Optional[str] = None
    time: Optional[int] = None
    isHome: Optional[bool] = None
    incidentClass: Optional[str] = None
    reversedPeriodTime: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")
    player_id: Optional[int] = Field(default=None, foreign_key="lineup_players.id")

    # Relationships
    event: Optional[Event] = Relationship()
    player: Optional[LineupPlayer] = Relationship()


##############################
# Graph Component Entities
##############################


class GraphPoint(SQLModel, table=True):  # type: ignore
    __tablename__ = "graph_points"

    id: Optional[int] = Field(default=None, primary_key=True)
    minute: float  # Can be decimal like 45.5, 90.5 for added time
    value: int  # Momentum value (positive favors home, negative favors away)
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")

    # Relationships
    event: Optional[Event] = Relationship(back_populates="graph_points")


##############################
# Match Result/Scraping Entities
##############################


class ComponentStatusEnum(str, Enum):  # type: ignore
    SUCCESS = "success"
    FAILED = "failed"
    NOT_ATTEMPTED = "not_attempted"


class ComponentError(SQLModel, table=True):  # type: ignore
    __tablename__ = "component_errors"

    id: Optional[int] = Field(default=None, primary_key=True)
    component: str
    status: ComponentStatusEnum
    error_message: Optional[str] = None
    attempted_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    match_result_id: Optional[int] = Field(
        default=None, foreign_key="match_scraping_results.id"
    )

    # Relationships
    match_result: Optional["MatchScrapingResult"] = Relationship(
        back_populates="component_errors"
    )


class MatchScrapingResult(SQLModel, table=True):  # type: ignore
    __tablename__ = "match_scraping_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int
    scraped_at: datetime = Field(default_factory=datetime.now)
    success_rate: str
    has_base_data: bool = False
    scraping_duration: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    event_id: Optional[int] = Field(default=None, foreign_key="events.id")
    season_scraping_result_id: Optional[int] = Field(
        default=None, foreign_key="season_scraping_results.id"
    )

    # Relationships
    event: Optional[Event] = Relationship()
    component_errors: List[ComponentError] = Relationship(back_populates="match_result")
    season_scraping_result: Optional["SeasonScrapingResult"] = Relationship(
        back_populates="match_results"
    )


class SeasonScrapingResult(SQLModel, table=True):  # type: ignore
    __tablename__ = "season_scraping_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    tournament_id: int
    season_id: int
    total_matches: int
    successful_matches: int
    failed_matches: int
    scraping_duration: float
    success_rate_percent: float
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    tournament_id_fk: Optional[int] = Field(default=None, foreign_key="tournaments.id")
    season_id_fk: Optional[int] = Field(default=None, foreign_key="seasons.id")

    # Relationships
    tournament: Optional[Tournament] = Relationship()
    season: Optional[Season] = Relationship()
    match_results: List[MatchScrapingResult] = Relationship(
        back_populates="season_scraping_result"
    )


# Create all tables function
def create_all_tables(engine):
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)
