"""Subtitle parser"""

import re
from dataclasses import dataclass
from typing import List

@dataclass
class Subtitle:
    index: int
    start: str  # 00:00:00,000
    end: str
    text: str

    def to_srt(self) -> str:
        return f"{self.index}\n{self.start} --> {self.end}\n{self.text}\n"

class SubtitleParser:
    """Subtitle parser"""

    @staticmethod
    def parse_srt(content: str) -> List[Subtitle]:
        """Parse SRT format"""
        subtitles = []
        blocks = re.split(r'\n\s*\n', content.strip())

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue

            try:
                index = int(lines[0])
                time_line = lines[1]
                text = '\n'.join(lines[2:])

                # Parse timestamps
                match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', time_line)
                if match:
                    start, end = match.groups()
                    subtitles.append(Subtitle(index, start, end, text))
            except:
                continue

        return subtitles

    @staticmethod
    def parse_vtt(content: str) -> List[Subtitle]:
        """Parse VTT format"""
        subtitles = []
        lines = content.strip().split('\n')

        i = 0
        index = 1
        while i < len(lines):
            line = lines[i].strip()

            if '-->' in line:
                match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', line)
                if match:
                    start = match.group(1).replace('.', ',')
                    end = match.group(2).replace('.', ',')

                    text_lines = []
                    j = i + 1
                    while j < len(lines) and lines[j].strip():
                        text_lines.append(lines[j].strip())
                        j += 1

                    subtitles.append(Subtitle(index, start, end, '\n'.join(text_lines)))
                    index += 1
                    i = j
                    continue
            i += 1

        return subtitles

    @staticmethod
    def detect_format(content: str) -> str:
        """Detect format"""
        if content.strip().startswith('WEBVTT'):
            return 'vtt'
        return 'srt'

def load_subtitle(filepath: str) -> List[Subtitle]:
    """Load subtitle"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = SubtitleParser()
    fmt = parser.detect_format(content)

    if fmt == 'vtt':
        return parser.parse_vtt(content)
    return parser.parse_srt(content)

def save_subtitle(subtitles: List[Subtitle], filepath: str, format: str = 'srt'):
    """Save subtitle"""
    with open(filepath, 'w', encoding='utf-8') as f:
        if format == 'vtt':
            f.write("WEBVTT\n\n")
        for sub in subtitles:
            f.write(sub.to_srt())
