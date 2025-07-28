import json
import logging

import sofascrape.schemas.general as pydanticschema  # type: ignore

import sqlsofa.schema.sqlmodels as sqlschema
from sqlsofa.abstract import BaseComponenetConverter

logger = logging.getLogger(__name__)


class TournamentComponentConverter(BaseComponenetConverter):
    """
    details here
    """

    def __init__(self) -> None:
        super().__init__()

    def _convert_sport(self, t: pydanticschema.TournamentSchema) -> sqlschema.Sport:
        sport: pydanticschema.SportSchema = t.category.sport
        return sqlschema.Sport(**sport.to_sql_dict())

    def _convert_category(
        self, t: pydanticschema.TournamentSchema
    ) -> sqlschema.Category:
        category: pydanticschema.CategorySchema = t.category
        return sqlschema.Category(**category.to_sql_dict())

    def _convert_tournament(
        self, t: pydanticschema.TournamentSchema
    ) -> sqlschema.Tournament:
        return sqlschema.Tournament(**t.to_sql_dict())

    def convert(self, pydantic_data: pydanticschema.TournamentData) -> None:

        try:
            t = pydantic_data.tournament
        except Exception as e:
            logger.error(
                json.dumps(
                    {
                        "Message": f"Failed to get tournament data for {repr(pydantic_data)}.",
                        "Error": str(e),
                    },
                    indent=2,
                )
            )

        # sports

        sport = self._convert_sport(t)
        category = self._convert_category(t)
        tournament = self._convert_tournament(t)

        self.data = [sport, category, tournament]

    def normilise(self) -> None:
        """trivial here"""
        pass
