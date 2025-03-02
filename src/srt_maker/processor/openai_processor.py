"""
OpenAI processor module.

This module provides a processor that uses OpenAI's API to process text segments.
"""

import logging
from typing import List, Optional

import aisuite as ai
from dotenv import load_dotenv

from ..model import TextSegment
from . import register_processor
from .base import BaseProcessor

logger = logging.getLogger(__name__)


def load_prompt_from_file(file_path: str) -> str:
    """
    Load a prompt from a file.

    Args:
        file_path: Path to the prompt file

    Returns:
        The prompt text

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error(f"Prompt file not found: {file_path}")
        raise


@register_processor("openai")
class OpenAIProcessor(BaseProcessor):
    """
    Processor that uses OpenAI's API to process text segments.
    """

    def __init__(self, prompt: Optional[str] = None, prompt_file: Optional[str] = None, model: str = "openai:gpt-4o-mini"):
        """
        Initialize the OpenAI processor.

        Args:
            prompt: The system prompt text (takes precedence over prompt_file)
            prompt_file: Path to the prompt file (used if prompt is not provided)
            model: The model to use for processing (default: "openai:gpt-4o-mini")
        """
        self.model = model

        # Load environment variables from a .env file
        load_dotenv()

        # Initialize aisuite client
        self.client = ai.Client()

        # Set the system message from either the prompt or prompt_file
        if prompt:
            self.system_message = prompt
            self.source = "direct prompt"
        elif prompt_file:
            self.system_message = load_prompt_from_file(prompt_file)
            self.source = f"prompt file: {prompt_file}"
        else:
            logger.warning("No prompt or prompt_file provided, using empty prompt")
            self.system_message = ""
            self.source = "empty prompt"

    def process(self, segments: List[TextSegment]) -> List[TextSegment]:
        """
        Process text segments using OpenAI's API.

        Args:
            segments: List of TextSegment objects to process

        Returns:
            The processed list of TextSegment objects
        """
        logger.info(f"Processing {len(segments)} segments with OpenAI using {self.source}")

        processed_segments = []

        for i, segment in enumerate(segments):
            logger.debug(f"Processing segment {i+1}/{len(segments)}")

            try:
                # Call OpenAI API through aisuite
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_message},
                        {"role": "user", "content": segment.text}
                    ]
                )

                # Create a new segment with the processed text
                processed_text = segment.text
                if response.choices and response.choices[0].message.content:
                    processed_text = response.choices[0].message.content.strip()
                else:
                    logger.warning(f"Empty response for segment {i+1}")

                processed_segment = TextSegment(
                    text=processed_text,
                    start_time=segment.start_time,
                    end_time=segment.end_time
                )
                processed_segments.append(processed_segment)

            except Exception as e:
                logger.error(f"Error processing segment {i+1}: {str(e)}")
                # Keep the original segment in case of error
                processed_segments.append(segment)

        return processed_segments