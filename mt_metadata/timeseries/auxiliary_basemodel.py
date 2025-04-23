# =====================================================
# Imports
# =====================================================
from enum import Enum
from typing import Annotated

from mt_metadata.timeseries.channel_basemodel import Channel
from pydantic import Field


# =====================================================


class Auxiliary(Channel):
    """
    Auxiliary channel class for storing auxiliary channel information.
    """
