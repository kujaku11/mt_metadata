"""
Base classes for holding metadata and schema objects
"""

from .metadata import Base
from .schema import get_schema, BaseDict

__all__ = ["Base", "get_schema", "BaseDict"]
