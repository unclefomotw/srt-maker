import json
from typing import Any, Dict, List, Optional

from ..model import TextSegment

# Define punctuation that indicates natural segment boundaries
PUNCTUATION = set(
    [
        ".",
        "!",
        "?",
        ",",
        ";",
        ":",
        "-",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        '"',
        "，",
        "。",
        "？",
        "！",
    ]
)


def process_file(input_file: str) -> List[TextSegment]:
    """
    Process an elevenlabs transcript file and return text segments.

    Args:
        input_file: Path to the input file containing elevenlabs transcript data

    Returns:
        List of TextSegment objects
    """
    # Read and parse the input file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Extract the words data
    words = data.get("words", [])

    # Process the words into segments
    return combine_into_segments(words)


def combine_into_segments(
    char_data: List[Dict[str, Any]],
    max_len: int = 40,
    punctuation: Optional[set] = None,
) -> List[TextSegment]:
    """
    Combines character-level transcript data into meaningful text segments.

    Args:
        char_data: List of dictionaries with keys 'text', 'start', and 'end'
        max_len: Maximum weighted length allowed in a segment.
                 ASCII characters count as 1, non-ASCII count as 2.
        punctuation: Optional set of characters to consider as punctuation.
                    If None, uses the default PUNCTUATION set.

    Returns:
        List of TextSegment objects
    """
    if not char_data:
        return []

    if punctuation is None:
        punctuation = PUNCTUATION

    # Helper function to calculate the weighted length of a character
    def char_weight(char: str) -> int:
        return 1 if ord(char) < 128 else 2

    segments = []
    current_text = ""
    current_weight = 0
    start_idx = 0

    # Track the last punctuation position for potential backoff
    last_punct_idx = -1
    last_punct_text = ""

    i = 0
    while i < len(char_data):
        char_item = char_data[i]
        char = char_item["text"]
        weight = char_weight(char)

        # Check if adding this character would exceed max_len
        if current_weight + weight > max_len:
            # Exception: if the next char is punctuation, include it
            if char in punctuation:
                current_text += char
                i += 1  # Move past this punctuation

                # Create segment with the punctuation included
                segments.append(
                    TextSegment(
                        text=current_text,
                        start_time=char_data[start_idx]["start"],
                        end_time=char_data[i - 1]["end"],
                    )
                )
            # If we have a punctuation to back off to, use that as the segment boundary
            elif last_punct_idx >= 0:
                segments.append(
                    TextSegment(
                        text=last_punct_text,
                        start_time=char_data[start_idx]["start"],
                        end_time=char_data[last_punct_idx]["end"],
                    )
                )
                # Start next segment after the punctuation
                i = last_punct_idx + 1
            else:
                # No punctuation to back off to, just create segment at max_len
                segments.append(
                    TextSegment(
                        text=current_text,
                        start_time=char_data[start_idx]["start"],
                        end_time=char_data[i - 1]["end"],
                    )
                )

            # Reset for next segment
            current_text = ""
            current_weight = 0

            # Skip leading whitespace in the next segment
            while i < len(char_data) and char_data[i]["text"].isspace():
                i += 1

            start_idx = i if i < len(char_data) else len(char_data) - 1
            last_punct_idx = -1
            last_punct_text = ""
            continue

        # Add character to current segment
        current_text += char
        current_weight += weight

        # Track punctuation for potential backoff
        if char in punctuation:
            last_punct_idx = i
            last_punct_text = current_text

        i += 1

    # Add any remaining text as the final segment
    if current_text:
        segments.append(
            TextSegment(
                text=current_text,
                start_time=char_data[start_idx]["start"],
                end_time=char_data[-1]["end"],
            )
        )

    return segments
