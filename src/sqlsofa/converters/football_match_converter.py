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

    def build(self) -> None:
        """Build core entities using existing converter functions"""
        if not self.can_build():
            logger.warning("No BASE data available")
            return

        event_data: sofaschema.FootballDetailsSchema = self.match_data.base.event
