# Video-DL: Advanced Video and Subtitle Downloader

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/video-dl/badge/?version=latest)](https://video-dl.readthedocs.io/en/latest/?badge=latest)

Video-DL is a powerful, feature-rich video and subtitle downloader with advanced processing capabilities.

## Features

- Download videos from multiple platforms (YouTube, Vimeo, etc.)
- Process videos (resize, crop, HDR to SDR conversion)
- Download and process subtitles
- Batch processing support
- Configurable settings

## Quick Start

### Installation

```bash
# Install ffmpeg first
# On macOS:
brew install ffmpeg

# On Ubuntu/Debian:
sudo apt install ffmpeg

# Install video-dl
pip install video-dl
```

### Basic Usage

```bash
# Download video
video-dl download "https://youtube.com/watch?v=example"

# Download with processing
video-dl download "https://youtube.com/watch?v=example" --process --resize 1080p

# Download subtitles
subtitle-dl download "https://youtube.com/watch?v=example" -l en,es
```

## Documentation

Full documentation is available at [video-dl.readthedocs.io](https://video-dl.readthedocs.io/), including:

- [Installation Guide](https://video-dl.readthedocs.io/en/latest/guides/installation/)
- [Quick Start Guide](https://video-dl.readthedocs.io/en/latest/guides/quickstart/)
- [Advanced Usage](https://video-dl.readthedocs.io/en/latest/guides/advanced-usage/)
- [API Reference](https://video-dl.readthedocs.io/en/latest/api/)
- [Contributing Guide](https://video-dl.readthedocs.io/en/latest/contributing/)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the core downloading functionality
- [FFmpeg](https://ffmpeg.org/) for video processing capabilities