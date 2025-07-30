import logging
from typing import Any, Dict, Optional

from sofascrape.schemas import general as sofaschema

from sqlsofa.schema import sqlmodels as sqlschema
from sqlsofa.utils import converters  # Your existing converter functions!

from .base_converter import BaseComponentBuilder, ConversionResult

logger = logging.getLogger(__name__)


class DetailsComponentBuilder(BaseComponentBuilder):
    """Handles BASE / Details component - must be run first"""

    def can_build(self) -> bool:
        """Check if BASE data is available"""
        return self.match_data.base is not None

    def process_tournament(self, event_data: sofaschema.FootballDetailsSchema) -> None:
        tournament_result: converters.TournamentResult = converters.tournament(
            event_data.tournament
        )
        self._store_entity("sport", tournament_result["sport"])
        self._store_entity("category", tournament_result["category"])
        self._store_entity("tournament", tournament_result["tournament"])

    def process_season(self, event_data: sofaschema.FootballDetailsSchema) -> None:
        season_obj: converters.SeasonResult = converters.season(event_data.season)
        self._store_entity("season", season_obj)

    def process_teams(self, event_data: sofaschema.FootballTeamSchema) -> None:
        home_team_result: converters.TeamResult = converters.team(event_data.homeTeam)
        away_team_result: converters.TeamResult = converters.team(event_data.awayTeam)

        self._store_entity("home_team", home_team_result["team"])
        self._store_entity("away_team", away_team_result["team"])
        self._store_entity("home_team_colors", home_team_result["team_colors"])
        self._store_entity("away_team_colors", away_team_result["team_colors"])

        # Store countries in collection
        self._add_to_collection("countries", home_team_result["country"])
        self._add_to_collection("countries", away_team_result["country"])

    def build(self) -> None:
        """Build core entities using existing converter functions"""
        if not self.can_build():
            logger.warning("No BASE data available")
            return

        event_data: sofaschema.FootballDetailsSchema = self.match_data.base.event

        # Use your existing converter functions!
        # 1. Tournament chain (Sport -> Category -> Tournament)
        self.process_tournament(event_data=event_data)
        # 2. Season
        self.process_season(event_data=event_data)

        # 3. Teams - using your team converter
        self.process_teams(event_data=event_data)

        # 4. Event details
        status_obj = converters.status(event_data.status)
        round_info_obj = converters.round_info(event_data.roundInfo)

        # 5. Optional objects
        if event_data.time:
            time_obj = converters.time_football(event_data.time)
            self._store_entity("time_football", time_obj)

        if event_data.homeScore:
            home_score_obj = converters.score(event_data.homeScore)
            self._store_entity("home_score", home_score_obj)

        if event_data.awayScore:
            away_score_obj = converters.score(event_data.awayScore)
            self._store_entity("away_score", away_score_obj)

        # 6. Football-specific fields
        if hasattr(event_data, "venue") and event_data.venue:
            venue_result = converters.venue(event_data.venue)
            self._store_entity("venue", venue_result["venue"])
            # Add venue-related entities to collections

        if hasattr(event_data, "referee") and event_data.referee:
            referee_result = converters.referee(event_data.referee)
            self._store_entity("referee", referee_result["referee"])

        # 7. Create the main Event
        event_dict = event_data.to_sql_dict()
        # Now add foreign keys from our entity_map
        event_dict.update(
            {
                "tournament_id": self.entity_map["tournament"].id,
                "season_id": self.entity_map["season"].id,
                "home_team_id": self.entity_map["home_team"].id,
                "away_team_id": self.entity_map["away_team"].id,
                # Add other foreign keys as needed
            }
        )

        event_obj = sqlschema.Event(**event_dict)
        self._store_entity("event", event_obj)

        logger.info(f"Successfully built BASE component for match {event_obj.id}")

    def _store_entity(self, key: str, entity: Any) -> None:
        """Store entity in map and add to normalized collection"""
        self.entity_map[key] = entity

        # Also add to normalized collections
        if isinstance(entity, sqlschema.Sport):
            self.parent.normalized_entities["sports"].add(entity)
        elif isinstance(entity, sqlschema.Team):
            self.parent.normalized_entities["teams"].add(entity)
        # ... etc for other types

    def _add_to_collection(self, key: str, entity: Any) -> None:
        """Add entity to a collection (like countries)"""
        if key not in self.entity_map:
            self.entity_map[key] = {}

        # Use appropriate key for the entity
        if isinstance(entity, sqlschema.Country):
            self.entity_map[key][entity.alpha3] = entity
            self.parent.normalized_entities["countries"].add(entity)
