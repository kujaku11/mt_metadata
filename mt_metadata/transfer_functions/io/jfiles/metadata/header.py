# =====================================================
# Imports
# =====================================================
from typing import Annotated

from pydantic import Field

from mt_metadata.base import MetadataBase

from . import BirrpAngles, BirrpBlock, BirrpParameters


# =====================================================
class Header(MetadataBase):
    title: Annotated[
        str,
        Field(
            default="",
            description="title of file",
            examples=["BIRRP Version 5 basic mode output"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    station: Annotated[
        str,
        Field(
            default="",
            description="station name",
            examples=["mt001"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    azimuth: Annotated[
        float,
        Field(
            default=0.0,
            description="rotation of full impedance tensor",
            examples=["0"],
            alias=None,
            json_schema_extra={
                "units": "degrees",
                "required": True,
            },
        ),
    ]

    birrp_parameters: Annotated[
        BirrpParameters,
        Field(
            default_factory=BirrpParameters,  # type: ignore
            description="BIRRP parameters",
            examples=["BirrpParameters(...)"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    data_blocks: Annotated[
        list[BirrpBlock],
        Field(
            default_factory=list,
            description="BIRRP data blocks",
            examples=["BirrpBlock(...)"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    angles: Annotated[
        list[BirrpAngles],
        Field(
            default_factory=list,
            description="BIRRP angles",
            examples=["BirrpAngles(...)"],
            alias=None,
            json_schema_extra={
                "units": None,
                "required": True,
            },
        ),
    ]

    def _read_header_line(self, line: str) -> dict:
        """
        Parse a single header line from the BIRRP output.

        Parameters
        ----------
        line : str
            A line from the BIRRP header.

        Returns
        -------
        dict
            A dictionary with the parsed key-value pairs.
        """

        line = " ".join(line[1:].strip().split())

        new_line = ""

        # need to restructure the string so its readable, at least the way
        # that birrp outputs the file
        e_find = 0
        for ii in range(len(line)):
            if line[ii] == "=":
                e_find = ii
                new_line += line[ii]
            elif line[ii] == " ":
                if abs(e_find - ii) == 1:
                    pass
                else:
                    new_line += ","
            else:
                new_line += line[ii]
        # now that we have a useful line, split it into its parts
        line_list = new_line.split(",")

        # try to split up the parts into a key=value setup
        # and try to make the values floats if they can be
        l_dict = {}
        key = "null"
        for ll in line_list:
            ll_list = ll.split("=")
            if len(ll_list) == 1:
                continue
            # some times there is just a list of numbers, need a way to read
            # that.
            if len(ll_list) != 2:
                if type(l_dict[key]) is not list:
                    l_dict[key] = list([l_dict[key]])
                try:
                    l_dict[key].append(float(ll))
                except ValueError:
                    l_dict[key].append(ll)
            else:
                key = ll_list[0]
                try:
                    value = float(ll_list[1])
                except ValueError:
                    value = ll_list[1]
                l_dict[key] = value
        return l_dict

    def read_header(self, j_lines: str) -> None:
        """
        Parsing the header lines of a j-file to extract processing information.

        Parameters
        ----------
        j_lines : str
            The lines of the j-file as a string.

        """

        self.data_blocks = []
        self.angles = []

        header_lines = [j_line for j_line in j_lines if "#" in j_line]
        self.title = header_lines[0][1:].strip()

        fn_count = -1
        theta_count = -1
        # put the information into a dictionary
        for h_line in header_lines[1:]:
            h_dict = self._read_header_line(h_line)
            for key, value in h_dict.items():
                if key in [
                    "filnam",
                    "nskip",
                    "nread",
                    "ncomp",
                    "indices",
                    "nfil",
                ]:
                    if key in ["nfil"]:
                        fn_count += 1
                    if len(self.data_blocks) != fn_count + 1:
                        self.data_blocks.append(BirrpBlock())
                    self.data_blocks[fn_count].update_attribute(key, value)
                # if its the line of angles, put them all in a list with a unique key
                elif key in ["theta1", "theta2", "phi"]:
                    if key == "theta1":
                        theta_count += 1
                    if len(self.angles) != theta_count + 1:
                        self.angles.append(BirrpAngles())
                    self.angles[theta_count].update_attribute(key, value)
                else:
                    self.birrp_parameters.update_attribute(key, value)

    def read_metadata(self, j_lines: str) -> None:
        """
        Read in the metadata of the station, or information of station
        logistics like: lat, lon, elevation

        Parameters
        ----------
        j_lines : str
            The lines of the j-file as a string.

        Not really needed for a birrp output since all values are nan's
        """

        metadata_lines = [j_line for j_line in j_lines if ">" in j_line]

        for m_line in metadata_lines:
            m_list = m_line.strip().split("=")
            m_key = m_list[0][1:].strip().lower()
            try:
                m_value = float(m_list[0].strip())
            except ValueError:
                m_value = 0.0
            self.update_attribute(m_key, m_value)
