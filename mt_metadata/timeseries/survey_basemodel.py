#=====================================================
# Imports
#=====================================================
from enum import Enum
from typing import Annotated

import numpy as np
import pandas as pd
from mt_metadata.base import MetadataBase
from mt_metadata.utils.mttime import MTime
from pydantic import Field, field_validator


#=====================================================
class DatumEnum(str, Enum):
    WGS84 = 'WGS84'
    NAD27 = 'NAD27'
    NAD83 = 'NAD83'
    ETRS89 = 'ETRS89'
    GDA94 = 'GDA94'
    PZ-90.11 = 'PZ-90.11'
    other = 'other'
class Survey(MetadataBase):
    id: Annotated[str, Field(
    default='',
    description='Alpha numeric ID that will be unique for archiving.',
    examples='EMT20',
    type='string',
    alias=None,
    pattern='^[a-zA-Z0-9]*$',
    json_schema_extra={'units':None,'required':True,},

)]

    comments: Annotated[str | None, Field(
    default=None,
    description='Any comments about the survey.',
    examples='long survey',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':False,},

)] = None

    datum: Annotated[DatumEnum, Field(
    default=WGS84,
    description='Datum of latitude and longitude coordinates. Should be a well-known datum, such as WGS84, and will be the reference datum for all locations.  This is important for the user, they need to make sure all coordinates in the survey and child items (i.e. stations, channels) are referenced to this datum.',
    examples='WGS84',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    geographic_name: Annotated[str, Field(
    default='',
    description='Closest geographic reference to survey, usually a city but could be a landmark or some other common geographic reference point.',
    examples='Yukon',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    name: Annotated[str, Field(
    default='',
    description='Descriptive name of the survey.',
    examples='MT Characterization of Yukon Terrane',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    project: Annotated[str, Field(
    default='',
    description='Alpha numeric name for the project e.g USGS-GEOMAG.',
    examples='YUTOO',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    summary: Annotated[str, Field(
    default='',
    description='Summary paragraph of survey including the purpose; difficulties; data quality; summary of outcomes if the data have been processed and modeled.',
    examples='long project of characterizing mineral resources in Yukon',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    time_period.end_date: Annotated[MTime | str | float | int | np.datetime64 | pd.Timestamp, Field(
    default_factory=lambda: MTime(time_stamp=None),
    description='End date of the survey in UTC.',
    examples='1995-01-01',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    time_period.start_date: Annotated[MTime | str | float | int | np.datetime64 | pd.Timestamp, Field(
    default_factory=lambda: MTime(time_stamp=None),
    description='Start date of the survey in UTC.',
    examples='1/2/2020',
    type='string',
    alias=None,
    json_schema_extra={'units':None,'required':True,},

)]

    @field_validator('time_period.end_date', mode='before')
    @classmethod
    def validate_time_period.end_date(cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str):
        return MTime(time_stamp=field_value)

    @field_validator('time_period.start_date', mode='before')
    @classmethod
    def validate_time_period.start_date(cls, field_value: MTime | float | int | np.datetime64 | pd.Timestamp | str):
        return MTime(time_stamp=field_value)
