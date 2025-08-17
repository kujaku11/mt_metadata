# -*- coding: utf-8 -*-
"""
====================
zonge
====================
    * Tools for interfacing with MTFT24
    * Tools for interfacing with MTEdit


Created on Tue Jul 11 10:53:23 2013
@author: jpeacock-pr
"""

# ==============================================================================
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

from mt_metadata.timeseries import Electric, Magnetic, Run, Survey
from mt_metadata.transfer_functions.io.tools import get_nm_elev
from mt_metadata.transfer_functions.tf import Station

from .metadata import Header


# ==============================================================================
# deal with avg files output from mtedit
# ==============================================================================
class ZongeMTAvg:
    """
    deal with avg files output from mtedit
    """

    def __init__(self, fn=None, **kwargs):
        self.header = Header()

        self.info_keys = [
            "skip",
            "frequency",
            "e_magnitude",
            "b_magnitude",
            "z_magnitude",
            "z_phase",
            "apparent_resistivity",
            "apparent_resistivity_err",
            "z_phase_err",
            "coherency",
            "fc_use",
            "fc_try",
        ]
        self.info_fmt = []

        self.z = None
        self.z_err = None
        self.t = None
        self.t_err = None
        self.components = []

        self._comp_index_down = {
            "zxx": (0, 0),
            "zxy": (0, 1),
            "zyx": (1, 0),
            "zyy": (1, 1),
            "tzx": (0, 0),
            "tzy": (0, 1),
            "zxxr": (0, 0),
            "zxyr": (0, 1),
            "zyxr": (1, 0),
            "zyyr": (1, 1),
        }

        self._comp_index_up = {
            "zxx": (1, 1),
            "zxy": (1, 0),
            "zyx": (0, 1),
            "zyy": (0, 0),
            "tzx": (0, 1),
            "tzy": (0, 0),
            "zxxr": (1, 1),
            "zxyr": (1, 0),
            "zyxr": (0, 1),
            "zyyr": (0, 0),
        }

        self.freq_index_dict = None
        self.z_positive = "down"

        self.fn = fn

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_comp_index(self) -> dict[str, tuple[int, int]]:
        """
        get the correct component index dictionary based on z_positive

        Down assumes x is north, y is east

        Up assumes x is east, y is north
        """
        if self.z_positive == "down":
            return self._comp_index_down
        elif self.z_positive == "up":
            return self._comp_index_up
        else:
            raise ValueError("z_postiive must be either [ 'up' | 'down' ]")

    @property
    def fn(self) -> Path | None:
        return self._fn

    @fn.setter
    def fn(self, value: str | Path | None):
        if value is not None:
            self._fn = Path(value)
        else:
            self._fn = None

    def read(self, fn: str | Path | None = None, get_elevation: bool = False) -> None:
        """
        Read data from a file into the object as a pandas DataFrame

        Parameters
        ----------
        fn : str | Path | None, optional
            The file name to read from, by default None
        get_elevation : bool, optional
            Whether to get elevation data, by default False
        """

        if fn is not None:
            self.fn = Path(fn)

        if self.fn is None or not self.fn.exists():
            raise FileNotFoundError(f"File not found: {self.fn}")

        with self.fn.open("r") as fid:
            lines = fid.readlines()

        # read header
        data_lines = self.header.read_header(lines)

        data_list = []
        for line in data_lines:
            if "$" in line:
                key, comp = [ss.strip() for ss in line.split("=")]
            elif "skp" in line.lower() or len(line) < 2:
                continue
            else:
                line = line.replace("*", "0.50")
                values = [comp.lower()] + [float(ss.strip()) for ss in line.split(",")]
                entry = dict(
                    [
                        (key.lower(), value)
                        for key, value in zip(["comp"] + self.info_keys, values)
                    ]
                )
                data_list.append(entry)

        self.df = pd.DataFrame(data_list)

        self.frequency = self.df.frequency.unique()
        self.frequency.sort()
        self.n_freq = self.frequency.size
        self.components = self.df.comp.unique()

        self.freq_index_dict = dict([(ff, ii) for ii, ff in enumerate(self.frequency)])

        self.z, self.z_err = self._fill_z()
        self.t, self.t_err = self._fill_t()

        if self.header.elevation == 0 and get_elevation:
            if self.header.latitude != 0 and self.header.longitude != 0:
                self.header.elevation = get_nm_elev(
                    self.header.latitude, self.header.longitude
                )

    def to_complex(
        self, zmag: np.typing.NDArray, zphase: np.typing.NDArray
    ) -> tuple[np.typing.NDArray, np.typing.NDArray]:
        """
        Convert magnitude and phase to complex representation.

        Outputs of mtedit are magnitude and phase of z, convert to real and
        imaginary parts, phase is in milliradians.

        Parameters
        ----------
        zmag : np.typing.NDArray
            The magnitude array.
        zphase : np.typing.NDArray
            The phase array.

        Returns
        -------
        tuple[np.typing.NDArray, np.typing.NDArray]
            The real and imaginary parts of the complex representation.

        """

        if isinstance(zmag, np.ndarray):
            assert len(zmag) == len(zphase)
        zreal = zmag * np.cos((zphase / 1000))
        zimag = zmag * np.sin((zphase / 1000))
        return zreal, zimag

    def to_amp_phase(
        self, zreal: np.typing.NDArray, zimag: np.typing.NDArray
    ) -> tuple[np.typing.NDArray, np.typing.NDArray]:
        """
        Convert to amplitude and phase from real and imaginary

        Parameters
        ----------
        zreal : np.typing.NDArray
            The real part of the complex representation.
        zimag : np.typing.NDArray
            The imaginary part of the complex representation.

        Returns
        -------
        tuple[np.typing.NDArray, np.typing.NDArray]
            The amplitude and phase representation.

        """

        if isinstance(zreal, np.ndarray):
            assert len(zreal) == len(zimag)
        zphase = np.arctan2(zimag, zreal) * 1000
        zmag = np.sqrt(zreal**2 + zimag**2)

        return zmag, zphase

    def _fill_z(self) -> tuple[np.typing.NDArray, np.typing.NDArray]:
        """
        create Z array with data, need to take into account when the different
        components have different frequencies, sometimes one might get skipped.

        Parameters
        ----------
        None

        Returns
        -------
        tuple[np.typing.NDArray, np.typing.NDArray]
            The Z and Z error arrays.
        """

        z = np.zeros((self.n_freq, 2, 2), dtype=complex)
        z_err = np.ones((self.n_freq, 2, 2), dtype=float)

        comp_index = self._get_comp_index()

        for row in self.df[self.df.comp.str.startswith("z")].itertuples():
            ii, jj = comp_index[row.comp]
            f_index = self.freq_index_dict[row.frequency]
            z_real, z_imag = self.to_complex(row.z_magnitude, row.z_phase)
            z_real_error, z_imag_error = self.to_complex(
                (
                    np.sqrt(
                        (
                            (row.apparent_resistivity_err / 100)
                            * row.apparent_resistivity
                        )
                        * 5
                        * row.frequency
                    )
                ),
                row.z_phase_err,
            )

            z[f_index, ii, jj] = z_real + 1j * z_imag

            z_err[f_index, ii, jj] = np.sqrt(z_real_error**2 + z_imag_error**2)

        return z, z_err

    def _fill_t(
        self,
    ) -> tuple[np.typing.NDArray, np.typing.NDArray] | tuple[None, None]:
        """
        fill tipper values

        Returns
        -------
        tuple[np.typing.NDArray, np.typing.NDArray]
            The T and T error arrays.
        """

        if "tzx" not in self.df.comp.to_list():
            logger.debug(
                "No Tipper found in {self.fn.name}",
            )
            return None, None

        t = np.zeros((self.n_freq, 1, 2), dtype=complex)
        t_err = np.ones((self.n_freq, 1, 2), dtype=float)

        comp_index = self._get_comp_index()

        for row in self.df[self.df.comp.str.startswith("t")].itertuples():
            t_real, t_imag = self.to_complex(row.z_magnitude, row.z_phase)
            ii, jj = comp_index[row.comp]
            f_index = self.freq_index_dict[row.frequency]

            if self.z_positive == "up":
                t[f_index, ii, jj] = -1 * (t_real + t_imag * 1j)
            else:
                t[f_index, ii, jj] = t_real + t_imag * 1j
            # error estimation
            t_real_error, t_imag_error = self.to_complex(
                (
                    np.sqrt(
                        (
                            (row.apparent_resistivity_err / 100)
                            * row.apparent_resistivity
                        )
                    )
                ),
                row.z_phase_err,
            )
            t_err[f_index, ii, jj] = np.sqrt(t_real**2 + t_imag**2)

        return t, t_err

    @property
    def run_metadata(self) -> Run:
        rm = Run(id="001")
        rm.data_logger.id = self.header.instrument_id
        rm.data_logger.type = self.header.instrument_type
        rm.data_logger.manufacturer = "Zonge International"
        if self.header.firmware is not None:
            rm.data_logger.firmware.version = self.header.firmware
        if self.header.start_time is not None:
            rm.time_period.start = self.header.start_time

        if "zxy" in self.components or "zxxr" in self.components:
            rm.add_channel(self.ex_metadata)
            rm.add_channel(self.ey_metadata)
            rm.add_channel(self.hx_metadata)
            rm.add_channel(self.hy_metadata)

        if "tzx" in self.components or "rxxr" in self.components:
            rm.add_channel(self.hz_metadata)

        return rm

    @property
    def ex_metadata(self) -> Electric:
        ch = Electric(component="ex")
        if self.header._has_channel("zxy"):
            ch.dipole_length = self.header._comp_dict["zxy"]["rx"].length
            ch.measurement_azimuth = self.header._comp_dict["zxy"]["ch"].azimuth[0]
            ch.translated_azimuth = self.header._comp_dict["zxy"]["ch"].azimuth[0]
            ch.measurement_tilt = self.header._comp_dict["zxy"]["ch"].incl[0]
            ch.translated_tilt = self.header._comp_dict["zxy"]["ch"].incl[0]
            ch.channel_id = self.header._comp_dict["zxy"]["ch"].number[0]
            ch.time_period.start = self.header.start_time

        else:
            ch.dipole_length = self.header.rx.length
            ch.measurement_azimuth = self.header.rx.h_p_r[0]
            ch.translated_azimuth = self.header.rx.h_p_r[0]
            ch.channel_id = 4

        return ch

    @property
    def ey_metadata(self) -> Electric:
        ch = Electric(component="ey")
        if self.header._has_channel("zyx"):
            ch.dipole_length = self.header._comp_dict["zyx"]["rx"].length
            ch.measurement_azimuth = self.header._comp_dict["zyx"]["ch"].azimuth[0]
            ch.translated_azimuth = self.header._comp_dict["zyx"]["ch"].azimuth[0]
            ch.measurement_tilt = self.header._comp_dict["zyx"]["ch"].incl[0]
            ch.translated_tilt = self.header._comp_dict["zyx"]["ch"].incl[0]
            ch.channel_id = self.header._comp_dict["zyx"]["ch"].number[0]
            ch.time_period.start = self.header.start_time

        else:
            ch.dipole_length = self.header.rx.length
            ch.measurement_azimuth = self.header.rx.h_p_r[0] + 90
            ch.translated_azimuth = self.header.rx.h_p_r[0] + 90
            ch.channel_id = 5

        return ch

    @property
    def hx_metadata(self) -> Magnetic:
        ch = Magnetic(component="hx")
        if self.header._has_channel("zyx"):
            ch.measurement_azimuth = self.header._comp_dict["zyx"]["ch"].azimuth[1]
            ch.translated_azimuth = self.header._comp_dict["zyx"]["ch"].azimuth[1]
            ch.measurement_tilt = self.header._comp_dict["zyx"]["ch"].incl[1]
            ch.translated_tilt = self.header._comp_dict["zyx"]["ch"].incl[1]
            ch.sensor.id = self.header._comp_dict["zyx"]["ch"].number[1]
            ch.channel_id = 1
            ch.time_period.start = self.header.start_time

        else:
            ch.measurement_azimuth = self.header.rx.h_p_r[0]
            ch.translated_azimuth = self.header.rx.h_p_r[0]
            ch.channel_id = 1

        return ch

    @property
    def hy_metadata(self) -> Magnetic:
        ch = Magnetic(component="hy")
        if self.header._has_channel("zxy"):
            ch.measurement_azimuth = self.header._comp_dict["zxy"]["ch"].azimuth[1]
            ch.translated_azimuth = self.header._comp_dict["zxy"]["ch"].azimuth[1]
            ch.measurement_tilt = self.header._comp_dict["zxy"]["ch"].incl[1]
            ch.translated_tilt = self.header._comp_dict["zxy"]["ch"].incl[1]
            ch.sensor.id = self.header._comp_dict["zxy"]["ch"].number[1]
            ch.channel_id = 2
            ch.time_period.start = self.header.start_time

        else:
            ch.measurement_azimuth = self.header.rx.h_p_r[0] + 90
            ch.translated_azimuth = self.header.rx.h_p_r[0] + 90
            ch.channel_id = 2

        return ch

    @property
    def hz_metadata(self) -> Magnetic:
        ch = Magnetic(component="hz")
        if self.header._has_channel("tzx"):
            # Parse comma-separated values safely
            azimuth_values = self.header._comp_dict["tzx"]["ch"].azimuth
            incl_values = self.header._comp_dict["tzx"]["ch"].incl
            number_values = self.header._comp_dict["tzx"]["ch"].number

            # Extract second value from comma-separated strings
            if azimuth_values and "," in azimuth_values:
                try:
                    azimuth_val = float(azimuth_values.split(",")[1].strip())
                    ch.measurement_azimuth = azimuth_val
                    ch.translated_azimuth = azimuth_val
                except (IndexError, ValueError):
                    pass

            if incl_values and "," in incl_values:
                try:
                    incl_val = float(incl_values.split(",")[1].strip())
                    ch.measurement_tilt = incl_val
                    ch.translated_tilt = incl_val
                except (IndexError, ValueError):
                    pass

            if number_values and "," in number_values:
                try:
                    ch.sensor.id = number_values.split(",")[1].strip()
                except IndexError:
                    pass

            ch.channel_id = "3"
            if self.header.start_time:
                ch.time_period.start = self.header.start_time

        else:
            ch.measurement_azimuth = self.header.rx.h_p_r[-1]
            ch.translated_azimuth = self.header.rx.h_p_r[-1]
            ch.channel_id = "3"

        return ch

    @property
    def station_metadata(self) -> Station:
        sm = Station()

        sm.id = self.header.station
        sm.location.latitude = self.header.latitude
        sm.location.longitude = self.header.longitude
        sm.location.elevation = self.header.elevation
        sm.location.datum = self.header.datum.upper()

        sm.transfer_function.id = self.header.station
        sm.transfer_function.software.author = "Zonge International"
        sm.transfer_function.software.name = "MTEdit"
        sm.transfer_function.software.version = self.header.m_t_edit.version.split()[0]
        sm.transfer_function.software.last_updated = (
            self.header.m_t_edit.version.split()[-1]
        )

        for key, value in self.header.m_t_edit.to_dict(single=True).items():
            if "version" in key:
                continue
            sm.transfer_function.processing_parameters.append(f"mtedit.{key}={value}")

        sm.data_type = self.header.survey.type
        sm.add_run(self.run_metadata)
        sm.transfer_function.runs_processed = [self.run_metadata.id]
        if self.header.start_time is not None:
            sm.time_period.start = self.header.start_time

        return sm

    @station_metadata.setter
    def station_metadata(self, sm):
        self.header.station = sm.id
        self.header.latitdude = sm.location.latitude
        self.header.longitude = sm.location.longitude

        if hasattr(sm.run[0].ex):
            self.header.rx.length = sm.run[0].ex.dipole_length

    @property
    def survey_metadata(self) -> Survey:
        sm = Survey()
        sm.add_station(self.station_metadata)
        sm.update_time_period()
        return sm

    def _create_dataframe_from_arrays(self) -> pd.DataFrame:
        """
        Create a DataFrame from Z and T arrays for writing.
        This is used when data is available as arrays but not as a DataFrame.
        """
        if self.z is None or self.frequency is None:
            raise ValueError("No impedance data or frequency array available")

        data_list = []
        comp_index = self._get_comp_index()

        # Create data for each impedance component
        for comp, (i, j) in comp_index.items():
            if not comp.startswith(("z", "t")):
                continue

            for f_idx, freq in enumerate(self.frequency):
                if comp.startswith("z") and self.z is not None:
                    z_val = self.z[f_idx, i, j]
                    z_err_val = (
                        self.z_err[f_idx, i, j] if self.z_err is not None else 0.0
                    )

                    # Convert complex impedance to magnitude and phase
                    z_mag, z_phase = self.to_amp_phase(z_val.real, z_val.imag)

                    # Calculate apparent resistivity
                    app_res = 0.2 * (1.0 / freq) * (z_mag**2)
                    app_res_err = 2.0 * z_err_val / z_mag * 100 if z_mag != 0 else 0.0

                    entry = {
                        "comp": comp,
                        "skip": 2,  # Default skip value
                        "frequency": freq,
                        "e_magnitude": 1.0,  # Default E magnitude
                        "b_magnitude": 1.0,  # Default B magnitude
                        "z_magnitude": z_mag,
                        "z_phase": z_phase,
                        "apparent_resistivity": app_res,
                        "apparent_resistivity_err": app_res_err,
                        "z_phase_err": z_err_val * 1000,  # Convert to milliradians
                        "coherency": 0.9,  # Default coherency
                        "fc_use": 100,  # Default values
                        "fc_try": 200,
                    }
                    data_list.append(entry)

                elif comp.startswith("t") and self.t is not None:
                    t_val = self.t[f_idx, 0, j]  # Tipper is 1x2
                    t_err_val = (
                        self.t_err[f_idx, 0, j] if self.t_err is not None else 0.0
                    )

                    # Convert complex tipper to magnitude and phase
                    t_mag, t_phase = self.to_amp_phase(t_val.real, t_val.imag)

                    entry = {
                        "comp": comp,
                        "skip": 2,
                        "frequency": freq,
                        "e_magnitude": 1.0,
                        "b_magnitude": 1.0,
                        "z_magnitude": t_mag,
                        "z_phase": t_phase,
                        "apparent_resistivity": 1.0,  # Not applicable for tipper
                        "apparent_resistivity_err": t_err_val * 100,
                        "z_phase_err": t_err_val * 1000,
                        "coherency": 0.9,
                        "fc_use": 100,
                        "fc_try": 200,
                    }
                    data_list.append(entry)

        self.df = pd.DataFrame(data_list)
        self.components = self.df.comp.unique()

    def write(self, fn: str | Path) -> None:
        """
        Write an .avg file

        Parameters
        ----------
        fn : str or Path
            Filename to write to

        """

        if fn is not None:
            self.fn = Path(fn)

        # Create DataFrame from arrays if it doesn't exist
        if not hasattr(self, "df") or self.df is None or self.df.empty:
            self._create_dataframe_from_arrays()

        # Write header lines
        header_lines = self.header.write_header()

        # Group data by component and write each component section
        for comp in self.components:
            # Get component data
            comp_data = self.df[self.df.comp == comp].copy()
            if comp_data.empty:
                continue

            # Add component header line
            header_lines.append(f"$Rx.Cmp = {comp.capitalize()}")

            # Add component metadata lines if they exist in header
            if hasattr(self.header, "_comp_dict") and comp in self.header._comp_dict:
                comp_metadata = self.header._comp_dict[comp]
                # Add component specific metadata lines based on the structure
                # These would include lines like $Rx.Length, $Rx.Center, etc.
                # The exact structure depends on the header metadata
                for key, value in comp_metadata.items():
                    if key.startswith("rx_"):
                        header_key = key.replace("rx_", "$Rx.").replace("_", ".")
                        header_lines.append(f"{header_key}={value}")
                    elif key.startswith("ch_"):
                        header_key = key.replace("ch_", "$Ch.").replace("_", ".")
                        header_lines.append(f"{header_key}={value}")

            # Add data column header
            header_lines.append(
                "Skp,Freq,      E.mag,      B.mag,      Z.mag,      Z.phz,   "
                "ARes.mag,   ARes.%err,Z.perr,  Coher,   FC.NUse,FC.NTry"
            )

            # Sort data by frequency for this component
            comp_data = comp_data.sort_values("frequency")

            # Write data lines for this component
            for _, row in comp_data.iterrows():
                # Format each value according to the expected format to match the original file
                line = (
                    f"{int(row.skip)}, "
                    f"{row.frequency:11.4E}, "
                    f"{row.e_magnitude:11.4E}, "
                    f"{row.b_magnitude:11.4E}, "
                    f"{row.z_magnitude:11.4E}, "
                    f"{row.z_phase:6.1f}, "
                    f"  {row.apparent_resistivity:11.4E}, "
                    f"{row.apparent_resistivity_err:4.1f}, "
                    f"    {row.z_phase_err:6.1f}, "
                    f"  {row.coherency:5.3f}, "
                    f"  {int(row.fc_use):2}, "
                    f"    {int(row.fc_try):2}"
                )

                header_lines.append(line)

        # Write to file
        if self.fn is None:
            raise ValueError("No filename specified for writing")

        with self.fn.open("w") as fid:
            fid.write("\n".join(header_lines))
