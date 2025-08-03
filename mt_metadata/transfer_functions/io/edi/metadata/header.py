# =====================================================
# Imports
# =====================================================
from typing import Annotated

import numpy as np
import pandas as pd
from loguru import logger
from pydantic import Field, field_validator

from mt_metadata import __version__
from mt_metadata.common import (
    BasicLocation,
    Declination,
    GeographicLocation,
    GeographicReferenceFrameEnum,
    StdEDIversionsEnum,
)
from mt_metadata.common.mttime import get_now_utc, MTime
from mt_metadata.common.units import get_unit_object
from mt_metadata.utils.location_helpers import convert_position_float2str
from mt_metadata.utils.validators import validate_station_name


# =====================================================


class Header(BasicLocation, GeographicLocation):
    acqby: Annotated[
        str | None,
        Field(
            default=None,
            description="person, group, company, university that collected the data",
            examples=["mt experts"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    acqdate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Start date the time series data were collected",
            examples=["2020-01-01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    coordinate_system: Annotated[
        GeographicReferenceFrameEnum,
        Field(
            default="geographic",
            description="coordinate system the transfer function is currently in. Its preferred the transfer function be in a geographic coordinate system for archiving and sharing.",
            examples=["geopgraphic"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    dataid: Annotated[
        str,
        Field(
            default="",
            description="station ID.",
            examples=["mt001"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    enddate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp | None,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="End date the time series data were collected",
            examples=["2020-01-01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    empty: Annotated[
        float,
        Field(
            default=1e32,
            description="null data values, usually a large number",
            examples=["1E+32"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    fileby: Annotated[
        str,
        Field(
            default="",
            description="person, group, company, university that made the file",
            examples=["mt experts"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    filedate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date the file was made",
            examples=["2020-01-01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    progdate: Annotated[
        MTime | str | float | int | np.datetime64 | pd.Timestamp,
        Field(
            default_factory=lambda: MTime(time_stamp=None),
            description="Date of the most recent update of the program used to make the file",
            examples=["2020-01-01"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    progname: Annotated[
        str,
        Field(
            default="mt_metadata",
            description="Name of the program used to make the file.",
            examples=["mt_metadata"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    progvers: Annotated[
        str,
        Field(
            default="0.1.6",
            description="Version of the program used to make the file.",
            examples=["0.1.6"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    project: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the project the data was collected for, usually a short description or acronym of the project name.",
            examples=["iMUSH"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    prospect: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the prospect the data was collected for, usually a short description of the location",
            examples=["Benton"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    loc: Annotated[
        str | None,
        Field(
            default=None,
            description="Usually a short description of the location",
            examples=["Benton, CA"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    declination: Annotated[
        Declination,
        Field(
            default_factory=lambda: Declination(value=0.0),  # type: ignore
            description="Declination of the station in degrees",
            examples=["Declination(10.0)"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    stdvers: Annotated[
        StdEDIversionsEnum,
        Field(
            default="SEG 1.0",
            description="EDI standards version SEG 1.0",
            examples=["SEG 1.0"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    survey: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the survey",
            examples=["CONUS"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    units: Annotated[
        str | None,
        Field(
            default="milliVolt per kilometer per nanoTesla",
            description="In the EDI standards this is the elevation units, in newer versions this should be units of the transfer function.",
            examples=["milliVolt per kilometer per nanoTesla"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    @field_validator("acqdate", "enddate", "filedate", "progdate", mode="before")
    @classmethod
    def validate_acqdate(
        cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str
    ):
        if isinstance(field_value, MTime):
            return field_value
        return MTime(time_stamp=field_value)

    @field_validator("units", mode="before")
    @classmethod
    def validate_units(cls, value: str) -> str:
        if value in [None, ""]:
            return ""
        try:
            unit_object = get_unit_object(value)
            return unit_object.name
        except ValueError as error:
            raise KeyError(error)
        except KeyError as error:
            raise KeyError(error)

    def __str__(self):
        return "".join(self.write_header())

    def __repr__(self):
        return self.__str__()

    def get_header_list(self, edi_lines):
        """
        Get the header information from the .edi file in the form of a list,
        where each item is a line in the header section.

        :param edi_lines: DESCRIPTION
        :type edi_lines: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        header_list = []
        head_find = False

        # read in list line by line and then truncate
        for line in edi_lines:
            # check for header label
            if ">" in line and "head" in line.lower():
                head_find = True
            # if the header line has been found then the next >
            # should be the next section so stop
            elif ">" in line:
                if head_find is True:
                    break
                else:
                    pass
            # get the header information into a list
            elif head_find:
                # skip any blank lines
                if len(line.strip()) > 2:
                    line = line.strip().replace('"', "")
                    h_list = line.split("=")
                    if len(h_list) == 2:
                        key = h_list[0].strip()
                        value = h_list[1].strip()
                        header_list.append("{0}={1}".format(key, value))
        return header_list

    def read_header(self, edi_lines):
        """
        read a header information from a list of lines
        containing header information.

        :param edi_lines: DESCRIPTION
        :type edi_lines: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        for h_line in self.get_header_list(edi_lines):
            h_list = h_line.split("=")
            key = h_list[0].lower()
            value = h_list[1]
            # test if its a phoenix formated .edi file
            if key in ["progvers"]:
                if value.lower().find("mt-editor") != -1:
                    self.phoenix_edi = True
            elif key in ["coordinate_system"]:
                value = value.lower()
                if "geomagnetic" in value:
                    value = "geomagnetic"
                elif "geographic" in value:
                    value = "geographic"
                elif "station" in value:
                    value = "station"
            elif key in ["stdvers"]:
                if value in ["N/A", "None", "null"]:
                    value = "SEG 1.0"
            elif key in ["units"]:
                if value in ["m", "M"]:
                    value = "m"

            if key == "declination":
                setattr(self.declination, "value", value)
                continue
            elif key in ["long", "lon", "lonigutde"]:
                key = "longitude"
            elif key in ["lat", "latitude"]:
                key = "latitude"
            elif key in ["elev", "elevation"]:
                key = "elevation"
            else:
                if key in ["dataid"]:
                    value = validate_station_name(value)

            setattr(self, key, value)

    def write_header(
        self,
        longitude_format="LON",
        latlon_format="dms",
        required=False,
    ):
        """
        Write header information to a list of lines.


        :param header_list: should be read from an .edi file or input as
                            ['key_01=value_01', 'key_02=value_02']
        :type header_list: list
        :param longitude_format:  whether to write longitude as LON or LONG.
                                  options are 'LON' or 'LONG', default 'LON'
        :type longitude_format:  string
        :param latlon_format:  format of latitude and longitude in output edi,
                               degrees minutes seconds ('dms') or decimal
                               degrees ('dd')
        :type latlon_format:  string

        :returns header_lines: list of lines containing header information

        """

        self.filedate = get_now_utc()
        self.progvers = __version__
        self.progname = "mt_metadata"
        self.progdate = "2021-12-01"

        header_lines = [">HEAD\n"]
        for key, value in self.to_dict(single=True, required=required).items():
            if key in ["x", "x2", "y", "y2", "z", "z2"]:
                continue
            if value in [None, "None"]:
                continue
            if key in ["latitude"]:
                key = "lat"
            elif key in ["longitude"]:
                key = longitude_format.lower()
            elif key in ["elevation"]:
                key = "elev"
            if "declination" in key:
                if self.declination.value == 0.0:
                    continue
            if key in ["lat", "lon", "long"] and value is not None:
                if latlon_format.lower() == "dd":
                    value = f"{value:.6f}"
                else:
                    value = convert_position_float2str(value)
            if key in ["elev"] and value is not None:
                value = "{0:.3f}".format(value)
            if isinstance(value, list):
                value = ",".join(value)
            header_lines.append(f"\t{key.upper()}={value}\n")
        header_lines.append("\n")
        return header_lines

    def _validate_header_list(self, header_list):
        """
        make sure the input header list is valid

        returns a validated header list
        """

        if header_list is None:
            logger.info("No header information to read")
            return None
        new_header_list = []
        for h_line in header_list:
            h_line = h_line.strip().replace('"', "")
            if len(h_line) > 1:
                h_list = h_line.split("=")
                if len(h_list) == 2:
                    key = h_list[0].strip().lower()
                    value = h_list[1].strip()
                    new_header_list.append("{0}={1}".format(key, value))
        return new_header_list
