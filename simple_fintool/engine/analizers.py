"""
Module containing the available analizers.
"""

from datetime import date
from typing import List, Optional, Protocol, Tuple, runtime_checkable


@runtime_checkable
class DataAnalizer(Protocol):
    description: str

    def process_datapoint(self, date: date, price: float) -> None: ...

    def process_alldata(self) -> float: ...


class DefaultAnalizer(DataAnalizer):
    description: str = "sum of the latest 10 prices"
    prices_list: List[Tuple[date, float]] = list()

    def process_datapoint(self, date: date, price: float) -> None:

        if len(self.prices_list) < 10:
            self.add_to_list(date, price)

        elif self.prices_list[-1][0] < date:
            self.prices_list.pop()
            self.add_to_list(date, price)

    def add_to_list(self, date: date, price: float) -> None:
        self.prices_list.append((date, price))
        self.prices_list = sorted(self.prices_list, key=lambda x: x[0])
        self.prices_list.reverse()
        print(self.prices_list)
        print()

    def process_alldata(self) -> float:
        return sum([price_tuple[1] for price_tuple in self.prices_list])


class TotalMean(DataAnalizer):
    description: str = "mean for the full period provided"
    total_price: float = 0.0
    total_count: int = 0

    def process_datapoint(self, date: date, price: float) -> None:
        self.total_price += price
        self.total_count += 1

    def process_alldata(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.total_price / float(self.total_count)


class MonthSpecificMean(DataAnalizer):
    description: str = "mean for the month of 11/2014"
    month: int = 11
    year: int = 2014
    total_price: float = 0.0
    total_count: int = 0

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.description = f"mean for the month of {self.month}/{self.year}"

    def process_datapoint(self, date: date, price: float) -> None:
        if not date.year == self.year:
            return
        if not date.month == self.month:
            return
        self.total_price += price
        self.total_count += 1

    def process_alldata(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.total_price / float(self.total_count)


class MaxPriceSpread(DataAnalizer):
    description: str = "the difference between max and min in the period provided"
    minval: Optional[float] = None
    maxval: Optional[float] = None

    def process_datapoint(self, date: date, price: float) -> None:

        if self.minval is None:
            self.minval = price

        if self.maxval is None:
            self.maxval = price

        self.minval = min(self.minval, price)
        self.maxval = max(self.maxval, price)

    def process_alldata(self) -> float:
        if self.minval is None or self.maxval is None:
            return 0.0
        return self.maxval - self.minval
