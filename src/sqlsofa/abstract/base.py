import logging
from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, Set

from pydantic import BaseModel
from sqlmodel import Session, SQLModel

logger = logging.getLogger(__name__)


class BaseEntityConverter(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session


class BaseComponenetConverter:
    """Converts basic event data - can run standalone"""

    def __init__(self) -> None:
        self.raw_data: List[SQLModel] = []
        self.data: Set[SQLModel] = set()

    @abstractmethod
    def convert(self, pydantic_data: BaseModel) -> None:
        """
        Here we want to convert all the data into the sql models

        Store the data as a list attr

        """
        pass

    @abstractmethod
    def normilise(self) -> None:
        """
        Remove duplicates within the convert sqlmodel data.
         store in self
        """
        pass
