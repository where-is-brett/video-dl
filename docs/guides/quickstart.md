# Quick Start Guide

Get started with Video-DL's basic features and commands.

## Basic Usage

### Download a Video

```bash
# Basic download (best quality)
video-dl download "https://youtube.com/watch?v=example"

# Specify quality
video-dl download "https://youtube.com/watch?v=example" -q 1080p

# Specify output directory
video-dl download "https://youtube.com/watch?v=example" -o ~/Downloads/videos
```

### Download Subtitles

```bash
# Download English subtitles
subtitle-dl download "https://youtube.com/watch?v=example"

# Download multiple languages
subtitle-dl download "https://youtube.com/watch?v=example" -l "en,es,fr"

# Convert to SRT format
subtitle-dl download "https://youtube.com/watch?v=example" --convert-srt
```

### Process Videos

```bash
# Resize video
video-dl download "https://youtube.com/watch?v=example" \
  --process \
  --resize 1920x1080

# Convert HDR to SDR
video-dl download "https://youtube.com/watch?v=example" \
  --process \
  --hdr-to-sdr

# Extract audio
video-dl download "https://youtube.com/watch?v=example" \
  --extract-audio \
  --audio-format mp3
```

## Command Structure

Video-DL commands follow this pattern:
```bash
video-dl <command> [options] URL
subtitle-dl <command> [options] URL
```

Common options:
- `-o, --output`: Output directory
- `-q, --quality`: Video quality
- `-f, --format`: Format selection
- `--process`: Enable video processing
- `--verbose`: Show detailed output

## Examples

### Download Playlist
```bash
video-dl download "https://youtube.com/playlist?list=example" \
  -o playlist \
  -q 720p
```

### Download with Custom Format
```bash
video-dl download "https://youtube.com/watch?v=example" \
  -f "bestvideo[height<=1080]+bestaudio/best"
```

### Process and Convert
```bash
video-dl download "https://youtube.com/watch?v=example" \
  --process \
  --resize 1280x720 \
  --fps 30 \
  --video-codec libx264
```

## Next Steps

- Check out the [Configuration Guide](configuration.md) for customizing Video-DL
- Learn about [Advanced Usage](advanced-usage.md) features
- Read the [API Reference](../api/downloader.md) for programmatic usage