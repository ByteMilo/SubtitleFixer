# 字幕工具

AI 字幕校对 & YouTube 元数据生成工具

功能：
- **字幕校对** — 用 AI 修正字幕错误
- **YouTube 标题生成** — 生成 5 个吸引人的标题
- **YouTube 简介** — 创建吸引人的视频描述
- **SEO 优化** — 生成章节、关键词和标签

## 快速开始

### 1. 首次设置（只设置一次）

```bash
cd ~/subtitle_project
python main.py --wizard
```

按提示输入：
- API Key
- API URL（直接回车用默认）
- Model（直接回车用默认）

### 2. 使用方法

将字幕文件（SRT/VTT）放到 `important/` 文件夹，然后运行：

```bash
python main.py --auto
```

会显示菜单让你选择文件，然后自动处理！

## 工作流程

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

## 命令

| 命令 | 说明 |
|------|------|
| `--wizard` | 向导模式，设置 API |
| `--auto` | 自动模式，从 important 读取 |
| `--input xxx.srt` | 处理指定文件 |
| `--output output/` | 指定输出目录 |

## 输出文件

每个视频一个文件夹，包含：

| 文件 | 内容 |
|------|------|
| `*_corrected.srt` | 校对后的字幕 |
| `correction_report.json` | 校对报告 |
| `titles.json` | 5 个标题建议 |
| `description.txt` | 视频简介 |
| `chapters.json` | 章节时间点 |
| `keywords.json` | SEO 关键词 |

## 科技名词

编辑 `dict/tech_terms.json` 添加你的专有名词。

## API

支持任何 OpenAI 兼容的 API，默认使用 Mini Max。

## 示例

```bash
# 设置 API（首次）
python main.py --wizard

# 处理字幕（自动选择）
python main.py --auto

# 或指定文件
python main.py --input important/video.srt
```
