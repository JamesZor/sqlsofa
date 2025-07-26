import logging
from typing import Dict, List, Union

from sqlmodel import Session


class EntityHelper:
    """
    Utility methods for get-or create patterns with sqlmodels
    """

    def __init(self, session: Session) -> None:
        self.session: Session = session
