from typing import Dict, List, Protocol

from srt_maker.stt.models import TextSegment

from . import elevenlabs

__all__ = ['TextSegment', 'get_stt_processor']

# Protocol for STT service processors
class STTProcessor(Protocol):
    def __call__(self, input_file: str) -> List[TextSegment]:
        """
        Process an input file and return a list of text segments.

        Args:
            input_file: Path to the input file

        Returns:
            List of TextSegment objects
        """
        ...

# Registry of available STT services
_STT_PROCESSORS: Dict[str, STTProcessor] = {}

# Register the STT processors
def _register_processors():
    """Register all available STT processors."""

    # Register elevenlabs processor
    _STT_PROCESSORS['elevenlabs'] = elevenlabs.process_file

# Initialize the registry
_register_processors()

def get_stt_processor(service_name: str) -> STTProcessor:
    """
    Get the STT processor function by name.

    Args:
        service_name: Name of the STT service to use

    Returns:
        A function that processes an input file into text segments

    Raises:
        ValueError: If the requested service is not available
    """
    if service_name not in _STT_PROCESSORS:
        available_services = ", ".join(_STT_PROCESSORS.keys())
        raise ValueError(f"STT service '{service_name}' not available. Choose from: {available_services}")

    return _STT_PROCESSORS[service_name]

def register_stt_processor(name: str, processor: STTProcessor) -> None:
    """
    Register a new STT processor.

    Args:
        name: Name of the STT service
        processor: Function that processes an input file into text segments
    """
    _STT_PROCESSORS[name] = processor