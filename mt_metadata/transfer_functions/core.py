# -*- coding: utf-8 -*-
"""
.. module:: TF
   :synopsis: The main container for transfer functions

.. moduleauthor:: Jared Peacock <jpeacock@usgs.gov>
"""

# ==============================================================================
from pathlib import Path
from copy import deepcopy

import numpy as np
import xarray as xr

from mt_metadata.transfer_functions.tf import Survey, Station, Run, Electric, Magnetic
from mt_metadata.utils.mt_logger import setup_logger
from mt_metadata.transfer_functions.io.readwrite import read_file, write_file


# =============================================================================
class TF:
    """
    Generic container to hold information about an electromagnetic
    transfer funtion
    """

    def __init__(self, fn=None, **kwargs):
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")

        # set metadata for the station
        self.survey_metadata = Survey()
        self.station_metadata = Station()
        self.station_metadata.run_list.append(Run())
        self.station_metadata.run_list[0].ex = Electric(component="ex")
        self.station_metadata.run_list[0].ey = Electric(component="ey")
        self.station_metadata.run_list[0].hx = Magnetic(component="hx")
        self.station_metadata.run_list[0].hy = Magnetic(component="hy")
        self.station_metadata.run_list[0].hz = Magnetic(component="hz")
        self.data = None

        self._rotation_angle = 0

        self.save_dir = Path.cwd()
        self._fn = None
        self.fn = fn

        # provide key words to fill values if an edi file does not exist
        for key in list(kwargs.keys()):
            setattr(self, key, kwargs[key])

    def __str__(self):
        lines = [f"Station: {self.station}", "-" * 50]
        lines.append(f"\tSurvey:        {self.survey_metadata.id}")
        lines.append(f"\tProject:       {self.survey_metadata.project}")
        lines.append(f"\tAcquired by:   {self.station_metadata.acquired_by.author}")
        lines.append(f"\tAcquired date: {self.station_metadata.time_period.start_date}")
        lines.append(f"\tLatitude:      {self.latitude:.3f}")
        lines.append(f"\tLongitude:     {self.longitude:.3f}")
        lines.append(f"\tElevation:     {self.elevation:.3f}")
        lines.append("\tDeclination:   ")
        lines.append(
            f"\t\tValue:     {self.station_metadata.location.declination.value}"
        )
        lines.append(
            f"\t\tModel:     {self.station_metadata.location.declination.model}"
        )
        # if self.Z.z is not None:
        #     lines.append("\tImpedance:     True")
        # else:
        #     lines.append("\tImpedance:     False")
        # if self.Tipper.tipper is not None:
        #     lines.append("\tTipper:        True")
        # else:
        #     lines.append("\tTipper:        False")

        # if self.Z.z is not None:
        #     lines.append(f"\tN Periods:     {len(self.Z.freq)}")

        #     lines.append("\tPeriod Range:")
        #     lines.append(f"\t\tMin:   {self.periods.min():.5E} s")
        #     lines.append(f"\t\tMax:   {self.periods.max():.5E} s")

        #     lines.append("\tFrequency Range:")
        #     lines.append(f"\t\tMin:   {self.frequencies.max():.5E} Hz")
        #     lines.append(f"\t\tMax:   {self.frequencies.min():.5E} Hz")

        return "\n".join(lines)

    def __repr__(self):
        lines = []
        lines.append(f"station='{self.station}'")
        lines.append(f"latitude={self.latitude:.2f}")
        lines.append(f"longitude={self.longitude:.2f}")
        lines.append(f"elevation={self.elevation:.2f}")

        return f"TF( {(', ').join(lines)} )"

    def __eq__(self, other):
        is_equal = True
        if not isinstance(other, TF):
            self.logger.info(f"Comparing object is not TF, type {type(other)}")
            is_equal = False
        if self.station_metadata != other.station_metadata:
            self.logger.info("Station metadata is not equal")
            is_equal = False
        if self.survey_metadata != other.survey_metadata:
            self.logger.info("Survey Metadata is not equal")
            is_equal = False
        if self.Z != other.Z:
            self.logger.info("Z is not equal")
            is_equal = False
        if self.Tipper != other.Tipper:
            self.logger.info("Tipper is not equal")
            is_equal = False
        return is_equal

    def copy(self):
        return deepcopy(self)

    # ==========================================================================
    # Properties
    # ==========================================================================
    @property
    def fn(self):
        """reference to original data file"""
        return self._fn

    @fn.setter
    def fn(self, value):
        """set file name"""
        try:
            self._fn = Path(value)
            if self._fn.exists():
                self.read_tf_file(self._fn)
            else:
                self.logger.warning(f"Could not find {self._fn} skip reading.")
        except TypeError:
            self._fn = None

    @property
    def latitude(self):
        """Latitude"""
        return self.station_metadata.location.latitude

    @latitude.setter
    def latitude(self, latitude):
        """
        set latitude making sure the input is in decimal degrees

        upon setting utm coordinates are recalculated
        """
        self.station_metadata.location.latitude = latitude

    @property
    def longitude(self):
        """Longitude"""
        return self.station_metadata.location.longitude

    @longitude.setter
    def longitude(self, longitude):
        """
        set longitude making sure the input is in decimal degrees

        upon setting utm coordinates are recalculated
        """
        self.station_metadata.location.longitude = longitude

    @property
    def elevation(self):
        """Elevation"""
        return self.station_metadata.location.elevation

    @elevation.setter
    def elevation(self, elevation):
        """
        set elevation, should be input as meters
        """
        self.station_metadata.location.elevation = elevation

    # @property
    # def Z(self):
    #     """mtpy.core.z.Z object to hole impedance tensor"""
    #     return self._Z

    # @Z.setter
    # def Z(self, z_object):
    #     """
    #     set z_object

    #     recalculate phase tensor and invariants, which shouldn't change except
    #     for strike angle
    #     """

    #     self._Z = z_object
    #     self._Z.compute_resistivity_phase()

    # @property
    # def Tipper(self):
    #     """mtpy.core.z.Tipper object to hold tipper information"""
    #     return self._Tipper

    # @Tipper.setter
    # def Tipper(self, t_object):
    #     """
    #     set tipper object

    #     recalculate tipper angle and magnitude
    #     """

    #     self._Tipper = t_object
    #     if self._Tipper is not None:
    #         self._Tipper.compute_amp_phase()
    #         self._Tipper.compute_mag_direction()

    @property
    def periods(self):
        if self.Z is not None:
            return 1.0 / self.Z.freq
        elif self.Tipper is not None:
            return 1.0 / self.Tipper.freq
        return None

    @periods.setter
    def periods(self, value):
        self.logger.warning(
            "Cannot set TF.periods directly," + " set either Z.freq or Tipper.freq"
        )
        return

    @property
    def frequencies(self):
        if self.Z is not None:
            return self.Z.freq
        elif self.Tipper is not None:
            return self.Tipper.freq
        return None

    @frequencies.setter
    def frequencies(self, value):
        self.logger.warning(
            "Cannot set TF.frequencies directly," + " set either Z.freq or Tipper.freq"
        )
        return

    @property
    def station(self):
        """station name"""
        return self.station_metadata.id

    @station.setter
    def station(self, station_name):
        """
        set station name
        """
        self.station_metadata.id = station_name

    # def plot_mt_response(self, **kwargs):
    #     """
    #     Returns a mtpy.imaging.plotresponse.PlotResponse object

    #     :Plot Response: ::

    #         >>> mt_obj = mt.TF(edi_file)
    #         >>> pr = mt.plot_mt_response()
    #         >>> # if you need more info on plot_mt_response
    #         >>> help(pr)

    #     """

    #     from mtpy.imaging import plot_mt_response

    #     # todo change this to the format of the new imaging API
    #     plot_obj = plot_mt_response.PlotMTResponse(
    #         z_object=self.Z,
    #         t_object=self.Tipper,
    #         pt_obj=self.pt,
    #         station=self.station,
    #         **kwargs,
    #     )

    # return plot_obj
    # # raise NotImplementedError

    def write_tf_file(
        self,
        fn=None,
        save_dir=None,
        fn_basename=None,
        file_type="edi",
        longitude_format="longitude",
        latlon_format="dms",
    ):
        """
        Write an mt file, the supported file types are EDI and XML.

        .. todo:: jtype and Gary Egberts z format

        :param fn: full path to file to save to
        :type fn: :class:`pathlib.Path` or string

        :param save_dir: full path save directory
        :type save_dir: string

        :param fn_basename: name of file with or without extension
        :type fn_basename: string

        :param file_type: [ 'edi' | 'xml' ]
        :type file_type: string

        :param longitude_format:  whether to write longitude as longitude or LONG.
                                  options are 'longitude' or 'LONG', default 'longitude'
        :type longitude_format:  string
        :param latlon_format:  format of latitude and longitude in output edi,
                               degrees minutes seconds ('dms') or decimal
                               degrees ('dd')
        :type latlon_format:  string

        :returns: full path to file
        :rtype: string

        :Example: ::

            >>> mt_obj.write_mt_file(file_type='xml')

        """

        if fn is not None:
            new_fn = Path(fn)
            self.save_dir = new_fn.parent
            fn_basename = new_fn.name

        if save_dir is not None:
            self.save_dir = Path(save_dir)

        if fn_basename is not None:
            fn_basename = Path(fn_basename)
            if fn_basename.suffix in ["", None]:
                fn_basename += f".{file_type}"

        if fn_basename is None:
            fn_basename = Path(f"{self.station}.{file_type}")

        if file_type is None:
            file_type = fn_basename.suffix.lower()[1:]
        if file_type not in ["edi", "xml", "j", "zmm", "zrr"]:
            msg = f"File type {file_type} not supported yet."
            self.logger.error(msg)
            raise TFError(msg)

        fn = self.save_dir.joinpath(fn_basename)

        return write_file(self, fn, file_type=file_type)

    def read_tf_file(self, fn, file_type=None):
        """

        Read an TF response file.

        .. note:: Currently only .edi, .xml, and .j files are supported

        :param fn: full path to input file
        :type fn: string

        :param file_type: ['edi' | 'j' | 'xml' | ... ]
                          if None, automatically detects file type by
                          the extension.
        :type file_type: string

        :Example: ::

            >>> import mtpy.core.mt as mt
            >>> mt_obj = mt.TF()
            >>> mt_obj.read_mt_file(r"/home/mt/mt01.xml")

        """

        mt_obj = read_file(fn, file_type=file_type)
        self.__dict__.update(mt_obj.__dict__)


# ==============================================================================
#             Error
# ==============================================================================


class TFError(Exception):
    pass
