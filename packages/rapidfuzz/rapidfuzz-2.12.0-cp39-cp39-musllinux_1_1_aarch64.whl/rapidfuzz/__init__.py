"""
rapid string matching library
"""
__author__: str = "Max Bachmann"
__license__: str = "MIT"
__version__: str = "2.12.0"

from rapidfuzz import distance, fuzz, process, string_metric, utils

__all__ = ["distance", "fuzz", "process", "string_metric", "utils"]
