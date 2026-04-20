# SubtitleFixer

AI 字幕校对 & YouTube 元数据生成工具

📖 [English README](README.md)

功能：
- **字幕校对** — 用 AI 修正字幕错误
- **YouTube 标题生成** — 生成 5 个吸引人的标题
- **YouTube 简介** — 创建吸引人的视频描述
- **SEO 优化** — 生成章节、关键词和标签

## 快速开始

## 安装

### 1. 克隆项目
```bash
git clone https://github.com/ByteMilo/SubtitleFixer.git
cd SubtitleFixer
```

### 2. 创建虚拟环境
```bash
python -m venv venv
```

### 3. 激活虚拟环境
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 运行设置
```bash
venv\Scripts\python main.py --setup
```

按提示输入：
- API Key
- API URL（直接回车用默认）
- Model（直接回车用默认）

### 2. 使用方法

将字幕文件（SRT/VTT）放到 `input/` 文件夹，然后运行：

```bash
venv\Scripts\python main.py --auto
```

会显示菜单让你选择文件，然后自动处理！

## 工作流程

```
input/                output/
├── video1.srt   →   video1/
├── video2.srt   →   ├── video1_corrected.srt
└── video3.srt       ├── correction_report.json
                      └── youtube_info.txt (标题、简介、章节、关键词)
```

## 命令

| 命令 | 说明 |
|------|------|
| `--setup` / `-s` | 设置模式，配置 API |
| `--auto` / `-a` | 自动模式，从 input 读取 |
| `--input` / `-i` | 处理指定文件 |
| `--output` / `-o` | 指定输出目录（默认：output） |

## 输出文件

每个视频一个文件夹，包含：

| 文件 | 内容 |
|------|------|
| `*_corrected.srt` | 校对后的字幕 |
| `correction_report.json` | 校对报告 |
| `youtube_info.txt` | YouTube 全部内容（标题、简介、章节、关键词） |

## 术语配置

编辑以下两个文件来自定义术语和纠正规则：

### `dict/frequently_used_terms.json` — 常用术语
专业术语列表，AI 会自动识别并在字幕中保持一致。例如：
```json
{
  "terms": ["AI", "机器学习", "GPT", "API", "GPU"]
}
```

### `dict/corrections.json` — 常见错误纠正
常见拼写错误和格式问题，AI 会自动修复。例如：
```json
{
  "teh": "the",
  "thier": "their",
  "  ": " "
}
```

添加你自己的术语和错误模式即可生效。

## API

支持任何 OpenAI 兼容的 API，默认使用 Mini Max。

## 示例

```bash
# 设置 API（首次）
venv\Scripts\python main.py --setup

# 处理字幕（自动选择）
venv\Scripts\python main.py --auto

# 或指定文件
venv\Scripts\python main.py --input input/video.srt --output output/
```