"""
Module containing the engine which runs the analizers with pandas.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict

import pandas as pd
from pydantic import BaseModel

from simple_fintool.database.manager import DatabaseManager

from .analizers import (
    DataAnalizerDF,
    DefaultAnalizerDF,
    MaxPriceSpreadDF,
    MonthSpecificMeanDF,
    TotalMeanDF,
)

MONTH_NAME_TO_NUMBER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


class CoreEngineDF(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    analizer_list: Dict[str, DataAnalizerDF] = {
        "INSTRUMENT1": TotalMeanDF(),
        "INSTRUMENT2": MonthSpecificMeanDF(year=2014, month=11),
        "INSTRUMENT3": MaxPriceSpreadDF(),
    }
    default_analizer: DataAnalizerDF = DefaultAnalizerDF()
    database_manager: DatabaseManager = DatabaseManager()

    def process_file(self, filepath: str):
        """Process data from a given file."""

        file_path = Path(filepath)
        if not file_path.is_file():
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        chunk_size = 1000000
        for df_chunk in pd.read_csv(
            file_path,
            header=None,
            names=["Instrument", "Date", "Price"],
            chunksize=chunk_size,
        ):

            # Convert to datetime
            # Custom way knowing the exact month string is faster than the more
            # versatile and secure intrinsic datetime function.
            def convert_to_date(date_str):
                datelist = date_str.split("-")
                newy = int(datelist[2])
                newm = MONTH_NAME_TO_NUMBER[datelist[1]]
                newd = int(datelist[0])
                return datetime(newy, newm, newd)

            df_chunk["Date"] = df_chunk["Date"].apply(convert_to_date)
            # df_chunk['Date'] = pd.to_datetime(df_chunk['Date'], format='%d-%b-%Y')#.dt.date

            # Filter out weekends
            # Having to copy to convert to dates seems not necessary and
            # extra expensive.
            df_chunk = df_chunk[df_chunk["Date"].dt.weekday < 5]  # .copy()
            # df_chunk['Date'] = df_chunk['Date'].dt.date

            # Get the distinct instruments
            distinct_instruments = df_chunk["Instrument"].unique()

            for distinct_instrument in distinct_instruments:

                if distinct_instrument not in self.analizer_list:
                    self.analizer_list[distinct_instrument] = self.default_analizer

                df_chunk_filtered = df_chunk[
                    df_chunk["Instrument"] == distinct_instrument
                ].copy()
                price_mult = self.database_manager.get_stashed_multiplier(
                    distinct_instrument
                )
                df_chunk_filtered["Price"] = df_chunk_filtered["Price"] * price_mult

                self.analizer_list[distinct_instrument].process_chunk(df_chunk_filtered)

        for instrument, analizer in self.analizer_list.items():
            result = analizer.process_alldata()
            print(f"Results of `{analizer.description}` for {instrument}: {result}")
