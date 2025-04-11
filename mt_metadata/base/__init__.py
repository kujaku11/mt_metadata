"""
Base classes for holding metadata and schema objects
"""

from .metadata import MetadataBase
from .schema import get_schema, BaseDict

__all__ = ["MetadataBase", "get_schema", "BaseDict"]
