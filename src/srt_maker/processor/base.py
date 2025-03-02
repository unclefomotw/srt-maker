"""
Base processor module.

This module defines the base class for all processors.
"""

from abc import ABC, abstractmethod
from typing import List

from ..model import TextSegment


class BaseProcessor(ABC):
    """
    Base class for all processors.

    All processors should inherit from this class and implement the process method.
    """

    @abstractmethod
    def process(self, segments: List[TextSegment]) -> List[TextSegment]:
        """
        Process a list of text segments.

        Args:
            segments: List of TextSegment objects to process

        Returns:
            The processed list of TextSegment objects
        """
        pass