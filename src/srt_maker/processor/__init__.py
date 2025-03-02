"""
Processor package for SRT Maker.

This package contains processors that can be applied to text segments.
"""

import importlib
import logging
import os
import pkgutil
from typing import Dict, List, Optional, Type

import yaml

from ..model import TextSegment
from .base import BaseProcessor

logger = logging.getLogger(__name__)

# Registry to store processor classes
_processor_registry: Dict[str, Type[BaseProcessor]] = {}


def register_processor(processor_type: str):
    """
    Decorator to register a processor class.

    Args:
        processor_type: The type name for the processor
    """

    def decorator(cls):
        _processor_registry[processor_type] = cls
        return cls

    return decorator


def get_processor(processor_type: str) -> Optional[Type[BaseProcessor]]:
    """
    Get a processor class by type.

    Args:
        processor_type: The type name for the processor

    Returns:
        The processor class or None if not found
    """
    return _processor_registry.get(processor_type)


def load_processor_from_config(config_path: str) -> Optional[BaseProcessor]:
    """
    Load a processor from a YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file

    Returns:
        An initialized processor instance or None if loading fails
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        if not config or "type" not in config:
            logger.error(
                f"Invalid processor config in {config_path}: missing 'type' field"
            )
            return None

        processor_type = config.pop("type")
        processor_class = get_processor(processor_type)

        if not processor_class:
            logger.error(f"Unknown processor type '{processor_type}' in {config_path}")
            return None

        return processor_class(**config)
    except Exception as e:
        logger.error(f"Error loading processor from {config_path}: {str(e)}")
        return None


def process_segments(
    segments: List[TextSegment], processor_configs: List[str]
) -> List[TextSegment]:
    """
    Process text segments using a list of processor configurations.

    Args:
        segments: List of TextSegment objects to process
        processor_configs: List of paths to processor configuration files

    Returns:
        The processed list of TextSegment objects
    """
    processed_segments = segments

    for config_path in processor_configs:
        processor = load_processor_from_config(config_path)
        if processor:
            logger.info(f"Applying processor from: {config_path}")
            processed_segments = processor.process(processed_segments)
        else:
            logger.warning(f"Skipping invalid processor config: {config_path}")

    return processed_segments


# Import all modules in this package to register processors
def _import_processors():
    """Import all processor modules to register them."""
    package_dir = os.path.dirname(__file__)
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        if module_name != "base":  # Skip the base module
            importlib.import_module(f"{__name__}.{module_name}")


_import_processors()
