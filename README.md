# subtitle_tool

AI Subtitle Correction & YouTube Metadata Generator

📖 [中文版 README](README_zh.md)

Features:
- **Subtitle Correction** — Fix subtitle errors using AI
- **YouTube Title Generation** — Generate 5 catchy titles
- **YouTube Description** — Create engaging video descriptions
- **SEO Optimization** — Generate chapters, keywords, and tags

## Quick Start

### 1. First-Time Setup (once only)

```bash
venv\Scripts\python main.py --setup
```

Follow the prompts to enter:
- API Key
- API URL (press Enter for default)
- Model (press Enter for default)

### 2. Usage

Place subtitle files (SRT/VTT) in the `input/` folder, then run:

```bash
venv\Scripts\python main.py --auto
```

This shows a menu to select files and processes them automatically!

## Workflow

```
input/                output/
├── video1.srt   →   video1/
├── video2.srt   →   ├── video1_corrected.srt
└── video3.srt       ├── correction_report.json
                      └── youtube_info.txt (titles, description, chapters, keywords)
```

## Commands

| Command | Description |
|---------|-------------|
| `--setup` / `-s` | Setup mode, configure API |
| `--auto` / `-a` | Auto mode, reads from input |
| `--input` / `-i` | Process specific file |
| `--output` / `-o` | Specify output directory (default: output) |

## Output Files

Each video gets its own folder containing:

| File | Content |
|------|---------|
| `*_corrected.srt` | Corrected subtitles |
| `correction_report.json` | Correction report |
| `youtube_info.txt` | All YouTube content (titles, description, chapters, keywords) |

## Tech Terms

Edit `dict/frequently_used_terms.json` and `dict/corrections.json` to customize terminology and corrections.

## API

Supports any OpenAI-compatible API, defaults to Mini Max.

## Examples

```bash
# Setup API (first time)
venv\Scripts\python main.py --setup

# Process subtitles (auto select)
venv\Scripts\python main.py --auto

# Or specify file
venv\Scripts\python main.py --input input/video.srt --output output/
```