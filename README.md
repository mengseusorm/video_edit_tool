# 🎬 Video Terminal Tool

A beautiful command-line interface for video processing with support for resizing, splitting, and cropping videos for social media platforms.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🎨 Beautiful Terminal UI** - Rich, colorful interface with responsive design
- **📐 Video Resizing** - Resize videos to custom dimensions
- **✂️ Video Splitting** - Split videos by duration with precise timing
- **📱 Social Media Cropping** - Pre-configured crop settings for popular platforms
- **📊 Video Information** - Display video details (resolution, duration, file size)
- **📋 File Management** - List and select video files from directory

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+** installed on your system
2. **FFmpeg** installed and accessible from command line
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd video-terminal-tool
```

2. Install required Python packages:
```bash
pip install rich ffmpeg-python keyboard
```

3. Run the tool:
```bash
python video_tool.py
```

## 📱 Social Media Crop Presets

| Platform | Aspect Ratio | Dimensions | Use Case |
|----------|-------------|------------|----------|
| TikTok/Instagram Stories | 9:16 | 1080×1920 | Vertical videos |
| Instagram Post | 1:1 | 1080×1080 | Square posts |
| Facebook Post | 1.91:1 | 1200×630 | Landscape posts |
| YouTube Thumbnail | 16:9 | 1080×608 | Video thumbnails |
| Instagram Feed | 4:5 | 1080×1350 | Portrait posts |
| Custom | User-defined | Custom | Any dimensions |

## 🎯 Usage

### Main Menu Options

1. **📐 Resize Video** - Change video dimensions
2. **✂️ Split Video** - Split video into segments by duration
3. **📱 Crop Video** - Crop video for social media platforms
4. **📋 List Videos** - Show all video files in current directory
5. **🚪 Exit** - Quit the application

### Example Workflows

#### Resize Video for Web
1. Select option `1` (Resize Video)
2. Choose your video file
3. Enter new width and height
4. Video is resized and saved with `_resized` suffix

#### Create TikTok Video
1. Select option `3` (Crop Video)
2. Choose your video file
3. Select option `1` (TikTok/Instagram Stories 9:16)
4. Video is cropped and saved with `_cropped_tiktok_stories_9x16` suffix

#### Split Long Video
1. Select option `2` (Split Video)
2. Choose your video file
3. Enter segment duration in seconds
4. Video is split into numbered segments in `segments/` folder

## 🛠️ Technical Details

### Dependencies

```python
rich>=13.0.0          # Terminal UI components
ffmpeg-python>=0.2.0  # FFmpeg Python bindings
keyboard>=0.13.0      # Arrow key navigation (optional)
```

### Video Processing

- **Codec**: H.264 (libx264) for video, AAC for audio
- **Quality**: Maintains original quality during processing
- **Formats**: Supports MP4, AVI, MOV, MKV, and other FFmpeg-supported formats

### Smart Cropping

The tool automatically scales down crop dimensions if they exceed the input video size while maintaining aspect ratio:

```python
# Example: If input is 720×480 and crop target is 1080×1920
# The tool scales to 270×480 (maintaining 9:16 ratio)
```

## 📁 File Structure

```
video-terminal-tool/
├── video_tool.py          # Main application
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── segments/              # Split video outputs (auto-created)
└── examples/              # Example videos (optional)
```

## 🎨 Interface Preview

```
╔══════════════════════════════════════════════════════════════╗
║                        Welcome                               ║
║                                                              ║
║              🎬 VIDEO TERMINAL TOOL 🎬                      ║
║              Resize & Split Videos Like a Pro!               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

┌─ 🎬 Video Processing Menu ─────────────────────────────────────┐
│ ┌────────┬────────────────────────────────────────────────────┐ │
│ │ Option │ Description                                        │ │
│ ├────────┼────────────────────────────────────────────────────┤ │
│ │   1    │ 📐 Resize Video                                   │ │
│ │   2    │ ✂️ Split Video by Duration                        │ │
│ │   3    │ 📱 Crop Video for Social Media                    │ │
│ │   4    │ 📋 List Video Files                               │ │
│ │   5    │ 🚪 Exit                                           │ │
│ └────────┴────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```
   Error: ffmpeg not found in PATH
   ```
   **Solution**: Install FFmpeg and add it to your system PATH

2. **Permission denied**
   ```
   Error: Permission denied when saving file
   ```
   **Solution**: Run with administrator privileges or check file permissions

3. **Invalid video format**
   ```
   Error: Could not open input file
   ```
   **Solution**: Ensure video format is supported by FFmpeg

4. **Large file processing**
   - For large files (>1GB), processing may take several minutes
   - Progress indicators show current operation status

### Performance Tips

- Use lower resolution settings for faster processing
- Split large videos into smaller segments for easier handling
- Keep original files as backups before processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - For beautiful terminal formatting
- [FFmpeg](https://ffmpeg.org/) - For powerful video processing capabilities
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) - For Python FFmpeg bindings

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#🔧-troubleshooting) section
2. Search existing [Issues](../../issues)
3. Create a new [Issue](../../issues/new) with detailed information

---

**Made with ❤️ for the video editing community**# video_edit_tool
# video_edit_tool
# video_edit_tool
