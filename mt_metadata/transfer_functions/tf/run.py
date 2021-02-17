# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import (
    Person,
    Provenance,
    TimePeriod,
    Fdsn,
    DataLogger,
    Electric,
    Magnetic,
    Auxiliary,
)

# =============================================================================
attr_dict = get_schema("run", SCHEMA_FN_PATHS)
attr_dict.add_dict(get_schema("fdsn", SCHEMA_FN_PATHS), "fdsn")
dl_dict = get_schema("instrument", SCHEMA_FN_PATHS)
dl_dict.add_dict(get_schema("timing_system", SCHEMA_FN_PATHS), "timing_system")
dl_dict.add_dict(get_schema("software", SCHEMA_FN_PATHS), "firmware")
dl_dict.add_dict(get_schema("battery", SCHEMA_FN_PATHS), "power_source")
attr_dict.add_dict(dl_dict, "data_logger")
attr_dict.add_dict(get_schema("time_period", SCHEMA_FN_PATHS), "time_period")
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS), "acquired_by", keys=["author", "comments"]
)
attr_dict.add_dict(
    get_schema("person", SCHEMA_FN_PATHS), "metadata_by", keys=["author", "comments"]
)
attr_dict.add_dict(
    get_schema("provenance", SCHEMA_FN_PATHS), "provenance", keys=["comments", "log"]
)
attr_dict.add_dict(get_schema("electric", SCHEMA_FN_PATHS), "ex")
attr_dict.add_dict(get_schema("electric", SCHEMA_FN_PATHS), "ey")
attr_dict.add_dict(get_schema("magnetic", SCHEMA_FN_PATHS), "hx")
attr_dict.add_dict(get_schema("magnetic", SCHEMA_FN_PATHS), "hy")
attr_dict.add_dict(get_schema("magnetic", SCHEMA_FN_PATHS), "hz")
attr_dict.add_dict(get_schema("magnetic", SCHEMA_FN_PATHS), "rrhx")
attr_dict.add_dict(get_schema("magnetic", SCHEMA_FN_PATHS), "rrhy")
attr_dict.add_dict(get_schema("auxiliary", SCHEMA_FN_PATHS), "temperature")
# =============================================================================
class Run(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self.id = None
        self.sample_rate = None
        self.comments = None
        self._n_chan = None
        self.data_type = None
        self.acquired_by = Person()
        self.provenance = Provenance()
        self.time_period = TimePeriod()
        self.data_logger = DataLogger()
        self.metadata_by = Person()
        self.fdsn = Fdsn()
        self._ex = Electric()
        self._ey = Electric()
        self._hx = Magnetic()
        self._hy = Magnetic()
        self._hz = Magnetic()
        self._rrhx = Magnetic()
        self._rrhy = Magnetic()
        self._temperature = Auxiliary()

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def n_channels(self):
        number = 0
        for channel in ["auxiliary", "electric", "magnetic"]:
            channel_list = getattr(self, "channels_recorded_{0}".format(channel))
            if channel_list is not None:
                number += len(channel_list)
        return number

    @property
    def channels_recorded_all(self):
        """
        
        :return: a list of all channels recorded
        :rtype: TYPE

        """

        all_channels = []
        for recorded in ["electric", "magnetic", "auxiliary"]:
            rec_list = getattr(self, f"channels_recorded_{recorded}")
            if rec_list is None:
                continue
            else:
                all_channels += rec_list

        return all_channels

    @property
    def channels_recorded_electric(self):
        rchannels = []
        for key, obj in self.__dict__.items():
            if isinstance(obj, Electric):
                if obj.component is None:
                    continue
                rchannels.append(obj.component)
        return rchannels

    @channels_recorded_electric.setter
    def channels_recorded_electric(self, value):
        if isinstance(value, str):
            value = [value]
        for comp in value:
            if comp.lower() in ["ex", "ey"]:
                setattr(self, comp, Electric(component=comp))
            else:
                msg = f"Input electric channel must be ex or ey, not {comp}"
                self.logger.error(msg)
                raise ValueError(msg)

    @property
    def channels_recorded_magnetic(self):
        rchannels = []
        for key, obj in self.__dict__.items():
            if isinstance(obj, Magnetic):
                if obj.component is None:
                    continue
                rchannels.append(obj.component)
        return rchannels

    @channels_recorded_magnetic.setter
    def channels_recorded_magnetic(self, value):
        if isinstance(value, str):
            value = [value]
        for comp in value:
            if comp.lower() in ["hx", "hy", "hz", "rrhx", "rrhy"]:
                setattr(self, comp, Magnetic(component=comp))
            else:
                msg = f"Input magnetic channel must be in [hx, hy, hz, rrhx, rrhy], not {comp}"
                self.logger.error(msg)
                raise ValueError(msg)

    @property
    def channels_recorded_auxiliary(self):
        rchannels = []
        for key, obj in self.__dict__.items():
            if isinstance(obj, Auxiliary):
                if obj.component is None:
                    continue
                rchannels.append(obj.component)
        return rchannels

    @channels_recorded_auxiliary.setter
    def channels_recorded_auxiliary(self, value):
        if isinstance(value, str):
            value = [value]
        for comp in value:
            setattr(self, comp, Auxiliary(component=comp))

    @property
    def ex(self):
        return self._ex

    @ex.setter
    def ex(self, value):
        if not isinstance(value, Electric):
            msg = f"Input must be metadata.Electric not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component is None:
            msg = "assuming initial empty Electric object"
            self.logger.debug(msg)
        elif value.component.lower() not in ["ex"]:
            msg = f"Input Electric.component must be ex not {value.component}"
            self.logger.error(msg)
            raise ValueError(msg)
        self._ex.from_dict(value.to_dict())

    @property
    def ey(self):
        return self._ey

    @ey.setter
    def ey(self, value):
        if not isinstance(value, Electric):
            msg = f"Input must be metadata.Electric not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component is None:
            msg = "assuming initial empty Electric object"
            self.logger.debug(msg)
        elif value.component.lower() not in ["ey"]:
            msg = f"Input Electric.component must be ey not {value.component}"
            self.logger.error(msg)
            raise ValueError(msg)
        self._ey.from_dict(value.to_dict())

    @property
    def hx(self):
        return self._hx

    @hx.setter
    def hx(self, value):
        if not isinstance(value, Magnetic):
            msg = f"Input must be metadata.Magnetic not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component is None:
            msg = "assuming initial empty Magnetic object"
            self.logger.debug(msg)
        elif value.component.lower() not in ["hx"]:
            msg = f"Input Magnetic.component must be hx not {value.component}"
            self.logger.error(ValueError)
            raise ValueError(msg)
        self._hx.from_dict(value.to_dict())

    @property
    def hy(self):
        return self._hy

    @hy.setter
    def hy(self, value):
        if not isinstance(value, Magnetic):
            msg = f"Input must be metadata.Magnetic not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component is None:
            msg = "assuming initial empty Magnetic object"
            self.logger.debug(msg)
        elif value.component.lower() not in ["hy"]:
            msg = f"Input Magnetic.component must be hy not {value.component}"
            self.logger.error(ValueError)
            raise ValueError(msg)
        self._hy.from_dict(value.to_dict())

    @property
    def hz(self):
        return self._hz

    @hz.setter
    def hz(self, value):
        if not isinstance(value, Magnetic):
            msg = f"Input must be metadata.Magnetic not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component is None:
            msg = "assuming initial empty Magnetic object"
            self.logger.debug(msg)
        elif value.component.lower() not in ["hz"]:
            msg = f"Input Magnetic.component must be hz not {value.component}"
            self.logger.error(ValueError)
            raise ValueError(msg)
        self._hz.from_dict(value.to_dict())

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if not isinstance(value, Auxiliary):
            msg = f"Input must be metadata.Magnetic not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component.lower() not in ["temperature"]:
            msg = f"Input Auxiliary.component must be temperature not {value.component}"
            self.logger.error(ValueError)
            raise ValueError(msg)
        self._temperature.from_dict(value.to_dict())

    @property
    def rrhx(self):
        return self._rrhx

    @rrhx.setter
    def rrhx(self, value):
        if not isinstance(value, Magnetic):
            msg = f"Input must be metadata.Magnetic not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component is None:
            msg = "assuming initial empty Magnetic object"
            self.logger.debug(msg)
        elif value.component.lower() not in ["rrhx"]:
            msg = f"Input Magnetic.component must be rrhx not {value.component}"
            self.logger.error(ValueError)
            raise ValueError(msg)
        self._rrhx.from_dict(value.to_dict())

    @property
    def rrhy(self):
        return self._rrhy

    @rrhy.setter
    def rrhy(self, value):
        if not isinstance(value, Magnetic):
            msg = f"Input must be metadata.Magnetic not {type(value)}"
            self.logger.error(msg)
            raise ValueError(msg)
        if value.component is None:
            msg = "assuming initial empty Magnetic object"
            self.logger.debug(msg)
        elif value.component.lower() not in ["rrhy"]:
            msg = f"Input Magnetic.component must be rrhy not {value.component}"
            self.logger.error(ValueError)
            raise ValueError(msg)
        self._rrhy.from_dict(value.to_dict())
