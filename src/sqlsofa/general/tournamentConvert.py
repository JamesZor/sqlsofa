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
        return sqlschema.Sport(
            id=t.category.sport.id,
            name=t.category.sport.name,
            slug=t.category.sport.slug,
        )

    def _convert_category(
        self, t: pydanticschema.TournamentSchema
    ) -> sqlschema.Category:
        return sqlschema.Category(
            id=t.category.id,
            name=t.category.name,
            slug=t.category.slug,
            sport_id=t.category.sport.id,
        )

    def _convert_tournament(
        self, t: pydanticschema.TournamentSchema
    ) -> sqlschema.Tournament:
        return sqlschema.Tournament(
            id=t.id, name=t.name, slug=t.slug, category_id=t.category.id
        )

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

        self.raw_data = [sport, category, tournament]

    def normilise(self) -> None:
        """trivial here"""

        self.data = set(self.raw_data)
