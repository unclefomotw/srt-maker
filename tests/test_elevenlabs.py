from src.srt_maker.stt.elevenlabs import combine_into_segments


def test_empty_input():
    """Test with empty input data."""
    result = combine_into_segments([])
    assert result == []


def test_single_character():
    """Test with a single character."""
    char_data = [{"text": "A", "start": 0.0, "end": 1.0}]
    result = combine_into_segments(char_data)

    assert len(result) == 1
    assert result[0].text == "A"
    assert result[0].start_time == 0.0
    assert result[0].end_time == 1.0


def test_basic_segmentation():
    """Test basic segmentation with punctuation."""
    char_data = [
        {"text": "H", "start": 0.0, "end": 0.1},
        {"text": "e", "start": 0.1, "end": 0.2},
        {"text": "l", "start": 0.2, "end": 0.3},
        {"text": "l", "start": 0.3, "end": 0.4},
        {"text": "o", "start": 0.4, "end": 0.5},
        {"text": ",", "start": 0.5, "end": 0.6},
        {"text": " ", "start": 0.6, "end": 0.7},
        {"text": "w", "start": 0.7, "end": 0.8},
        {"text": "o", "start": 0.8, "end": 0.9},
        {"text": "r", "start": 0.9, "end": 1.0},
        {"text": "l", "start": 1.0, "end": 1.1},
        {"text": "d", "start": 1.1, "end": 1.2},
        {"text": "!", "start": 1.2, "end": 1.3},
    ]

    result = combine_into_segments(char_data)

    # Now expecting a single segment "Hello, world!" since it's below max_len
    assert len(result) == 1
    assert result[0].text == "Hello, world!"
    assert result[0].start_time == 0.0
    assert result[0].end_time == 1.3

    # Also test with a tiny max_len to force splitting
    result = combine_into_segments(char_data, max_len=5)
    assert len(result) == 2  # Should split into 2 segments with max_len=5
    assert result[0].text == "Hello,"
    assert result[1].text == "world!"


def test_max_length_constraint():
    """Test that segments respect the max_len parameter."""
    # Creating a string of 30 'a' characters
    char_data = []
    for i in range(30):
        char_data.append({"text": "a", "start": float(i), "end": float(i+1)})

    # Setting max_len to 10 should give us 3 segments
    result = combine_into_segments(char_data, max_len=10)
    assert len(result) == 3
    for segment in result:
        assert len(segment.text) == 10


def test_ascii_and_non_ascii_characters():
    """Test handling of ASCII and non-ASCII characters with different weights."""
    char_data = [
        {"text": "A", "start": 0.0, "end": 0.1},  # ASCII - weight 1
        {"text": "B", "start": 0.1, "end": 0.2},  # ASCII - weight 1
        {"text": "C", "start": 0.2, "end": 0.3},  # ASCII - weight 1
        {"text": "👍", "start": 0.3, "end": 0.4},  # Non-ASCII - weight 2
        {"text": "😊", "start": 0.4, "end": 0.5},  # Non-ASCII - weight 2
        {"text": ".", "start": 0.5, "end": 0.6},  # ASCII - weight 1 (punctuation)
        {"text": "D", "start": 0.6, "end": 0.7},  # ASCII - weight 1
        {"text": "E", "start": 0.7, "end": 0.8},  # ASCII - weight 1
        {"text": "世", "start": 0.8, "end": 0.9},  # Non-ASCII - weight 2
        {"text": "界", "start": 0.9, "end": 1.0},  # Non-ASCII - weight 2
    ]

    # With max_len=10, everything should be in a single segment
    # Total weight: 1+1+1+2+2+1+1+1+2+2 = 14
    result = combine_into_segments(char_data, max_len=14)
    assert len(result) == 1
    assert result[0].text == "ABC👍😊.DE世界"

    # With max_len=8, the period should create two segments
    # "ABC👍😊." (weights: 1+1+1+2+2+1=8) and "DE世界" (weights: 1+1+2+2=6)
    result = combine_into_segments(char_data, max_len=8)
    assert len(result) == 2
    assert result[0].text == "ABC👍😊."
    assert result[1].text == "DE世界"

    # With max_len=5, we should get even smaller segments
    result = combine_into_segments(char_data, max_len=5)
    assert len(result) == 4
    assert result[0].text == "ABC👍"
    assert result[1].text == "😊."
    assert result[2].text == "DE世"
    assert result[3].text == "界"


def test_combining_segments():
    """Test that segments are combined when possible."""
    char_data = [
        {"text": "H", "start": 0.0, "end": 0.1},
        {"text": "i", "start": 0.1, "end": 0.2},
        {"text": ".", "start": 0.2, "end": 0.3},
        {"text": " ", "start": 0.3, "end": 0.4},
        {"text": "B", "start": 0.4, "end": 0.5},
        {"text": "y", "start": 0.5, "end": 0.6},
        {"text": "e", "start": 0.6, "end": 0.7},
        {"text": "!", "start": 0.7, "end": 0.8},
    ]

    # With max_len=8, all characters should fit in a single segment
    result = combine_into_segments(char_data, max_len=8)
    assert len(result) == 1
    assert result[0].text == "Hi. Bye!"

    # With max_len=4, it should split into "Hi." and " Bye!"
    result = combine_into_segments(char_data, max_len=4)
    assert len(result) == 2
    assert result[0].text == "Hi."
    assert result[1].text == "Bye!"