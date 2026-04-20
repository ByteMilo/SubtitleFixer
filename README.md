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
cd ~/subtitle_project
python main.py --wizard
```

Follow the prompts to enter:
- API Key
- API URL (press Enter for default)
- Model (press Enter for default)

### 2. Usage

Place subtitle files (SRT/VTT) in the `important/` folder, then run:

```bash
python main.py --auto
```

This shows a menu to select files and processes them automatically!

## Workflow

```
important/           output/
├── video1.srt   →   video1/
├── video2.srt   →   ├── video1_corrected.srt
└── video3.srt       ├── correction_report.json
                      ├── titles.json
                      ├── description.txt
                      ├── chapters.json
                      └── keywords.json
```

## Commands

| Command | Description |
|---------|-------------|
| `--wizard` | Setup mode, configure API |
| `--auto` | Auto mode, reads from important |
| `--input xxx.srt` | Process specific file |
| `--output output/` | Specify output directory |

## Output Files

Each video gets its own folder containing:

| File | Content |
|------|---------|
| `*_corrected.srt` | Corrected subtitles |
| `correction_report.json` | Correction report |
| `titles.json` | 5 title suggestions |
| `description.txt` | Video description |
| `chapters.json` | Chapter timestamps |
| `keywords.json` | SEO keywords |

## Tech Terms

Edit `dict/tech_terms.json` to add your domain-specific terminology.

## API

Supports any OpenAI-compatible API, defaults to Mini Max.

## Examples

```bash
# Setup API (first time)
python main.py --wizard

# Process subtitles (auto select)
python main.py --auto

# Or specify file
python main.py --input important/video.srt
```
