"""
Unit tests for the TextProcessor class using pytest style.
"""



from src.srt_maker.model import TextSegment
from src.srt_maker.processor.text_processor import (TextProcessor,
                                                    TextTransformation)


# Tests for TextTransformation
def test_to_upper():
    """Test converting text to uppercase."""
    transformation = TextTransformation(to_upper=True)
    result = transformation.apply("hello world")
    assert result == "HELLO WORLD"


def test_to_lower():
    """Test converting text to lowercase."""
    transformation = TextTransformation(to_lower=True)
    result = transformation.apply("HELLO WORLD")
    assert result == "hello world"


def test_upper_and_lower_precedence():
    """Test that to_upper takes precedence over to_lower when both are set."""
    transformation = TextTransformation(to_upper=True, to_lower=True)
    result = transformation.apply("Hello World")
    assert result == "HELLO WORLD"


def test_replace_pattern():
    """Test replacing text with a regex pattern."""
    transformation = TextTransformation(
        replace_pattern=r"\b(\w+)\s+\1\b",
        replace_with=r"\1"
    )
    result = transformation.apply("hello hello world")
    assert result == "hello world"


def test_prefix():
    """Test adding a prefix to text."""
    transformation = TextTransformation(prefix="[START] ")
    result = transformation.apply("hello world")
    assert result == "[START] hello world"


def test_suffix():
    """Test adding a suffix to text."""
    transformation = TextTransformation(suffix=" [END]")
    result = transformation.apply("hello world")
    assert result == "hello world [END]"


def test_combined_transformations():
    """Test applying multiple transformations in a single TextTransformation."""
    transformation = TextTransformation(
        to_upper=True,
        prefix="[START] ",
        suffix=" [END]",
        replace_pattern=r"\s+",
        replace_with="_"
    )
    result = transformation.apply("hello world")
    assert result == "[START] HELLO_WORLD [END]"


# Tests for TextProcessor
def test_empty_process_list():
    """Test with an empty process list."""
    processor = TextProcessor([])
    segments = [
        TextSegment(text="Hello world", start_time=0.0, end_time=1.0)
    ]
    result = processor.process(segments)
    assert len(result) == 1
    assert result[0].text == "Hello world"
    assert result[0].start_time == 0.0
    assert result[0].end_time == 1.0


def test_single_transformation():
    """Test with a single transformation."""
    processor = TextProcessor([
        {"to_upper": True}
    ])
    segments = [
        TextSegment(text="Hello world", start_time=0.0, end_time=1.0)
    ]
    result = processor.process(segments)
    assert len(result) == 1
    assert result[0].text == "HELLO WORLD"


def test_multiple_transformations():
    """Test with multiple transformations applied in sequence."""
    processor = TextProcessor([
        {"to_upper": True},
        {"replace_pattern": r"\s+", "replace_with": "_"},
        {"suffix": " [PROCESSED]"}
    ])
    segments = [
        TextSegment(text="Hello world", start_time=0.0, end_time=1.0)
    ]
    result = processor.process(segments)
    assert len(result) == 1
    assert result[0].text == "HELLO_WORLD [PROCESSED]"


def test_multiple_segments():
    """Test processing multiple segments."""
    processor = TextProcessor([
        {"to_upper": True}
    ])
    segments = [
        TextSegment(text="Hello world", start_time=0.0, end_time=1.0),
        TextSegment(text="Another segment", start_time=1.0, end_time=2.0)
    ]
    result = processor.process(segments)
    assert len(result) == 2
    assert result[0].text == "HELLO WORLD"
    assert result[1].text == "ANOTHER SEGMENT"


def test_preserve_timing():
    """Test that timing information is preserved."""
    processor = TextProcessor([
        {"to_upper": True}
    ])
    segments = [
        TextSegment(text="Hello", start_time=1.5, end_time=2.75)
    ]
    result = processor.process(segments)
    assert result[0].start_time == 1.5
    assert result[0].end_time == 2.75
