"""
Attempt at using manual batches for processing.
Did not improve performance.
"""

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Tuple

from pydantic import BaseModel

from simple_fintool.database.manager import DatabaseManager

from .analizers import (
    DataAnalizer,
    DefaultAnalizer,
    MaxPriceSpread,
    MonthSpecificMean,
    TotalMean,
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


class CoreEngine(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    analizer_list: Dict[str, DataAnalizer] = {
        "INSTRUMENT1": TotalMean(),
        "INSTRUMENT2": MonthSpecificMean(year=2014, month=11),
        "INSTRUMENT3": MaxPriceSpread(),
    }
    default_analizer: DataAnalizer = DefaultAnalizer()
    database_manager: DatabaseManager = DatabaseManager()

    def process_file(self, filepath: str):
        """Process data from a given file."""

        file_path = Path(filepath)
        if not file_path.is_file():
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        with open(file_path) as fileobj:
            csv_reader = csv.reader(fileobj)

            batch_size = 10000
            counter = 0
            tempdict: Dict[str, List[Tuple[date, float]]] = {}
            for row in csv_reader:
                counter += 1

                # Convert to datetime
                # Custom way knowing the exact month string is faster than the more
                # versatile and secure intrinsic datetime function.
                try:
                    instr_name = row[0]
                    # instr_date = datetime.strptime(row[1], "%d-%b-%Y").date()
                    rowlist = row[1].split("-")
                    newy = int(rowlist[2])
                    newm = MONTH_NAME_TO_NUMBER[rowlist[1]]
                    newd = int(rowlist[0])
                    instr_date = datetime(newy, newm, newd)
                    instr_price = float(row[2])
                except (IndexError, ValueError) as error:
                    raise ValueError(f"Error parsing row {row}") from error

                # Filter out weekend days
                if instr_date.weekday() >= 5:
                    date_string = instr_date.strftime("%Y-%m-%d")
                    print(f"Entry for invalid (weekend) date: {date_string}")
                    continue

                if instr_name not in tempdict:
                    tempdict[instr_name] = []
                tempdict[instr_name].append((instr_date, instr_price))

                if counter < batch_size:
                    continue

                for instrument, datalist in tempdict.items():

                    if instrument not in self.analizer_list:
                        self.analizer_list[instrument] = self.default_analizer

                    instrumen_multiplier = self.database_manager.get_stashed_multiplier(
                        instrument
                    )

                    for this_date, this_price in datalist:
                        this_price = this_price * instrumen_multiplier
                        self.analizer_list[instrument].process_datapoint(
                            this_date, this_price
                        )

                counter = 0
                tempdict = {}

            for instrument, datalist in tempdict.items():

                if instrument not in self.analizer_list:
                    self.analizer_list[instrument] = self.default_analizer

                instrumen_multiplier = self.database_manager.get_stashed_multiplier(
                    instrument
                )

                for this_date, this_price in datalist:
                    this_price = this_price * instrumen_multiplier
                    self.analizer_list[instrument].process_datapoint(
                        this_date, this_price
                    )

            for instrument, analizer in self.analizer_list.items():
                result = analizer.process_alldata()
                print(f"Results of `{analizer.description}` for {instrument}: {result}")
