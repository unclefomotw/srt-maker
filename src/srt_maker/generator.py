from datetime import timedelta
from typing import List, Optional

from srt import Subtitle

from .processor import process_segments
from .stt import get_stt_processor


def generate_srt(input_file: str, stt_service: str = "elevenlabs", processor_configs: Optional[List[str]] = None) -> List[Subtitle]:
    """
    Generate SRT subtitles from an input file using the specified STT service.

    Args:
        input_file: Path to the input file containing transcript data
        stt_service: Name of the STT service to use (default: "elevenlabs")
        processor_configs: Optional list of paths to processor configuration files

    Returns:
        List of SRT Subtitle objects
    """
    # Get the appropriate STT processor function for the specified service
    processor = get_stt_processor(stt_service)

    # Process the input file to get text segments
    segments = processor(input_file)

    # Process the segments if processor configs are provided
    if processor_configs:
        segments = process_segments(segments, processor_configs)

    # Convert text segments to SRT subtitles
    return [Subtitle(index=i,
                     start=timedelta(seconds=segment.start_time),
                     end=timedelta(seconds=segment.end_time),
                     content=segment.text)
            for i, segment in enumerate(segments)]
