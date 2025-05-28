# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import computed_field, Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.utils.location_helpers import validate_position
from mt_metadata.utils.units import get_unit_object


# =====================================================
class DefineMeasurement(MetadataBase):
    """
    DefineMeasurement class holds information about the measurement.  This
    includes how each channel was setup.  The main block contains information
    on the reference location for the station.  This is a bit of an archaic
    part and was meant for a multiple station .edi file.  This section is also
    important if you did any forward modeling with Winglink cause it only gives
    the station location in this section.  The other parts are how each channel
    was collected.  An example define measurement section looks like::

        >=DEFINEMEAS

            MAXCHAN=7
            MAXRUN=999
            MAXMEAS=9999
            UNITS=M
            REFTYPE=CART
            REFLAT=-30:12:49.4693
            REFLONG=139:47:50.87
            REFELEV=0

        >HMEAS ID=1001.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >HMEAS ID=1002.001 CHTYPE=HY X=0.0 Y=0.0 Z=0.0 AZM=90.0
        >HMEAS ID=1003.001 CHTYPE=HZ X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >EMEAS ID=1004.001 CHTYPE=EX X=0.0 Y=0.0 Z=0.0 X2=0.0 Y2=0.0
        >EMEAS ID=1005.001 CHTYPE=EY X=0.0 Y=0.0 Z=0.0 X2=0.0 Y2=0.0
        >HMEAS ID=1006.001 CHTYPE=HX X=0.0 Y=0.0 Z=0.0 AZM=0.0
        >HMEAS ID=1007.001 CHTYPE=HY X=0.0 Y=0.0 Z=0.0 AZM=90.0

    :param fn: full path to .edi file to read in.
    :type fn: string

    ================= ==================================== ======== ===========
    Attributes        Description                          Default  In .edi
    ================= ==================================== ======== ===========
    fn                Full path to edi file read in        None     no
    maxchan           Maximum number of channels measured  None     yes
    maxmeas           Maximum number of measurements       9999     yes
    maxrun            Maximum number of measurement runs   999      yes
    meas_####         HMeasurement or EMEasurment object   None     yes
                      defining the measurement made [1]__
    refelev           Reference elevation (m)              None     yes
    reflat            Reference latitude [2]_              None     yes
    refloc            Reference location                   None     yes
    reflon            Reference longituted [2]__           None     yes
    reftype           Reference coordinate system          'cart'   yes
    units             Units of length                      m        yes
    _define_meas_keys Keys to include in define_measurment [3]__     no
                      section.
    ================= ==================================== ======== ===========

    .. [1] Each channel with have its own define measurement and depending on
           whether it is an E or H channel the metadata will be different.
           the #### correspond to the channel number.
    .. [2] Internally everything is converted to decimal degrees.  Output is
          written as HH:MM:SS.ss so Winglink can read them in.
    .. [3] If you want to change what metadata is written into the .edi file
           change the items in _header_keys.  Default attributes are:
               * maxchan
               * maxrun
               * maxmeas
               * reflat
               * reflon
               * refelev
               * reftype
               * units

    """

    maxchan: Annotated[
        int,
        Field(
            default=999,
            description="maximum number of channels",
            examples=["16"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxrun: Annotated[
        int,
        Field(
            default=999,
            description="maximum number of runs",
            examples=["999"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    maxmeas: Annotated[
        int,
        Field(
            default=7,
            description="maximum number of measurements",
            examples=["999"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    reftype: Annotated[
        str | None,
        Field(
            default="cartesian",
            description="Type of offset from reference center point.",
            examples=["cartesian", "cart"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    refloc: Annotated[
        str | None,
        Field(
            default=None,
            description="Description of location reference center point.",
            examples=["here"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    reflat: Annotated[
        float,
        Field(
            default=0,
            description="Latitude of reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    reflon: Annotated[
        float,
        Field(
            default=0,
            description="Longitude reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": False,
            },
        ),
    ]

    refelev: Annotated[
        float,
        Field(
            default=0,
            description="Elevation reference center point.",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "meters",
                "required": False,
            },
        ),
    ]

    units: Annotated[
        float | None,
        Field(
            default="m",
            description="In the EDI standards this is the elevation units.",
            examples=["m"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

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

    @field_validator("reflat", "reflong", mode="before")
    @classmethod
    def validate_position(cls, value, info: ValidationInfo):
        return validate_position(value, info.field_name)

    def __str__(self):
        return "".join(self.write_measurement())

    def __repr__(self):
        return self.__str__()

    @computed_field
    @property
    def channel_ids(self):
        ch_ids = {}
        for comp in ["ex", "ey", "hx", "hy", "hz", "rrhx", "rrhy"]:
            try:
                m = getattr(self, f"meas_{comp}")
                # if there are remote references that are the same as the
                # h channels skip them.
                ch_ids[m.chtype] = m.id
            except AttributeError:
                continue

        return ch_ids
