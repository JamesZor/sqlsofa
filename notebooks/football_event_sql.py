from datetime import datetime
from typing import Any, List, Optional, Tuple, Union

import sofascrape.schemas.general as schemas  # type: ignore
from pydantic import BaseModel
from sofascrape.utils import NoteBookType, NotebookUtils  # type: ignore
from sqlmodel import (  # type: ignore
    Field,
    Relationship,
    Session,
    SQLModel,
)

########################################
###
########################################


if __name__ == "__main__":
    nbu = NotebookUtils(type=NoteBookType.FOOTBALL, web_on=False)
    matchid = 12436870
    playerid = 149380  # Harry Maguire
    base_match_raw = nbu.load(file_name=f"football_base_match_{matchid}")
    base_event_match: schemas.FootballDetailsSchema = (
        schemas.FootballDetailsSchema.model_validate(base_match_raw)
    )

    print(base_event_match.event.venue.model_dump_json(indent=3))
