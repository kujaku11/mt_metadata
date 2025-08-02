# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 13:53:55 2021

@author: jpeacock
"""
from typing import Annotated, ClassVar
from xml.etree import cElementTree as et

# =============================================================================
# Imports
# =============================================================================
import numpy as np
from loguru import logger
from pydantic import computed_field, Field, field_validator, ValidationInfo

from mt_metadata.base import MetadataBase
from mt_metadata.base.helpers import element_to_string


# =============================================================================


class TransferFunction(MetadataBase):
    """
    Deal with the complex XML format
    """

    _index_dict: ClassVar[dict] = {"hx": 0, "hy": 1, "ex": 0, "ey": 1, "hz": 0}
    _dtype_dict: ClassVar[dict] = {
        "complex": complex,
        "real": float,
        "complex128": "complex",
        "float64": "real",
    }
    _units_dict: ClassVar[dict] = {"z": "[mV/km]/[nT]", "t": "[]"}
    _name_dict: ClassVar[dict] = {
        "exhx": "zxx",
        "exhy": "zxy",
        "eyhx": "zyx",
        "eyhy": "zyy",
        "hzhx": "tx",
        "hzhy": "ty",
    }

    _array_dtypes_dict: ClassVar[dict] = {
        "period": float,
        "z": complex,
        "z_var": float,
        "z_invsigcov": complex,
        "z_residcov": complex,
        "t": complex,
        "t_var": float,
        "t_invsigcov": complex,
        "t_residcov": complex,
    }

    period: Annotated[
        np.typing.NDArray[np.float64] | None,
        Field(
            default_factory=lambda: np.empty((0,), dtype=np.float64),
            description="periods for estimates",
            examples=["0.01", "0.1", "1.0"],
            alias=None,
            json_schema_extra={
                "units": "second",
                "required": True,
            },
        ),
    ]
    z: Annotated[
        np.typing.NDArray[np.complex128] | None,
        Field(
            default_factory=lambda: np.empty((0, 2, 2), dtype=np.complex128),
            description="Estimates of the impedance tensor.",
            json_schema_extra={
                "units": "[mV/km]/[nT]",
                "required": False,
                "examples": ["1.0+0.0j", "0.5+0.5j"],
            },
        ),
    ]

    z_var: Annotated[
        np.typing.NDArray[np.float64] | None,
        Field(
            default_factory=lambda: np.empty((0, 2, 2), dtype=np.float64),
            description="Variance estimates for the impedance tensor.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["0.01", "0.1", "1.0"],
            },
        ),
    ]

    z_invsigcov: Annotated[
        np.typing.NDArray[np.complex128] | None,
        Field(
            default_factory=lambda: np.empty((0, 2, 2), dtype=np.complex128),
            description="Inverse of the covariance matrix for the impedance tensor.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1.0+0.0j", "0.5+0.5j"],
            },
        ),
    ]
    z_residcov: Annotated[
        np.typing.NDArray[np.complex128] | None,
        Field(
            default_factory=lambda: np.empty((0, 2, 2), dtype=np.complex128),
            description="Residual covariance matrix for the impedance tensor.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1.0+0.0j", "0.5+0.5j"],
            },
        ),
    ]
    t: Annotated[
        np.typing.NDArray[np.complex128] | None,
        Field(
            default_factory=lambda: np.empty((0, 1, 2), dtype=np.complex128),
            description="Estimates of the tipper tensor.",
            json_schema_extra={
                "units": "[]",
                "required": False,
                "examples": ["1.0+0.0j", "0.5+0.5j"],
            },
        ),
    ]
    t_var: Annotated[
        np.typing.NDArray[np.float64] | None,
        Field(
            default_factory=lambda: np.empty((0, 1, 2), dtype=np.float64),
            description="Variance estimates for the tipper tensor.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["0.01", "0.1", "1.0"],
            },
        ),
    ]
    t_invsigcov: Annotated[
        np.typing.NDArray[np.complex128] | None,
        Field(
            default_factory=lambda: np.empty((0, 2, 2), dtype=np.complex128),
            description="Inverse of the covariance matrix for the tipper tensor.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1.0+0.0j", "0.5+0.5j"],
            },
        ),
    ]
    t_residcov: Annotated[
        np.typing.NDArray[np.complex128] | None,
        Field(
            default_factory=lambda: np.empty((0, 1, 1), dtype=np.complex128),
            description="Residual covariance matrix for the tipper tensor.",
            json_schema_extra={
                "units": None,
                "required": False,
                "examples": ["1.0+0.0j", "0.5+0.5j"],
            },
        ),
    ]

    _write_dict: ClassVar[dict] = {
        "z": {"out": {0: "ex", 1: "ey"}, "in": {0: "hx", 1: "hy"}},
        "z_var": {"out": {0: "ex", 1: "ey"}, "in": {0: "hx", 1: "hy"}},
        "z_invsigcov": {
            "out": {0: "hx", 1: "hy"},
            "in": {0: "hx", 1: "hy"},
        },
        "z_residcov": {
            "out": {0: "ex", 1: "ey"},
            "in": {0: "ex", 1: "ey"},
        },
        "t": {"out": {0: "hz"}, "in": {0: "hx", 1: "hy"}},
        "t_var": {"out": {0: "hz"}, "in": {0: "hx", 1: "hy"}},
        "t_invsigcov": {
            "out": {0: "hx", 1: "hy"},
            "in": {0: "hx", 1: "hy"},
        },
        "t_residcov": {"out": {0: "hz"}, "in": {0: "hz"}},
    }

    _skip_derived_data: ClassVar[bool] = True
    _derived_keys: ClassVar[list] = [
        "rho",
        "rho_var",
        "phs",
        "phs_var",
        "tipphs",
        "tipphs_var",
        "tipmag",
        "tipmag_var",
        "zstrike",
        "zstrike_var",
        "zskew",
        "zskew_var",
        "zellip",
        "zellip_var",
        "tstrike",
        "tstrike_var",
        "tskew",
        "tskew_var",
        "tellip",
        "tellip_var",
        "indmag",
        "indmag_var",
        "indang",
        "indang_var",
    ]

    @field_validator(
        "period",
        "z",
        "z_var",
        "z_invsigcov",
        "z_residcov",
        "t",
        "t_var",
        "t_invsigcov",
        "t_residcov",
        mode="before",
    )
    @classmethod
    def validate_array(cls, value, info: ValidationInfo) -> np.ndarray | None:
        """
        Validate that the value is a numpy array or None.
        """
        if value is None:
            return None
        if isinstance(value, (list, tuple, np.ndarray)):
            return np.array(value, dtype=cls._array_dtypes_dict[info.field_name])
        else:
            msg = (
                f"input values must be an list, tuple, or np.ndarray, not {type(value)}"
            )
            logger.error(msg)
            raise TypeError(msg)

    def initialize_arrays(self, n_periods: int) -> None:
        """Initialize arrays for the transfer function data.

        :param n_periods: number of periods
        :type n_periods: int
        :return: None
        :rtype: None
        """
        self.period = np.zeros(n_periods)
        self.z = np.zeros((n_periods, 2, 2), dtype=self._array_dtypes_dict["z"])
        self.z_var = np.zeros_like(self.z, dtype=self._array_dtypes_dict["z_var"])
        self.z_invsigcov = np.zeros_like(
            self.z, dtype=self._array_dtypes_dict["z_invsigcov"]
        )
        self.z_residcov = np.zeros_like(
            self.z, dtype=self._array_dtypes_dict["z_residcov"]
        )
        self.t = np.zeros((n_periods, 1, 2), dtype=self._array_dtypes_dict["t"])
        self.t_var = np.zeros_like(self.t, dtype=self._array_dtypes_dict["t_var"])
        self.t_invsigcov = np.zeros(
            (n_periods, 2, 2), dtype=self._array_dtypes_dict["t_invsigcov"]
        )
        self.t_residcov = np.zeros(
            (n_periods, 1, 1), dtype=self._array_dtypes_dict["t_residcov"]
        )

    @computed_field
    @property
    def array_dict(self) -> dict:
        return {
            "z": self.z,
            "z_var": self.z_var,
            "z_invsigcov": self.z_invsigcov,
            "z_residcov": self.z_residcov,
            "t": self.t,
            "t_var": self.t_var,
            "t_invsigcov": self.t_invsigcov,
            "t_residcov": self.t_residcov,
        }

    @computed_field
    @property
    def n_periods(self) -> int:
        if self.period is not None:
            return self.period.size
        return 0

    def read_block(self, block: dict, period_index: int) -> None:
        """
        Read a period block which is root_dict["data"]["period"][ii]

        :param block: read a period block
        :type block: dict
        :param period_index: index of the period in the data
        :type period_index: int
        :return: None
        :rtype: None

        """

        for key in block.keys():
            comp = key.replace("_", "").replace(".", "_")
            if comp in ["value"]:
                continue
            elif self._skip_derived_data:
                if comp in self._derived_keys:
                    continue
            try:
                dtype = self._dtype_dict[block[key]["type"]]
            except KeyError:
                dtype = "unknown"

            try:
                value_list = block[key]["value"]
            except KeyError:
                logger.debug("No value for %s at period index %s", comp, period_index)
                continue

            if not isinstance(value_list, list):
                value_list = [value_list]
            for item in value_list:
                index_0 = self._index_dict[item["output"].lower()]
                index_1 = self._index_dict[item["input"].lower()]
                if dtype is complex:
                    value = item["value"].split()
                    value = complex(float(value[0]), float(value[1]))
                elif dtype in (float, int):
                    value = dtype(item["value"])
                elif dtype in ["unknown"]:
                    value = item["value"].split()
                    if len(value) > 1:
                        value = complex(float(value[0]), float(value[1]))
                    else:
                        value = float(value[0])

                self.array_dict[comp][period_index, index_0, index_1] = value

    def read_dict(self, root_dict: dict) -> None:
        """
        read root_dict["data"]
        This is the main data block for the transfer function data.
        :param root_dict: dictionary containing the transfer function data
        :type root_dict: dict
        :return: None
        :rtype: None

        """
        if self._skip_derived_data:
            logger.debug("Skipping derived quantities.")
        try:
            n_periods = int(float((root_dict["data"]["count"].strip())))
        except KeyError:
            n_periods = len(root_dict["data"]["period"])

        self.initialize_arrays(n_periods)
        for ii, block in enumerate(root_dict["data"]["period"]):
            self.period[ii] = float(block["value"])  # type: ignore[assignment]
            self.read_block(block, ii)

    def write_block(self, parent: et.Element, index: int) -> et.Element:
        """
        Write a data block

        :param parent: DESCRIPTION
        :type parent: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        period_element = et.SubElement(
            parent,
            "Period",
            {"value": f"{self.period[index]:.12e}", "units": "secs"},  # type: ignore[arg-type]
        )

        for key in self.array_dict.keys():
            if self.array_dict[key] is None:
                continue
            arr = np.nan_to_num(self.array_dict[key][index])

            # set zeros to empty value of 1E32
            if arr.dtype == complex:
                arr[np.where(arr == 0)] = 1e32 + 1e32j
            else:
                arr[np.where(arr == 0)] = 1e32

            attr_dict = {
                "type": self._dtype_dict[arr.dtype.name],
                "size": str(arr.shape)[1:-1].replace(",", ""),
            }
            try:
                attr_dict["units"] = self._units_dict[key]
            except KeyError:
                pass

            comp_element = et.SubElement(
                period_element, key.replace("_", ".").upper(), attr_dict
            )
            idx_dict = self._write_dict[key]
            shape = arr.shape
            for ii in range(shape[0]):
                for jj in range(shape[1]):
                    ch_out = idx_dict["out"][ii]
                    ch_in = idx_dict["in"][jj]
                    a_dict = {}
                    try:
                        a_dict["name"] = self._name_dict[ch_out + ch_in].capitalize()
                    except KeyError:
                        pass
                    a_dict["output"] = ch_out.capitalize()
                    a_dict["input"] = ch_in.capitalize()
                    ch_element = et.SubElement(comp_element, "value", a_dict)
                    ch_value = f"{arr[ii, jj].real:.6e}"
                    if attr_dict["type"] in ["complex"]:
                        ch_value = f"{ch_value} {arr[ii, jj].imag:.6e}"
                    ch_element.text = ch_value

        return period_element

    def to_xml(self, string: bool = False, required: bool = True) -> et.Element | str:
        """
        Write data blocks

        :param parent: DESCRIPTION
        :type parent: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        root = et.Element("Data", {"count": f"{self.n_periods:.0f}"})

        for index in range(self.period.size):  # type: ignore[attribute-error]
            self.write_block(root, index)

        if string:
            return element_to_string(root)
        return root
