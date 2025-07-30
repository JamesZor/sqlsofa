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


class BaseComponentBuilder(ABC):
    """Abstract base class for component builders for converters"""

    def __init__(self, parent_converter: "BaseConverter"):
        self.parent: "BaseConverter" = parent_converter
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
