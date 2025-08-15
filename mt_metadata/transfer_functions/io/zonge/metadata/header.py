# =====================================================
# Imports
# =====================================================
from typing import Annotated, Any, Dict, Optional

from pydantic import computed_field, Field, field_validator, PrivateAttr

from mt_metadata.base import MetadataBase
from mt_metadata.utils.validators import validate_attribute

from . import CH, GDP, GPS, Job, Line, MTEdit, MTFT24, Rx, STN, Survey, Tx, Unit


# =====================================================
class Header(MetadataBase):
    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Station name",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    survey: Annotated[
        Survey,
        Field(
            default_factory=Survey,
            description="Survey metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    tx: Annotated[
        Tx,
        Field(
            default_factory=Tx,
            description="Transmitter metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    rx: Annotated[
        Rx,
        Field(
            default_factory=Rx,
            description="Receiver metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    m_t_edit: Annotated[
        MTEdit,
        Field(
            default_factory=MTEdit,
            description="MTEdit metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    m_t_f_t24: Annotated[
        MTFT24,
        Field(
            default_factory=MTFT24,
            description="MTFT24 metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    gps: Annotated[
        GPS,
        Field(
            default_factory=GPS,
            description="GPS metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    gdp: Annotated[
        GDP,
        Field(
            default_factory=GDP,
            description="GDP metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    ch: Annotated[
        CH,
        Field(
            default_factory=CH,
            description="CH metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    stn: Annotated[
        STN,
        Field(
            default_factory=STN,
            description="STN metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    line: Annotated[
        Line,
        Field(
            default_factory=Line,
            description="Line metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    unit: Annotated[
        Unit,
        Field(
            default_factory=Unit,
            description="Unit metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    job: Annotated[
        Job,
        Field(
            default_factory=Job,
            description="Job metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    elevation: Annotated[
        float,
        Field(
            default=0.0,
            description="Elevation metadata",
            examples=["null"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": False,
            },
        ),
    ]

    # Private fields for GPS coordinates (excluded from serialization but used internally)
    _gps_lat: float = PrivateAttr(default=0.0)
    _gps_lon: float = PrivateAttr(default=0.0)
    _elevation: float = PrivateAttr(default=0.0)

    _comp_dict: Dict[str, Any] = PrivateAttr(default_factory=dict)

    _header_keys = [
        "survey.type",
        "survey.array",
        "tx.type",
        "m_t_edit.version",
        "m_t_edit.auto.phase_flip",
        "m_t_edit.phase_slope.smooth",
        "m_t_edit.phase_slope.to_z_mag",
        "m_t_edit.d_plus.use",
        "rx.gdp_stn",
        "rx.length",
        "rx.h_p_r",
        "g_p_s.lat",
        "g_p_s.lon",
        "unit.length",
    ]

    def read_header(self, lines):
        """
        Read the header of an AVG file and fill attributes accordingly

        :param lines: list of lines to read
        :type lines: list of strings

        """

        comp = None
        data_lines = []
        for ii, line in enumerate(lines):
            if line.find("=") > 0 and line.find("$") == 0:
                key, value = line[1:].split("=")
                key = ".".join(
                    [validate_attribute(k) for k in key.replace(":", ".").split(".")]
                )

                value = value.lower().strip()
                if "," in value:
                    value = [v.strip() for v in value.split(",")]
                if "length" in key:
                    value = value.split()
                    if len(value) > 1:
                        value = value[0]
                    else:
                        value = value[0].strip()

                if "rx.cmp" in key:
                    comp = value
                    data_lines.append(line)
                    self._comp_dict[comp] = {"rx": Rx(), "ch": CH()}
                if comp is not None:
                    comp_key, comp_attr = key.split(".")

                    self._comp_dict[comp][comp_key].set_attr_from_name(comp_attr, value)
                else:
                    self.set_attr_from_name(key, value)
            else:
                if len(line) > 2:
                    data_lines.append(line)

        return data_lines

    def _has_channel(self, component):
        try:
            if self._comp_dict["zxx"]["ch"].cmp is None:
                return False
        except KeyError:
            return False
        return True

    # =====================================================
    # Field validators for input validation
    # =====================================================

    @field_validator("elevation", mode="before")
    @classmethod
    def validate_elevation(cls, v):
        """Validate and convert elevation input."""
        if v is None:
            return 0.0
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v)

    @classmethod
    def validate_coordinates(cls, v):
        """Validate and convert coordinate input."""
        if v is None:
            return 0.0
        if isinstance(v, str):
            try:
                return float(v.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{v}' to float")
        return float(v)

    # =====================================================
    # Computed fields (read-only properties)
    # =====================================================

    @computed_field
    @property
    def latitude(self) -> float:
        """Get latitude from GPS data."""
        return self.gps.lat if hasattr(self.gps, "lat") else self._gps_lat

    @computed_field
    @property
    def longitude(self) -> float:
        """Get longitude from GPS data."""
        return self.gps.lon if hasattr(self.gps, "lon") else self._gps_lon

    @computed_field
    @property
    def easting(self) -> Optional[float]:
        """Get easting from center location."""
        center_loc = self.center_location
        return center_loc[0] if center_loc is not None else None

    @computed_field
    @property
    def northing(self) -> Optional[float]:
        """Get northing from center location."""
        center_loc = self.center_location
        return center_loc[1] if center_loc is not None else None

    @computed_field
    @property
    def center_location(self) -> Optional[list[float]]:
        """Get center location from component data."""
        if self._has_channel("zxx"):
            location_str = self._comp_dict["zxx"]["rx"].center
            if location_str is None:
                return None
            try:
                return [float(ss.strip().split()[0]) for ss in location_str.split(":")]
            except (ValueError, AttributeError, IndexError):
                return None
        return None

    @computed_field
    @property
    def datum(self) -> Optional[str]:
        """Get datum from GPS data."""
        return (
            self.gps.datum.upper()
            if hasattr(self.gps, "datum") and self.gps.datum
            else None
        )

    @computed_field
    @property
    def utm_zone(self) -> Optional[str]:
        """Get UTM zone from GPS data."""
        zone = self.gps.u_t_m_zone if hasattr(self.gps, "u_t_m_zone") else None
        return str(zone) if zone is not None else None

    @computed_field
    @property
    def station(self) -> Optional[str]:
        """Get station from RX data."""
        return self.rx.gdp_stn if hasattr(self.rx, "gdp_stn") else None

    @computed_field
    @property
    def instrument_id(self) -> Optional[str]:
        """Get instrument ID from component data."""
        if self._has_channel("zxx"):
            try:
                return self._comp_dict["zxx"]["ch"].gdp_box[0]
            except (KeyError, IndexError, AttributeError):
                return None
        return None

    @computed_field
    @property
    def instrument_type(self) -> Optional[str]:
        """Get instrument type from GDP data."""
        return (
            self.gdp.type.upper()
            if hasattr(self.gdp, "type") and self.gdp.type
            else None
        )

    @computed_field
    @property
    def firmware(self) -> Optional[str]:
        """Get firmware version from GDP data."""
        try:
            if hasattr(self.gdp, "prog_ver") and self.gdp.prog_ver:
                return self.gdp.prog_ver.split(":")[0]
        except (IndexError, AttributeError):
            pass
        return None

    @computed_field
    @property
    def start_time(self) -> Optional[str]:
        """Get start time from GDP data."""
        try:
            if hasattr(self.gdp, "time") and hasattr(self.gdp, "date"):
                if self.gdp.time != "1980-01-01T00:00:00+00:00":
                    return f"{self.gdp.date}T{self.gdp.time}"
        except AttributeError:
            pass
        return None

    # =====================================================
    # Custom setters using __setattr__ override
    # =====================================================

    def __setattr__(self, name: str, value: Any) -> None:
        """Custom setters for computed properties."""

        # Setter for latitude
        if name == "latitude":
            if isinstance(value, str):
                try:
                    value = float(value.strip())
                except ValueError:
                    raise ValueError(f"Invalid latitude: {value}")
            # Update both the private field and GPS object if available
            super().__setattr__("_gps_lat", float(value))
            if hasattr(self, "gps") and hasattr(self.gps, "lat"):
                self.gps.lat = float(value)
            return

        # Setter for longitude
        if name == "longitude":
            if isinstance(value, str):
                try:
                    value = float(value.strip())
                except ValueError:
                    raise ValueError(f"Invalid longitude: {value}")
            # Update both the private field and GPS object if available
            super().__setattr__("_gps_lon", float(value))
            if hasattr(self, "gps") and hasattr(self.gps, "lon"):
                self.gps.lon = float(value)
            return

        # Setter for elevation
        if name == "elevation":
            if isinstance(value, str):
                try:
                    value = float(value.strip())
                except ValueError:
                    raise ValueError(f"Invalid elevation: {value}")
            super().__setattr__("_elevation", float(value))
            # Also update the main elevation field
            super().__setattr__("elevation", float(value))
            return

        # Setter for station
        if name == "station":
            if (
                hasattr(self, "rx")
                and hasattr(self.rx, "gdp_stn")
                and value is not None
            ):
                self.rx.gdp_stn = str(value)
            return

        # Default behavior for all other attributes
        super().__setattr__(name, value)

    def write_header(self):
        """
        Write .avg header lines

        :return: DESCRIPTION
        :rtype: TYPE

        """
        lines = [""]

        for key in self._header_keys:
            # Map g_p_s to gps for attribute access
            actual_key = key.replace("g_p_s", "gps")
            value = self.get_attr_from_name(actual_key)
            if isinstance(value, list):
                value = ",".join([f"{v:.1f}" for v in value])
            elif isinstance(value, (float)):
                value = f"{value:.7f}"
            elif isinstance(value, (int)):
                value = f"{value:.0f}"

            key = (
                key.replace("_", " ")
                .title()
                .replace(" ", "")
                .replace("MTEdit.", "MTEdit:")
            )

            lines.append(f"${key}={value.capitalize()}")

        return lines
