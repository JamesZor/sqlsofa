# sqlsofa/converters/football_match_converter.py

import logging
from typing import Any, Dict, Optional

from sofascrape.schemas import general as sofaschema

from .base_converter import BaseConverter, ConversionResult
from .football_detials_converter import DetailsComponentBuilder

# from .football_stats_converter import StatsComponentBuilder
# from .football_lineup_converter import LineupComponentBuilder
# from .football_incidents_converter import IncidentsComponentBuilder
# from .football_graph_converter import GraphComponentBuilder

logger = logging.getLogger(__name__)


class FootballMatchConverter(BaseConverter):
    """Main converter for football match data"""

    def __init__(self, match_data: sofaschema.FootballMatchResultDetailed):
        # Initialize parent which sets up entity_map and normalized_entities
        super().__init__(match_data)

        # Initialize all component builders
        self.builders = self._initialize_builders()

    def _initialize_entity_map(self) -> Dict[str, Any]:
        """Initialize the entity map with football-specific structure"""
        return {
            # === CORE ENTITIES (from BASE/Details component) ===
            "sport": None,
            "category": None,
            "tournament": None,
            "season": None,
            "event": None,
            # === TEAMS & RELATED ===
            "home_team": None,
            "away_team": None,
            "home_team_colors": None,
            "away_team_colors": None,
            "venue": None,
            "referee": None,
            # === COLLECTIONS ===
            "countries": {},  # Dict[str, Country] - keyed by alpha3
            "players": {},  # Dict[int, LineupPlayer] - keyed by player_id
            "managers": {},  # Dict[int, Manager] - keyed by manager_id
            # === COMPONENT-SPECIFIC STRUCTURES ===
            "statistic_periods": {},  # Dict[str, FootballStatisticPeriod]
            "lineup_data": {
                "home_lineup": None,
                "away_lineup": None,
                "football_lineup": None,
            },
            "incidents_by_type": {
                "goals": [],
                "cards": [],
                "substitutions": [],
                "periods": [],
                "var_decisions": [],
            },
            "graph_points": [],
            # === METADATA ===
            "processed_components": {
                "base": False,
                "stats": False,
                "lineup": False,
                "incidents": False,
                "graph": False,
            },
        }

    def _initialize_builders(self) -> Dict[str, Any]:
        """Initialize all component builders"""
        return {
            "base": DetailsComponentBuilder(self),
            # Uncomment as you implement each builder
            # 'stats': StatsComponentBuilder(self),
            # 'lineup': LineupComponentBuilder(self),
            # 'incidents': IncidentsComponentBuilder(self),
            # 'graph': GraphComponentBuilder(self),
        }

    def convert(self) -> ConversionResult:
        """
        Main conversion method - orchestrates all component builders
        """
        logger.info(f"Starting conversion for match {self.match_data.match_id}")

        # 1. MUST process BASE/Details first - it populates core entities
        if "base" in self.builders and self.builders["base"].can_build():
            logger.info("Processing BASE/Details component")
            self.builders["base"].build()
            self.entity_map["processed_components"]["base"] = True
        else:
            logger.error("Cannot process match without BASE data")
            raise ValueError("BASE component is required for conversion")

        # 2. Process other components (they depend on BASE entities)
        for component_name in ["stats", "lineup", "incidents", "graph"]:
            if component_name in self.builders:
                builder = self.builders[component_name]
                if builder.can_build():
                    logger.info(f"Processing {component_name.upper()} component")
                    try:
                        builder.build()
                        self.entity_map["processed_components"][component_name] = True
                    except Exception as e:
                        logger.error(f"Failed to process {component_name}: {str(e)}")
                else:
                    logger.info(f"Skipping {component_name} - no data available")

        # 3. Collect and return results
        result = self._collect_conversion_result()
        logger.info(
            f"Conversion complete. Processed components: "
            f"{self.entity_map['processed_components']}"
        )

        return result
