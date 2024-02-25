"""
Module containing the available analizers with pandas.
"""

from datetime import date
from typing import List, Optional, Protocol, Tuple, runtime_checkable

from pandas import DataFrame


@runtime_checkable
class DataAnalizerDF(Protocol):
    description: str

    def process_chunk(self, dataframe: DataFrame) -> None: ...

    def process_alldata(self) -> float: ...


class DefaultAnalizerDF(DataAnalizerDF):
    description: str = "sum of the latest 10 prices"
    prices_list: List[Tuple[date, float]] = list()

    def process_chunk(self, dataframe: DataFrame) -> None:

        dataframe_latest10 = dataframe.sort_values(by="Date", ascending=False).head(10)
        newlist = list(
            zip(
                dataframe_latest10["Date"].tolist(),
                dataframe_latest10["Price"].tolist(),
            )
        )

        self.prices_list.extend(newlist)

        dataframe_latest10["Date"].tolist()
        self.prices_list = sorted(self.prices_list, key=lambda x: x[0])
        self.prices_list.reverse()
        self.prices_list = self.prices_list[0:10]

    def process_alldata(self) -> float:
        return sum([price_tuple[1] for price_tuple in self.prices_list])


class TotalMeanDF(DataAnalizerDF):
    description: str = "mean for the full period provided"
    total_price: float = 0.0
    total_count: int = 0

    def process_chunk(self, dataframe: DataFrame) -> None:
        self.total_price += dataframe["Price"].sum()
        self.total_count += dataframe.shape[0]

    def process_alldata(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.total_price / float(self.total_count)


class MonthSpecificMeanDF(DataAnalizerDF):
    description: str = "mean for the month of 11/2014"
    month: int = 11
    year: int = 2014
    total_price: float = 0.0
    total_count: int = 0

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.description = f"mean for the month of {self.month}/{self.year}"

    def is_selected(self, date: date):
        return date.year == self.year and date.month == self.month

    def process_chunk(self, dataframe: DataFrame) -> None:
        dataframe_filtered = dataframe[dataframe["Date"].apply(self.is_selected)]
        if not dataframe_filtered.empty:
            self.total_price += dataframe_filtered["Price"].sum()
            self.total_count += dataframe_filtered.shape[0]

    def process_alldata(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.total_price / float(self.total_count)


class MaxPriceSpreadDF(DataAnalizerDF):
    description: str = "the difference between max and min in the period provided"
    minval: Optional[float] = None
    maxval: Optional[float] = None

    def process_chunk(self, dataframe: DataFrame) -> None:
        newmin = dataframe["Price"].min()
        newmax = dataframe["Price"].max()

        if self.minval is None:
            self.minval = newmin

        if self.maxval is None:
            self.maxval = newmax

        self.minval = min(self.minval, newmin)
        self.maxval = max(self.maxval, newmax)

    def process_alldata(self) -> float:
        if self.minval is None or self.maxval is None:
            return 0.0
        return self.maxval - self.minval
