#!/usr/bin/env python3

import re
import sys
from pathlib import Path

# Amount to shift subtitles by (milliseconds)
SHIFT_MS = 1350

TIMESTAMP_PATTERN = re.compile(
    r'(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})'
)

def timestamp_to_ms(timestamp):
    hours, minutes, rest = timestamp.split(':')
    seconds, milliseconds = rest.split('.')

    return (
        int(hours) * 3600000 +
        int(minutes) * 60000 +
        int(seconds) * 1000 +
        int(milliseconds)
    )

def ms_to_timestamp(ms):
    if ms < 0:
        ms = 0

    hours = ms // 3600000
    ms %= 3600000

    minutes = ms // 60000
    ms %= 60000

    seconds = ms // 1000
    milliseconds = ms % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def shift_vtt(input_file, output_file, shift_ms):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.readlines()

    output_lines = []

    for line in content:
        match = TIMESTAMP_PATTERN.search(line)

        if match:
            start_time = timestamp_to_ms(match.group(1))
            end_time = timestamp_to_ms(match.group(2))

            start_time += shift_ms
            end_time += shift_ms

            line = (
                f"{ms_to_timestamp(start_time)} --> "
                f"{ms_to_timestamp(end_time)}\n"
            )

        output_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage:")
        print("python shift_vtt.py input.vtt output.vtt")
        sys.exit(1)

    shift_vtt(
        sys.argv[1],
        sys.argv[2],
        SHIFT_MS
    )

    print(f"Shifted subtitles by {SHIFT_MS}ms")