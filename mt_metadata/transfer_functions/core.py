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
        self._transfer_function = self._initialize_transfer_function()

        self._rotation_angle = 0

        self.save_dir = Path.cwd()
        self._fn = None
        self.fn = fn
        
        self._dataset_attr_dict = {
            "survey": "survey_metadata.id",
            "project": "survey_metadata.project",
            "id": "station_metadata.id",
            "name": "station_metadata.geographic_name",
            "latitude": "station_metadata.location.latitude",
            "longitude": "station_metadata.location.longitude",
            "elevation": "station_metadata.location.elevation",
            "declination": "station_metadata.location.declination.value",
            "datum": "station_metadata.location.datum",
            "acquired_by": "station_metadata.acquired_by.author",
            "start": "station_metadata.time_period.start",
            "end": "station_metadata.time_period.end",
            "runs_processed": "station_metadata.run_names",
            }

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
        
        lines.append(f"\tImpedance:     {self.has_impedance()}")
        lines.append(f"\tTipper:        {self.has_tipper()}")

        if self.period is not None:
            lines.append(f"\tN Periods:     {len(self.period)}")

            lines.append("\tPeriod Range:")
            lines.append(f"\t\tMin:   {self.period.min():.5E} s")
            lines.append(f"\t\tMax:   {self.period.max():.5E} s")

            lines.append("\tFrequency Range:")
            lines.append(f"\t\tMin:   {1./self.period.max():.5E} Hz")
            lines.append(f"\t\tMax:   {1./self.period.min():.5E} Hz")

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
    
    def _initialize_transfer_function(self, periods=[1]):
        """
        create an empty x array for the data.  For now this accommodates
        a single processed station. 
        
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        # create an empty array for the transfer function
        tf = xr.DataArray(
            data=0 + 0j,
            dims=["period", "output", "input"],
            coords={"period": periods,
                    "output": ['ex', 'ey', 'hz'],
                    "input":["hx", "hy"]},
            name="transfer_function"
            )
        
        tf_err = xr.DataArray(
            data=0,
            dims=["period", "output", "input"],
            coords={"period": periods,
                    "output": ['ex', 'ey', 'hz'],
                    "input":["hx", "hy"]},
            name="error"
            )
        
        inv_signal_power_matrix = xr.DataArray(
            data=0,
            dims=["period", "output", "input"],
            coords={"period": periods,
                    "output": ["hx", "hy"],
                    "input":["hx", "hy"]},
            name="inverse_coherent_signal_power"
            )
        
        residual_covariance = xr.DataArray(
            data=0,
            dims=["period", "output", "input"],
            coords={"period": periods,
                    "output": ["ex", "ey"],
                    "input":["ex", "ey"]},
            name="residual_covariance"
            )
        
        # will need to add in covariance in some fashion
        return xr.Dataset({tf.name: tf, tf_err.name: tf_err})
        
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
        
    @property
    def dataset(self):
        """
        This will return an xarray dataset with proper metadata
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        
        for key, mkey in self._dataset_attr_dict.items():
            obj, attr = mkey.split(".", 1)
            value = getattr(self, obj).get_attr_from_name(attr)
            
            self._transfer_function.attrs[key] = value
        
        return self._transfer_function
    
    def has_impedance(self):
        """
        Check to see if the transfer function is not 0 and has 
        transfer function components
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords["output"].data.tolist()
        if "ex" in outputs or "ey" in outputs:
            if np.all(self._transfer_function.transfer_function.sel(input=["hx", "hy"], output=["ex", "ey"]).data == 0):
                return False
            return True
        return False
    
    @property    
    def impedance(self):
        """
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if self.has_impedance():
            z = self.dataset.transfer_function.sel(input=["hx", "hy"], output=["ex", "ey"])
            z.name = "impedance"
            z_err = self.dataset.error.sel(input=["hx", "hy"], output=["ex", "ey"])
            z_err.name = "impedance_error"
        
            return xr.Dataset({z.name: z, z_err.name: z_err})
        
    @impedance.setter
    def impedance(self, value):
        """
        Set the impedance from values
        
        :param value: DESCRIPTION
        :type value: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(value, (list, tuple, np.ndarray)):
            value = np.array(value)
            if self.has_impedance():
                if value.shape[0] != self.period.size:
                    self.logger.warning(
                        "New impedance shape %s not same as old %s, making new dataset.", 
                        value.shape,  self.impedance.impedance.data.shape)
                    
            else:
                self._transfer_function = self._initialize_transfer_function(np.arange(value.shape[0]))
            if value.shape[1:] != (2, 2):
                msg = "Impedance must be have shape (n_periods, 2, 2), not %s"
                self.logger.error(msg, value.shape)
                raise ValueError(msg % value.shape)
            self._transfer_function.transfer_function.data[:, 0:2, 0:2] = value
            
        if isinstance(value, xr.DataArray):
            # should test for shape
            if "period" not in value.coords.keys() or 'input' not in value.coords.keys():
                msg = "Coordinates must be period, output, input, not %s"
                self.logger.error(msg, list(value.coords.keys()))
                raise ValueError(msg % value.coords.keys())
            if 'ex' not in value.coords["output"].data.tolist() or \
                'ey' not in value.coords["output"].data.tolist():
                msg = "Output dimensions must be 'ex' and 'ey' not %s"
                self.logger.error(msg, value.coords["output"].data.tolist())
                raise ValueError(msg % value.coords["output"].data.tolist())
            if 'hx' not in value.coords["input"].data.tolist() or \
                'hy' not in value.coords["input"].data.tolist():
                msg = "Input dimensions must be 'hx' and 'hy' not %s"
                self.logger.error(msg, value.coords["input"].data.tolist())
                raise ValueError(msg % value.coords["input"].data.tolist())
            if self._transfer_function.transfer_function.data.shape[0] == 1 and not self.has_tipper():
                self._transfer_function = self._initialize_transfer_function(value.period)
            else:
                msg = "Reassigning is dangerous.  Should re-initialize transfer_function or make a new instance of TF"
                self.logger.error(msg)
                raise TFError(msg)
                
            self._transfer_function['transfer_function'].loc[dict(input=["hx", "hy"], output=["ex", "ey"])] = value 
        else:
            msg = "Data type %s not supported use a numpy array or xarray.DataArray"
            self.logger.error(msg, type(value))
            raise ValueError(msg % type(value))
        
    def has_tipper(self):
        """
        Check to see if the transfer function is not 0 and has 
        transfer function components
        
        :return: DESCRIPTION
        :rtype: TYPE

        """
        outputs = self._transfer_function.transfer_function.coords["output"].data.tolist()
        if "hz" in outputs:
            if np.all(self._transfer_function.transfer_function.sel(input=["hx", "hy"], output=["hz"]).data == 0):
                return False
            return True
        return False

    @property
    def tipper(self):
        """
        
        :return: DESCRIPTION
        :rtype: TYPE
    
        """
        if self.has_impedance():
            t = self.dataset.transfer_function.sel(input=["hx", "hy"], output=["hz"])
            t.name = "tipper"
            t_err = self.dataset.error.sel(input=["hx", "hy"], output=["hz"])
            t_err.name = "tipper_error"
        
            return xr.Dataset({t.name: t, t_err.name: t_err})

    @property
    def period(self):
        if self.has_impedance() or self.has_tipper():
            return self.dataset.period.data
        return None

    @period.setter
    def period(self, value):
        if self.period is not None:
            if len(value) != len(self.period):
                self.logger.warning("New periods are not the same size as old ones, making a new dataset")
                self._transfer_function = self._initialize_transfer_function(periods=value)
            else:
                self.dataset["period"] = value
        else:
            self._transfer_function = self._initialize_transfer_function(periods=value)
        return

    @property
    def frequency(self):
        if self.period is not None:
            return 1./self.period
        return None

    @frequency.setter
    def frequency(self, value):
        if self.period is not None:
            if len(value) != len(self.period):
                self.logger.warning("New periods are not the same size as old ones, making a new dataset")
                self._transfer_function = self._initialize_transfer_function(periods=1./value)
            else:
                self.dataset["period"] = 1./value
        else:
            self._transfer_function = self._initialize_transfer_function(periods=1./value)
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
