### Electrode

# =======================================================================
# Imports
# =======================================================================
from typing import Annotated

from mt_metadata.common import Location, Instrument
from pydantic import Field


# =======================================================================
class Electrode(Location, Instrument):
    pass
