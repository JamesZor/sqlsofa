import json
import logging
from typing import List

import sofascrape.schemas.general as sofaschema  # type: ignore

import sqlsofa.schema.sqlmodels as sqlschema
from sqlsofa.abstract import BaseComponenetConverter

logger = logging.getLogger(__name__)


class SeasonsComponentConverter(BaseComponenetConverter):
    """
    Details here
    """

    def __init__(self) -> None:
        super().__init__()

    def _convert_season(self, s: sofaschema.SeasonSchema) -> sqlschema.Season:
        return sqlschema.Season(id=s.id, name=s.name, year=s.year)

    def convert(self, pydantic_data: sofaschema.SeasonsListSchema) -> None:

        try:
            seasons_list: List[sofaschema.SeasonSchema] = pydantic_data.seasons
        except Exception as e:
            logger.error(
                json.dumps(
                    {
                        "Message": f"Failed to get seasons data for {repr(pydantic_data)}.",
                        "Error": str(e),
                    },
                    indent=2,
                )
            )

        self.raw_data = [self._convert_season(s) for s in seasons_list]

    def normilise(self) -> None:
        pass
