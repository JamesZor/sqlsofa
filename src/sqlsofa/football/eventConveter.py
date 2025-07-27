import json
import logging
from typing import List

import sofascrape.schemas.general as sofaschema

import sqlsofa.schema.sqlmodels as sqlschema
from sqlsofa.abstract import BaseComponenetConverter

logger = logging.getLogger(__name__)


class EventFootballComponentConverter(BaseComponenetConverter):

    def __init__(self) -> None:
        super().__init__()

        def _convert_tournament(
            event: sofaschema.FootballEventSchema,
        ) -> sqlschema.Tournament:
            t = event.tournament

            return sqlschema.Tournament(
                id=t.id,
                name=t.name,
                slug=t.slug,
                competitionType=t.competitionType,
            )

        def convert(self, pydantic_data: sofaschema.FootballDetailsSchema) -> None:

            try:
                event: sofaschema.FootballEventSchema = pydantic_data.event
            except Exception as e:
                logger.error(
                    json.dumps(
                        {
                            "Message": f"Failed to get event basic data for {repr(pydantic_data)}.",
                            "Error": str(e),
                        },
                        indent=2,
                    )
                )
