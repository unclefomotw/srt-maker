#!/usr/bin/env python3
"""
SRT Maker CLI

A command-line tool for creating and manipulating SRT subtitle files.
"""

import argparse
import logging
import sys
from typing import List, Optional

import srt

from .generator import generate_srt

logging.basicConfig(level=logging.INFO)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SRT Maker - Create and manipulate SRT subtitle files"
    )

    parser.add_argument(
        "input_file",
        help="Path to the input audio or video file, or an intermediate output from an STT service"
    )
    parser.add_argument(
        "-s", "--stt",
        help="Specify which STT service to generate (default: 'elevenlabs')",
        default="elevenlabs"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output SRT file (default: input_file.srt)",
        default=None
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)

    try:
        logging.info(f"Generating SRT for: {parsed_args.input_file}")
        logging.info(f"Using STT service: {parsed_args.stt}")

        # Pass the STT service to the generator
        srt_list: List[srt.Subtitle] = generate_srt(
            parsed_args.input_file,
            stt_service=parsed_args.stt
        )

        srt_str = srt.compose(srt_list)
        if parsed_args.output:
            with open(parsed_args.output, "w") as f:
                f.write(srt_str)
                f.write("\n")
            logging.info(f"SRT file written to: {parsed_args.output}")
        else:
            print(srt_str)

        return 0
    except Exception as e:
        raise


if __name__ == "__main__":
    sys.exit(main())