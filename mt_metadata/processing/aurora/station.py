# =====================================================
# Imports
# =====================================================
from pathlib import Path
from typing import Annotated, Union

import pandas as pd
from pydantic import computed_field, Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.common import TimePeriod
from mt_metadata.processing.aurora.run import Run


# =====================================================
class Station(MetadataBase):
    id: Annotated[
        str,
        Field(
            default="",
            description="Station ID",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["mt001"],
            },
        ),
    ]

    mth5_path: Annotated[
        str | Path,
        Field(
            default="",
            description="full path to MTH5 file where the station data is contained",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["/home/mt/experiment_01.h5"],
            },
        ),
    ]

    remote: Annotated[
        bool,
        Field(
            default=False,
            description="remote station (True) or local station (False)",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["False"],
            },
        ),
    ]

    runs: Annotated[
        list[Run],
        Field(
            default_factory=list,
            description="List of runs to process",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["001"],
            },
        ),
    ]

    @field_validator("mth5_path", mode="before")
    @classmethod
    def validate_mth5_path(cls, value: str | Path, info: ValidationInfo) -> str | Path:
        try:
            return Path(value)
        except Exception as e:
            raise ValueError(f"could not convert {value} to Path") from e

    @field_validator("runs", mode="before")
    @classmethod
    def validate_runs(cls, values: Union[list, str, Run, dict], info: ValidationInfo):
        runs = []
        if not isinstance(values, list):
            values = [values]

        for item in values:
            if isinstance(item, str):
                run = Run(id=item)
            elif isinstance(item, Run):
                run = item
            elif isinstance(item, dict):
                run = Run()
                run.from_dict(item)

            else:
                raise TypeError(f"not sure what to do with type {type(item)}")

            runs.append(run)

        return runs

    def get_run(self, run_id) -> Run | None:
        """
        Get a run by ID

        Parameters
        ----------
        run_id : TYPE
            DESCRIPTION

        Returns
        -------
        Run | None
            DESCRIPTION
        """

        try:
            return self.run_dict[run_id]
        except KeyError:
            return None

    @computed_field
    @property
    def run_list(self) -> list[str]:
        """list of run names"""

        return [r.id for r in self.runs]

    @computed_field
    @property
    def run_dict(self) -> dict[str, Run]:
        """
        need to have a dictionary, but it can't be an attribute cause that
        gets confusing when reading in a json file

        Returns
        -------
        dict[str, Run]
            DESCRIPTION
        """
        return dict([(rr.id, rr) for rr in self.runs])

    def to_dataset_dataframe(self) -> pd.DataFrame:
        """
        Create a dataset definition dataframe that can be used in the
        processing

        [
            "station",
            "run",
            "start",
            "end",
            "mth5_path",
            "sample_rate",
            "input_channels",
            "output_channels",
            "remote",
        ]

        """

        data_list = []

        for run in self.runs:
            for tp in run.time_periods:
                entry = {
                    "station_id": self.id,
                    "run_id": run.id,
                    "start": str(tp.start),  # Convert to string to avoid MTime issues
                    "end": str(tp.end),  # Convert to string to avoid MTime issues
                    "mth5_path": self.mth5_path,
                    "sample_rate": run.sample_rate,
                    "input_channel_names": run.input_channels,
                    "output_channel_names": run.output_channels,
                    "remote": self.remote,
                    "channel_scale_factors": run.channel_scale_factors,
                }
                data_list.append(entry)

        df = pd.DataFrame(data_list)
        if len(df) > 0:
            df["start"] = pd.to_datetime(df["start"])
            df["end"] = pd.to_datetime(df["end"])

        return df

    def from_dataset_dataframe(self, df: pd.DataFrame):
        """
        set a data frame

        [
            "station",
            "run",
            "start",
            "end",
            "mth5_path",
            "sample_rate",
            "input_channels",
            "output_channels",
            "remote",
        ]

        Parameters
        ----------
        df : pd.DataFrame
            DESCRIPTION

        Returns
        -------
        TYPE
            DESCRIPTION
        """

        self.runs = []

        # Handle empty DataFrame case
        if df.empty:
            return

        self.id = df.station.unique()[0]
        self.mth5_path = df.mth5_path.unique()[0]
        self.remote = df.remote.unique()[0]

        for entry in df.itertuples():
            try:
                r = self.run_dict[entry.run]
                r.time_periods.append(
                    TimePeriod(start=str(entry.start), end=str(entry.end))
                )

            except KeyError:
                if hasattr(entry, "channel_scale_factors"):
                    channel_scale_factors = entry.channel_scale_factors
                else:
                    channel_scale_factors = {}
                r = Run(
                    id=entry.run,
                    sample_rate=entry.sample_rate,
                    input_channels=entry.input_channels,
                    output_channels=entry.output_channels,
                    time_periods=[
                        TimePeriod(start=str(entry.start), end=str(entry.end))
                    ],
                )
                r.set_channel_scale_factors(channel_scale_factors)
                self.runs.append(r)
