from dataclasses import dataclass


@dataclass
class TextSegment:
    """
    Data model representing a segment of text with start and end times.

    Attributes:
        text (str): The text content of the segment
        start_time (float): Start time in seconds
        end_time (float): End time in seconds
    """
    text: str
    start_time: float
    end_time: float

    def __repr__(self):
        return f"TextSegment({self.text}, {self.start_time:.2f} ~ {self.end_time:.2f})"
