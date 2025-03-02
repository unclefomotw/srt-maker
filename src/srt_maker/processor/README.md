# SRT Maker Processors

This package contains processors that can be applied to text segments in SRT files.

## Using Processors

Processors are configured using YAML files. Each processor has a specific type and configuration options.

To use processors with the SRT Maker CLI, use the `-p` or `--processors` option:

```bash
srt-maker input.mp3 -p processor1.yaml processor2.yaml
```

Multiple processors can be specified, and they will be applied in the order they are listed.

## Available Processors

### OpenAI Processor

The OpenAI processor uses OpenAI's API to process text segments.

Example configuration:

```yaml
type: openai
prompt: "You are a helpful assistant that cleans up and improves subtitle text."
model: openai:gpt-4o-mini
```

Or using a prompt file:

```yaml
type: openai
prompt_file: prompts/clean_text.txt
model: openai:gpt-4o-mini
```

Configuration options:
- `prompt`: The system prompt text (takes precedence over prompt_file)
- `prompt_file`: Path to a file containing the system prompt (used if prompt is not provided)
- `model`: The model to use (default: "openai:gpt-4o-mini")

### Text Processor

The Text processor performs basic text transformations through a sequence of processes.

Example configuration:

```yaml
type: text
processes:
  - to_lower: true
    replace_pattern: '\s+'
    replace_with: ' '
  - prefix: '- '
    suffix: ''
```

Configuration options:
- `processes`: A list of transformation processes to apply in sequence. Each process can have the following options:
  - `to_upper`: Convert text to uppercase (default: false)
  - `to_lower`: Convert text to lowercase (default: false)
  - `replace_pattern`: Regex pattern to replace
  - `replace_with`: Text to replace the pattern with
  - `prefix`: Text to add at the beginning
  - `suffix`: Text to add at the end

Each transformation in the processes list is applied in sequence, allowing for multiple transformations to be chained together.

## Creating Custom Processors

To create a custom processor:

1. Create a new Python file in the `processor` directory
2. Define a class that inherits from `BaseProcessor`
3. Implement the `process` method
4. Register the processor with the `@register_processor` decorator

Example:

```python
from typing import List

from ..model import TextSegment
from . import register_processor
from .base import BaseProcessor

@register_processor("my_processor")
class MyProcessor(BaseProcessor):
    def __init__(self, option1: str = "default", option2: bool = False):
        self.option1 = option1
        self.option2 = option2

    def process(self, segments: List[TextSegment]) -> List[TextSegment]:
        # Process the segments
        processed_segments = []
        for segment in segments:
            # Create a new segment with the processed text
            processed_segment = TextSegment(
                text=f"{self.option1}: {segment.text}",
                start_time=segment.start_time,
                end_time=segment.end_time
            )
            processed_segments.append(processed_segment)

        return processed_segments
```

Then create a YAML configuration file:

```yaml
type: my_processor
option1: custom value
option2: true
```