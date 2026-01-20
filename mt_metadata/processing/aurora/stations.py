# =====================================================
# Imports
# =====================================================
from typing import Annotated

import pandas as pd
from pydantic import Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.processing.aurora.station import Station


# =====================================================
class Stations(MetadataBase):
    remote: Annotated[
        list[Station],
        Field(
            default_factory=list,
            description="list of remote sites",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["10"],
            },
        ),
    ]

    local: Annotated[
        Station,
        Field(
            default_factory=Station,  # type: ignore
            description="local site",
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
                "examples": ["10"],
            },
        ),
    ]

    @field_validator("remote", mode="before")
    def validate_remote(
        cls, value: list[Station], info: ValidationInfo
    ) -> list[Station]:
        """
            Method for unpacking rr_station info into mt_metadata object.

            Developmnent Notes:
            This function was raising an exception when trying to populate an aurora.Processing object
            from a json.loads() dict.
            TODO: add a description of input variable and use cases, ... it seems that we may not want
            to support multiple rr stations yet.

        Parameters
        ----------
        rr_station

        Returns
        -------
        list of Station objects

        """
        remote = []
        if isinstance(value, list):
            for item in value:
                if isinstance(item, Station):
                    remote.append(item)
                elif isinstance(item, dict):
                    try:
                        station = Station()  # type: ignore
                        station.from_dict(item)
                        remote.append(station)
                    except Exception as e:
                        raise ValueError("could not unpack dict to a Station object")
                else:
                    raise TypeError(
                        f"list item must be Station object not {type(item)}"
                    )

        elif isinstance(value, dict):
            station = Station()
            station.from_dict(value)
            station.remote = True
            remote.append(station)

        elif isinstance(value, Station):
            value.remote = True
            remote.append(value)

        elif isinstance(
            value, str
        ):  # TODO: Add doc; what is this doing? This does not affect self._remote.
            if len(value) > 4:
                raise ValueError(f"not sure to do with {type(value)}")
            # TODO: Add doc explaining what happens when rr_station is str of length 3.

        else:
            raise ValueError(f"not sure to do with {type(value)}")

        return remote

    def add_remote(self, rr: Station | dict):
        """
        add a remote station

        Parameters
        ----------
        rr: Station | dict
            remote station to add
        """

        if not isinstance(rr, (Station, dict)):
            raise TypeError(f"List entry must be a Station object not {type(rr)}")
        if isinstance(rr, dict):
            obj = Station()  # type: ignore
            obj.from_dict(rr)

        else:
            obj = rr

        obj.remote = True

        self.remote.append(obj)

    @property
    def remote_dict(self) -> dict[str, Station]:
        """
        need to have a dictionary, but it can't be an attribute cause that
        gets confusing when reading in a json file

        Returns
        -------
        dict[str, Station]
            dictionary of remote stations

        """
        return dict([(rr.id, rr) for rr in self.remote])

    def from_dataset_dataframe(self, df: pd.DataFrame):
        """
        from a dataset dataframe

        Parameters
        ----------
        df: pd.DataFrame
            dataset dataframe to read from

        Returns
        -------
        None
        """

        # Handle empty DataFrame case
        if df.empty:
            return

        station = df[df.remote == False].station.unique()[0]
        rr_stations = df[df.remote == True].station.unique()

        self.local.from_dataset_dataframe(df[df.station == station])

        for rr_station in rr_stations:
            rr = Station()  # type: ignore
            rr.from_dataset_dataframe(df[df.station == rr_station])
            self.add_remote(rr)

    def to_dataset_dataframe(self) -> pd.DataFrame:
        """
        output a dataframe

        Returns
        -------
        pd.DataFrame
            dataframe representation of the station
        """

        df = self.local.to_dataset_dataframe()
        for rr in self.remote:
            remote_df = rr.to_dataset_dataframe()
            df = pd.concat([df, remote_df])  # , axis=1, ignore_index=True)

        df.reset_index(inplace=True, drop=True)

        return df

    def get_station(self, station_id: str) -> Station:
        """
        get a station object from the id

        Parameters
        ----------
        station_id: str
            ID of the station to retrieve

        Returns
        -------
        Station
            Station object corresponding to the given ID

        """

        if self.local.id == station_id:
            return self.local

        elif station_id in self.remote_dict.keys():
            return self.remote_dict[station_id]

        raise KeyError(f"could not find {station_id}")
