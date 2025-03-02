# SRT Maker

A command-line tool for creating SRT subtitle files from various Speech-to-Text (STT) services.

## Features

- Generate SRT subtitle files from transcription data
- Support for multiple STT services (currently elevenlabs, with whisper as an example)
- Flexible design pattern for adding new STT services with different input file formats

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/srt-maker.git
cd srt-maker

# Install the package
pip install -e .
```

## Usage

```bash
# Generate SRT using the default elevenlabs service
srt-maker input_file -o output.srt

# Generate SRT using a specific STT service
srt-maker input_file -s elevenlabs -o output.srt
```

### STT - Elevenlabs

This only transforms the JSON file exported by the https://elevenlabs.io/ web app.  This script does NOT accept an audio file when using elevenlabs.  You can go to https://elevenlabs.io/app/speech-to-text and upload your audio/video files.


## Development

This project uses Poetry for dependency management. To get started with development, follow these steps:

1. **Install Poetry**: If you haven't already, install Poetry by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

2. **Install Dependencies**: Run the following command to install the project dependencies:
   ```bash
   poetry install
   ```

3. **Activate the Virtual Environment**: You can activate the virtual environment created by Poetry with:
   ```bash
   poetry shell
   ```

4. **Run the Application**: Use the following command to run the application:
   ```bash
   poetry run srt-maker <input_file> -s <stt_service>
   ```

5. **Add New Dependencies**: To add new dependencies, use:
   ```bash
   poetry add <package_name>
   ```

6. **Update Dependencies**: To update your dependencies, run:
   ```bash
   poetry update
   ```

7. **Lock File**: The `poetry.lock` file will be automatically generated and updated with the exact versions of the dependencies installed.

For more information on using Poetry, refer to the [Poetry documentation](https://python-poetry.org/docs/).

### Adding a New STT Service

The project uses a flexible design pattern that makes it easy to add new STT services with different input file formats:

1. Create a new Python file in the `src/srt_maker/stt/` directory (e.g., `new_service.py`)
2. Implement a `process_file` function that takes an input file path and returns a list of `TextSegment` objects
3. Register the new service in `src/srt_maker/stt/__init__.py`

Example implementation:

```python
# src/srt_maker/stt/new_service.py
import json
from typing import Any, Dict, List, Optional, Set
from .models import TextSegment

def process_file(input_file: str) -> List[TextSegment]:
    """
    Process a transcript file from your STT service and return text segments.

    Args:
        input_file: Path to the input file containing transcript data

    Returns:
        List of TextSegment objects
    """
    # Read and parse the input file according to your service's format
    with open(input_file, 'r') as file:
        data = json.load(file)  # Or any other format your service uses

    # Extract and process the data according to your service's format
    segments = []

    # Example: Create TextSegment objects from your data
    for item in data.get("your_segments", []):
        segments.append(TextSegment(
            text=item.get("text", ""),
            start_time=item.get("start_time", 0),
            end_time=item.get("end_time", 0)
        ))

    return segments
```

Then register the service:

```python
# In src/srt_maker/stt/__init__.py
# Add to the _register_processors function:
_STT_PROCESSORS['new_service'] = new_service.process_file
```

## License

MIT
