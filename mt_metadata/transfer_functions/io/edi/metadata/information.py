# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 14:13:37 2021

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict

from pydantic import Field, PrivateAttr

from mt_metadata.base import MetadataBase


# ==============================================================================
# Info object
# ==============================================================================
class Information(MetadataBase):
    """
    Contain, read, and write info section of .edi file

    not much to really do here, but just keep it in the same format that it is
    read in as, except if it is in phoenix format then split the two paragraphs
    up so they are sequential.

    """

    info_dict: dict[str, str | list | None] = Field(
        default_factory=dict,
        description="Dictionary of information lines from the info section",
    )
    _phoenix_col_width: int = PrivateAttr(default=38)
    _phoenix_file: bool = PrivateAttr(default=False)
    _empower_file: bool = PrivateAttr(default=False)
    _phoenix_translation_dict: dict[str, str | list] = PrivateAttr(
        default_factory=lambda: {
            "survey": "survey.id",
            "company": "station.acquired_by.organization",
            "job": "survey.project",
            "hardware": "run.data_logger.model",
            "mtuprog version": "run.data_logger.firmware.version",
            "xpr weighting": "processing_parameter",
            "hx sen": "run.hx.sensor.id",
            "hy sen": "run.hy.sensor.id",
            "hz sen": "run.hz.sensor.id",
            "rx sen": "run.rrhx.sensor.id",
            "ry sen": "run.rrhy.sensor.id",
            "stn number": "station.id",
            "mtu-box serial number": "run.data_logger.id",
            "ex pot resist": "run.ex.contact_resistance.start",
            "ey pot resist": "run.ey.contact_resistance.start",
            "ex voltage": ["run.ex.ac.start", "run.ex.dc.start"],
            "ey voltage": ["run.ey.ac.start", "run.ey.dc.start"],
            "start-up": "station.time_period.start",
            "end-time": "station.time_period.end",
        }
    )

    _translation_dict: dict[str, str] = PrivateAttr(
        default_factory=lambda: {
            "operator": "run.acquired_by.author",
            "adu_serial": "run.data_logger.id",
            "e_azimuth": "run.ex.measurement_azimuth",
            "ex_len": "run.ex.dipole_length",
            "ey_len": "run.ey.dipole_length",
            "ex_resistance": "run.ex.contact_resistance.start",
            "ey_resistance": "run.ey.contact_resistance.start",
            "h_azimuth": "run.hx.measurement_azimuth",
            "hx": "run.hx.sensor.id",
            "hy": "run.hy.sensor.id",
            "hz": "run.hz.sensor.id",
            "hx_resistance": "run.hx.h_field_max.start",
            "hy_resistance": "run.hy.h_field_max.start",
            "hz_resistance": "run.hz.h_field_max.start",
            "algorithmname": "transfer_function.software.name",
            "ndec": "processing_parameter",
            "nfft": "processing_parameter",
            "ntype": "processing_parameter",
            "rrtype": "processing_parameter",
            "removelargelines": "processing_parameter",
            "rotmaxe": "processing_parameter",
            "project": "survey.project",
            "processedby": "transfer_function.processed_by.name",
            "processingsoftware": "transfer_function.software.name",
            "processingtag": "transfer_function.id",
            "signconvention": "transfer_function.sign_convention",
            "sitename": "station.geographic_name",
            "survey": "survey.id",
            "year": "survey.time_period.start_date",
            "runlist": "transfer_function.runs_processed",
            "remotesite": "transfer_function.remote_references",
            "remoteref": "transfer_function.processing_parameters",
        }
    )
    _empower_translation_dict: dict[str, str] = PrivateAttr(
        default_factory=lambda: {
            "processingsoftware": "transfer_function.software.name",
            "sitename": "station.geographic_name",
            "year": "survey.time_period.start_date",
            "process_date": "transfer_function.processed_date",
            "declination": "station.location.declination.value",
            "tag": "component",
            "length": "dipole_length",
            "ac": "ac.end",
            "dc": "dc.end",
            "negative_res": "contact_resistance.start",
            "positive_res": "contact_resistance.end",
            "sensor_type": "sensor.model",
            "azimuth": "measured_azimuth",
            "sensor_serial": "sensor.id",
            "cal_name": "comments",
            "saturation": "comments",
            "instrument_type": "model",
        }
    )

    def __str__(self):
        return "".join(self.write_info())

    def __repr__(self):
        return self.__str__()

    def read_info(self, edi_lines: list[str]) -> None:
        """
        Read information section and parse directly to info_dict.

        Parameters
        ----------
        edi_lines : list[str]
            List of lines from the EDI file.
        """
        self.info_dict = OrderedDict()
        self._phoenix_file = False
        self._empower_file = False

        # 1. Identify the info section and detect format in a single pass
        info_section = []
        info_started = False

        for line in edi_lines:
            line = line.strip()

            # Check for start/end markers
            if ">info" in line.lower():
                info_started = True
                continue
            elif info_started and line and line[0] == ">":
                break

            # Collect info lines for processing
            if info_started and line:
                # Detect format while collecting
                if "run information station" in line.lower():
                    self._phoenix_file = True
                elif "empower data" in line.lower():
                    self._empower_file = True

                info_section.append(line)

        # 2. Parse lines based on detected format
        if self._empower_file:
            self._parse_empower_info(info_section)
        elif self._phoenix_file:
            self._parse_phoenix_info(info_section)
        else:
            self._parse_standard_info(info_section)

    def _get_separator(self, line: str) -> str | None:
        """Find the key-value separator in a line."""
        sep = None
        if line.count(":") > 0 and line.count("=") > 0:
            if line.find(":") < line.find("="):
                sep = ":"
            else:
                sep = "="

        elif line.count(":") >= 1:
            sep = ":"
            # colon_find = line.find(":")
        elif line.count("=") >= 1:
            sep = "="

        return sep

    def _parse_standard_info(self, info_lines: list[str]) -> None:
        """Parse standard format EDI info lines directly to info_dict."""
        for line in info_lines:
            # Skip empty lines and section headers
            if not line or "<" in line or ">" in line:
                continue

            # Get separator and parse key/value
            sep = self._get_separator(line)
            if not sep:
                self.info_dict[line.strip()] = ""
                continue

            parts = line.split(sep, 1)
            if len(parts) != 2:
                continue

            key = parts[0].strip().lower()
            value = parts[1].strip()

            # Handle list values
            if value.startswith("[") and value.endswith("]"):
                value = [
                    v.strip()
                    for v in value[1:-1]
                    .replace(",", " ")
                    .replace(";", " ")
                    .replace(":", " ")
                    .split()
                ]

            # Apply translation dictionary
            std_key = self._translation_dict.get(key)

            if std_key:
                # Handle special processing parameters
                if std_key == "processing_parameter":
                    if "transfer_function.processing_parameters" not in self.info_dict:
                        self.info_dict["transfer_function.processing_parameters"] = []
                    self.info_dict["transfer_function.processing_parameters"].append(
                        f"{key}={value}"
                    )
                else:
                    self.info_dict[std_key] = value
            else:
                # Store unrecognized keys with original name
                self.info_dict[key] = value

    def _parse_phoenix_info(self, info_lines: list[str]) -> None:
        """Parse Phoenix format EDI info lines efficiently."""
        for line in info_lines:
            # Process each line for potential multi-column content
            is_multi_column, columns = self._split_phoenix_columns(line)

            for column in columns:
                sep = self._get_separator(column)
                if not sep:
                    continue

                parts = column.split(sep, 1)
                if len(parts) != 2:
                    continue

                key = parts[0].strip().lower()
                value = parts[1].strip()
                if value.count("  ") > 0:
                    value = value.split(" ")[0].strip()  # Apply Phoenix translation
                self._apply_phoenix_translation(key, value)

    def _parse_empower_info(self, info_lines: list[str]) -> None:
        """
        Parse Empower format EDI info lines efficiently.

        Empower format has a hierarchical structure with sections for
        general info, electrics, and magnetics.
        """
        section = "general"
        component = None

        # Process all lines and handle hierarchical structure
        for line in info_lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Check for section headers
            if line.lower() == "electrics":
                section = "electrics"
                continue
            elif line.lower() == "magnetics":
                section = "magnetics"
                continue

            # Component-level headers (e.g., "E1", "H1")
            if section in ["electrics", "magnetics"]:
                if self._get_separator(line) is None:
                    component = line.strip().lower()
                    continue

            # Regular key-value pairs
            sep = self._get_separator(line)
            if not sep:
                continue

            parts = line.split(sep, 1)
            if len(parts) != 2:
                continue

            key = parts[0].strip().lower()
            value = parts[1].strip()

            # Build the key based on section/component context
            std_key = self._get_empower_std_key(section, component, key)

            if std_key:
                if "comments" in std_key:
                    original_value = self.info_dict.get(std_key, [])
                    if not isinstance(original_value, list):
                        original_value = [original_value]
                    original_value.append(f"{key}={value}")
                    value = original_value
                self.info_dict[std_key] = value
            else:
                # For unrecognized keys, store with section prefix
                context_key = (
                    f"{section}.{component}.{key}" if component else f"{section}.{key}"
                )
                self.info_dict[context_key] = value

    def _get_empower_std_key(
        self, section: str, component: str | None, key: str
    ) -> str | None:
        """
        Get standardized key for Empower format based on section and component context.

        Parameters
        ----------
        section : str
            Current section ("general", "electrics", "magnetics")
        component : str
            Current component (e.g., "e1", "h1", None)
        key : str
            Original key name

        Returns
        -------
        str or None
            Standardized key name or None if no mapping found
        """
        # Handle general section keys
        if section == "general":
            mapped_key = self._empower_translation_dict.get(key)
            if mapped_key:
                return mapped_key
            return None

        # Handle component-specific keys
        if not component:
            return None

        # Map component names to standard names
        component_map = {
            "e1": "ex",
            "e2": "ey",
            "h1": "hx",
            "h2": "hy",
            "h3": "hz",
        }

        std_component = component_map.get(component, component)

        # Create run-prefixed attribute key
        attribute_key = self._empower_translation_dict.get(key)
        if attribute_key:
            return f"run.{std_component}.{attribute_key}"

        # Special cases for component key
        if key == "component" and component.startswith("h"):
            # Component is handled by return key mapping
            return None
        elif key == "component" and component.startswith("e"):
            return f"run.{std_component}.component"

        # Handle special cases for comments field
        if key in ["cal_name", "saturation"]:
            # Append to comments field
            comments_key = f"run.{std_component}.comments"

            # # If comments already exist, append to them
            # existing = self.info_dict.get(comments_key, "")
            # if existing:
            #     self.info_dict[comments_key] = f"{existing},{key}={value}"
            #     return None  # Return None to prevent overwriting

            return comments_key

        # Default case: use run.component.key format
        return f"run.{std_component}.{key}"

    def _split_phoenix_columns(self, line: str) -> tuple[bool, list[str]]:
        """
        Split Phoenix line into columns based on whitespace gaps and separators.
        Returns (is_multi_column, list_of_columns)
        """
        import re

        # Check for basic indicators first
        if not line or len(line) < 10:
            return False, [line]

        # Look for patterns that indicate multi-column format
        parts = [(m.group(), m.start()) for m in re.finditer(r"\S+", line)]

        if len(parts) < 4:  # Need at least 4 words for two key-value pairs
            return False, [line]

        # Calculate word gaps
        gaps = [
            parts[i + 1][1] - (parts[i][1] + len(parts[i][0]))
            for i in range(len(parts) - 1)
        ]

        # Find the largest gap
        if not gaps:
            return False, [line]

        max_gap = max(gaps)
        if max_gap <= 3:  # Too small to be a column separator
            return False, [line]

        max_gap_idx = gaps.index(max_gap)
        split_pos = parts[max_gap_idx + 1][1]

        # Check if we have key-value pairs on both sides
        left_text = line[:split_pos].strip()
        right_text = line[split_pos:].strip()

        # Verify both columns have separators
        left_has_sep = ":" in left_text or "=" in left_text
        right_has_sep = ":" in right_text or "=" in right_text

        if left_has_sep and right_has_sep:
            return True, [left_text, right_text]

        return False, [line]

    def _apply_phoenix_translation(self, key: str, value: str) -> None:
        """Apply Phoenix-specific translations and handle special cases."""

        # Remove units for resistance values
        if "Pot Resist".lower() in key.lower() and isinstance(value, str):
            value = value.split()[0]

        # Handle voltage with AC/DC
        if "voltage" in key.lower() and isinstance(value, str):
            comps = value.replace(" ", "").split(",")
            for comp in comps:
                if "=" in comp:
                    typ, val = comp.split("=")
                    typ = typ.lower()
                    val = val.replace("mV", "")
                    std_key = f"run.{key[0:2].lower()}.{typ}.start"
                    self.info_dict[std_key] = val
            return

        std_key = self._phoenix_translation_dict.get(key.lower(), "phoenix_attribute")
        if std_key:
            if isinstance(std_key, list):
                for kk in std_key:
                    self.info_dict[kk] = value
            else:
                self.info_dict[std_key] = value
            # Add Phoenix sensor metadata for Hx/Hy/Hz
            if " sen" in key.lower():
                comp = key.lower().split()[0]
                self.info_dict[f"{comp}.sensor.manufacturer"] = "Phoenix Geophysics"
                self.info_dict[f"{comp}.sensor.type"] = "Induction Coil"
        else:
            self.info_dict[key] = value

    def write_info(self) -> list[str]:
        """
        write out information
        """

        info_lines = [">INFO\n"]

        for key, value in self.info_dict.items():
            if key is None:
                continue
            if value in ["", None]:
                info_lines.append(f"{' '*4}{key}\n")
            elif isinstance(value, list):
                value = ",".join(value)
            elif isinstance(value, str):
                value = value.strip()
            info_lines.append(f"{' '*4}{key}={value}\n")

        return info_lines
