import json
import logging
from typing import List

import sofascrape.schemas.general as sofaschema  # type: ignore

import sqlsofa.schema.sqlmodels as sqlschema
from sqlsofa.abstract import BaseComponenetConverter

logger = logging.getLogger(__name__)


class EventsComponentConverter(BaseComponenetConverter):
    """
    Class for processing the list of events for a given seasion.

    sofaschema.EventsListSchema
    sofaschema.EventSchema
    """

    def __init__(self) -> None:
        super().__init__()

    def _convert_sport(self, sport: sofaschema.SportSchema) -> sqlschema.Sport:
        """One-liner conversion for simple models."""
        return sqlschema.Sport(**sport.to_sql_dict())

    def _convert_country(self, country: sofaschema.CountrySchema) -> sqlschema.Country:
        """One-liner conversion for simple models."""
        return sqlschema.Country(**country.to_sql_dict())

    def _convert_category(
        self, category: sofaschema.CategorySchema
    ) -> sqlschema.Category:
        """One-liner conversion - foreign keys handled automatically."""
        return sqlschema.Category(**category.to_sql_dict())

    def _convert_tournament(
        self, tournament: sofaschema.TournamentSchema
    ) -> sqlschema.Tournament:
        """One-liner conversion - foreign keys handled automatically."""
        return sqlschema.Tournament(**tournament.to_sql_dict())

    def _convert_season(self, season: sofaschema.SeasonSchema) -> sqlschema.Season:
        """One-liner conversion for simple models."""
        return sqlschema.Season(**season.to_sql_dict())

    def _convert_event(self, event: sofaschema.EventSchema) -> sqlschema.Event:
        """One-liner conversion - all complexity handled in Pydantic model."""
        return sqlschema.Event(**event.to_sql_dict())

    def process_event(self, event: sofaschema.EventSchema):
        event = self._convert_event(event)

    def convert(self, pydantic_data: sofaschema.EventsListSchema) -> None:

        try:
            events_list: List[sofaschema.EventSchema] = pydantic_data.events
        except Exception as e:
            logger.error(
                json.dumps(
                    {
                        "Message": f"Failed to get events for season, {repr(pydantic_data)}",
                        "Error": str(e),
                    },
                    indent=2,
                )
            )

        self.data = [self._convert_event(e) for e in events_list]
