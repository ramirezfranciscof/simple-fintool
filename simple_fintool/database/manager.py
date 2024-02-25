"""
Class to manage the access to the database.
"""

from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional

from sqlalchemy import select

from simple_fintool.database.session import get_session
from simple_fintool.database.tables import InstrumentPriceModifier


class DatabaseManager:

    def __init__(self, db_context_manager: Callable = get_session) -> None:
        """Initialize the manager."""
        self._db_context_manager = db_context_manager
        self._cached_multipliers = self.get_multipliers()
        self._last_cache = datetime.now()

    def get_stashed_multiplier(self, instrument_name):
        if self._last_cache + timedelta(seconds=5) < datetime.now():
            self._cached_multipliers = self.get_multipliers()
            self._last_cache = datetime.now()
        if instrument_name not in self._cached_multipliers:
            return 1.0
        return self._cached_multipliers[instrument_name]

    def get_multipliers(self, requested_multipliers: Optional[List[str]] = None):
        """Add multipliers from input dict."""
        query_str = select(InstrumentPriceModifier)

        if requested_multipliers is not None:
            query_str = query_str.where(
                InstrumentPriceModifier.name.in_(requested_multipliers)
            )

        with self._db_context_manager() as db_session:
            results = db_session.execute(query_str).all()

        results = {element[0].name: element[0].multiplier for element in results}
        return results

    def update_multipliers(self, input_dict: Dict[str, float]):
        """Update multipliers from input dict."""
        with self._db_context_manager() as db_session:
            for mult_name, mult_value in input_dict.items():

                query_str = select(InstrumentPriceModifier).where(
                    InstrumentPriceModifier.name == mult_name
                )
                results = db_session.execute(query_str).all()

                if len(results) == 0:
                    new_multiplier = InstrumentPriceModifier(
                        name=mult_name, multiplier=mult_value
                    )
                    db_session.add(new_multiplier)

                elif len(results) == 1:
                    old_multiplier = results[0][0]
                    old_multiplier.multiplier = mult_value

                else:
                    raise RuntimeError("Database seems corrupted.")

            db_session.commit()
