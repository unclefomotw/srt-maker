"""
Text processor module.

This module provides a simple text processor that can perform basic text transformations.
"""

import logging
import re
from typing import Any, Dict, List, Optional

from ..model import TextSegment
from . import register_processor
from .base import BaseProcessor

logger = logging.getLogger(__name__)


class TextTransformation:
    """
    A single text transformation with specific settings.
    """

    def __init__(
        self,
        to_upper: bool = False,
        to_lower: bool = False,
        replace_pattern: Optional[str] = None,
        replace_with: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None
    ):
        """
        Initialize a text transformation.

        Args:
            to_upper: Convert text to uppercase
            to_lower: Convert text to lowercase
            replace_pattern: Regex pattern to replace
            replace_with: Text to replace the pattern with
            prefix: Text to add at the beginning
            suffix: Text to add at the end
        """
        self.to_upper = to_upper
        self.to_lower = to_lower
        self.replace_pattern = replace_pattern
        self.replace_with = replace_with
        self.prefix = prefix
        self.suffix = suffix

        # Validate configuration
        if to_upper and to_lower:
            logger.warning("Both to_upper and to_lower are set to True. to_upper will take precedence.")

        if (replace_pattern and not replace_with) or (not replace_pattern and replace_with):
            logger.warning("Both replace_pattern and replace_with must be provided for replacement to work.")

    def apply(self, text: str) -> str:
        """
        Apply the transformation to a text.

        Args:
            text: The text to transform

        Returns:
            The transformed text
        """
        processed_text = text

        # Apply transformations
        if self.to_upper:
            processed_text = processed_text.upper()
        elif self.to_lower:
            processed_text = processed_text.lower()

        if self.replace_pattern and self.replace_with is not None:
            processed_text = re.sub(self.replace_pattern, self.replace_with, processed_text)

        if self.prefix:
            processed_text = f"{self.prefix}{processed_text}"

        if self.suffix:
            processed_text = f"{processed_text}{self.suffix}"

        return processed_text


@register_processor("text")
class TextProcessor(BaseProcessor):
    """
    Processor that performs basic text transformations.
    """

    def __init__(self, processes: List[Dict[str, Any]]):
        """
        Initialize the text processor with a list of transformation processes.

        Args:
            processes: List of transformation process configurations
        """
        self.transformations = []

        for i, process_config in enumerate(processes):
            try:
                transformation = TextTransformation(**process_config)
                self.transformations.append(transformation)
            except Exception as e:
                logger.error(f"Error initializing transformation {i+1}: {str(e)}")

    def process(self, segments: List[TextSegment]) -> List[TextSegment]:
        """
        Process text segments with the configured text transformations.

        Args:
            segments: List of TextSegment objects to process

        Returns:
            The processed list of TextSegment objects
        """
        logger.info(f"Processing {len(segments)} segments with TextProcessor using {len(self.transformations)} transformations")

        processed_segments = []

        for segment in segments:
            processed_text = segment.text

            # Apply each transformation in sequence
            for i, transformation in enumerate(self.transformations):
                processed_text = transformation.apply(processed_text)
                logger.debug(f"Applied transformation {i+1} to segment")

            # Create a new segment with the processed text
            processed_segment = TextSegment(
                text=processed_text,
                start_time=segment.start_time,
                end_time=segment.end_time
            )
            processed_segments.append(processed_segment)

        return processed_segments