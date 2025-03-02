from datetime import timedelta
from typing import List

from srt import Subtitle

from .stt import get_stt_processor


def generate_srt(input_file: str, stt_service: str = "elevenlabs") -> List[Subtitle]:
    """
    Generate SRT subtitles from an input file using the specified STT service.

    Args:
        input_file: Path to the input file containing transcript data
        stt_service: Name of the STT service to use (default: "elevenlabs")

    Returns:
        List of SRT Subtitle objects
    """
    # Get the appropriate STT processor function for the specified service
    processor = get_stt_processor(stt_service)

    # Process the input file to get text segments
    segments = processor(input_file)

    # Convert text segments to SRT subtitles
    return [Subtitle(index=i,
                     start=timedelta(seconds=segment.start_time),
                     end=timedelta(seconds=segment.end_time),
                     content=segment.text)
            for i, segment in enumerate(segments)]
