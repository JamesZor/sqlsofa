# sqlsofa/converters/base_converter.py

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from sofascrape.schemas import general as sofaschema

from sqlsofa.schema import sqlmodels as sqlschema

logger = logging.getLogger(__name__)


@dataclass
class ConversionResult:
    """Result container for all converted entities"""

    # Core entities
    sports: Set[sqlschema.Sport] = field(default_factory=set)
    categories: Set[sqlschema.Category] = field(default_factory=set)
    tournaments: Set[sqlschema.Tournament] = field(default_factory=set)
    seasons: Set[sqlschema.Season] = field(default_factory=set)
    events: Set[sqlschema.Event] = field(default_factory=set)

    # Teams and related
    teams: Set[sqlschema.Team] = field(default_factory=set)
    team_colors: Set[sqlschema.TeamColors] = field(default_factory=set)
    countries: Set[sqlschema.Country] = field(default_factory=set)
    venues: Set[sqlschema.Venue] = field(default_factory=set)

    # Match components (lists because order might matter)
    statistic_periods: List[sqlschema.FootballStatisticPeriod] = field(
        default_factory=list
    )
    lineups: List[sqlschema.FootballLineup] = field(default_factory=list)
    incidents: List[sqlschema.Incident] = field(default_factory=list)
    graph_points: List[sqlschema.GraphPoint] = field(default_factory=list)

    # Metadata
    match_id: int = 0
    processed_components: Dict[str, bool] = field(default_factory=dict)


class BaseConverter(ABC):
    """Abstract base class for all converters"""

    def __init__(self, match_data: sofaschema.FootballMatchResultDetailed):
        self.match_data = match_data
        self.entity_map = self._initialize_entity_map()
        self.normalized_entities = self._initialize_normalized_entities()

    @abstractmethod
    def _initialize_entity_map(self) -> Dict[str, Any]:
        """Initialize the entity map structure"""
        pass

    def _initialize_normalized_entities(self) -> Dict[str, Any]:
        """Initialize collections for normalized entities"""
        return {
            "sports": set(),
            "categories": set(),
            "tournaments": set(),
            "seasons": set(),
            "events": set(),
            "teams": set(),
            "team_colors": set(),
            "countries": set(),
            "venues": set(),
            "cities": set(),
            "stadiums": set(),
            "venue_coordinates": set(),
            "referees": set(),
            "managers": set(),
            "players": set(),
            "statistic_periods": [],
            "statistic_groups": [],
            "statistic_items": [],
            "lineups": [],
            "team_lineups": [],
            "lineup_entries": [],
            "incidents": [],
            "graph_points": [],
        }

    @abstractmethod
    def convert(self) -> ConversionResult:
        """Main conversion method"""
        pass

    def _collect_conversion_result(self) -> ConversionResult:
        """Collect all entities into result object"""
        return ConversionResult(
            sports=self.normalized_entities["sports"],
            categories=self.normalized_entities["categories"],
            tournaments=self.normalized_entities["tournaments"],
            seasons=self.normalized_entities["seasons"],
            events=self.normalized_entities["events"],
            teams=self.normalized_entities["teams"],
            team_colors=self.normalized_entities["team_colors"],
            countries=self.normalized_entities["countries"],
            venues=self.normalized_entities["venues"],
            statistic_periods=self.normalized_entities["statistic_periods"],
            lineups=self.normalized_entities["lineups"],
            incidents=self.normalized_entities["incidents"],
            graph_points=self.normalized_entities["graph_points"],
            match_id=self.match_data.match_id,
            processed_components=self.entity_map.get("processed_components", {}),
        )


class BaseComponentBuilder(ABC):
    """Abstract base class for component builders for converters"""

    def __init__(self, parent_converter: BaseConverter):
        self.parent: BaseConverter = parent_converter
        self.entity_map: Dict[str, Any] = parent_converter.entity_map
        self.match_data: sofaschema.FootballMatchResultDetailed = (
            parent_converter.match_data
        )

    @abstractmethod
    def build(self) -> None:
        """Build entities for this component"""
        pass

    @abstractmethod
    def can_build(self) -> bool:
        """Check if this component can be built (data available)"""
        pass
