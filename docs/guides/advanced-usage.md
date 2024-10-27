# Advanced Usage Guide

This guide covers advanced features and usage patterns of Video-DL.

## Video Processing

### Advanced Format Selection

Use complex format selectors to get exactly what you want:

```bash
# Select best MP4 format under 1080p
video-dl download "URL" -f 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best'

# Prefer VP9 codec
video-dl download "URL" -f 'bestvideo[vcodec^=vp9]+bestaudio/best'

# Download specific format
video-dl download "URL" -f 137+140
```

### Video Processing Pipeline

Chain multiple processing operations:

```bash
video-dl download "URL" \
  --process \
  --resize 1920x1080 \
  --crop 1920:800:0:140 \
  --fps 60 \
  --hdr-to-sdr \
  --video-codec libx264 \
  --video-bitrate 5M \
  --audio-codec aac \
  --audio-bitrate 192k
```

### HDR Processing

Advanced HDR to SDR conversion options:

```bash
# Custom HDR to SDR settings
video-dl download "URL" \
  --process \
  --hdr-to-sdr \
  --tonemap-mode hable \
  --peak-target-nits 200 \
  --dynamic-range 15

# With color space conversion
video-dl download "URL" \
  --process \
  --hdr-to-sdr \
  --color-space bt709 \
  --color-primaries bt709 \
  --color-trc bt709
```

## Batch Processing

### Batch Download from File

```bash
# Create URL list
cat > urls.txt << EOL
https://youtube.com/watch?v=example1
https://youtube.com/watch?v=example2
https://vimeo.com/example3
EOL

# Download all videos
video-dl batch urls.txt \
  --output batch_downloads \
  --quality 1080p \
  --max-concurrent 3
```

### Playlist Processing

```bash
# Download playlist with specific items
video-dl download "PLAYLIST_URL" \
  --playlist-items 1-3,7,10-12 \
  --playlist-reverse \
  --playlist-random

# Process entire playlist
video-dl download "PLAYLIST_URL" \
  --process \
  --resize 1280x720 \
  --output "playlist/%(playlist_title)s/%(title)s.%(ext)s"
```

## Advanced Subtitle Management

### Complex Subtitle Operations

```bash
# Download, convert, and merge subtitles
subtitle-dl download "URL" \
  --languages en,es,fr \
  --convert-srt \
  --fix-encoding \
  --remove-formatting \
  --merge \
  --output-format "%(title)s.%(lang)s.%(ext)s"

# Download with timing adjustment
subtitle-dl download "URL" \
  --languages en \
  --time-offset -2.5 \
  --split-at "00:05:00,00:10:00" \
  --remove-ads
```

### Subtitle Extraction from Video

```bash
# Extract embedded subtitles
video-dl extract-subs "video.mkv" \
  --languages all \
  --output "subs/%(lang)s.%(ext)s"

# Extract and convert
video-dl extract-subs "video.mkv" \
  --languages en,es \
  --convert-to srt \
  --fix-encoding
```

## Custom Output Templates

### Advanced Naming Patterns

```bash
# Complex output structure
video-dl download "URL" \
  --output "%(uploader)s/%(playlist_title)s/%(upload_date)s_%(title)s_%(resolution)s.%(ext)s"

# With custom formatting
video-dl download "URL" \
  --output "%(title).50s_%(height)dp_%(fps)dfps.%(ext)s" \
  --output-na-placeholder "UNKNOWN"
```

### Available Template Fields

- Basic: `title`, `ext`, `upload_date`, `uploader`, `channel`
- Technical: `height`, `width`, `fps`, `tbr`, `vcodec`, `acodec`
- Identifiers: `id`, `playlist_id`, `playlist_index`
- Time: `duration`, `upload_date`, `timestamp`
- Other: `like_count`, `view_count`, `comment_count`

## Rate Limiting and Proxies

### Advanced Download Control

```bash
# Rate limiting with burst
video-dl download "URL" \
  --limit-rate 1M \
  --limit-rate-burst 5M \
  --sleep-interval 2 \
  --max-sleep-interval 10

# With proxy rotation
video-dl download "URL" \
  --proxy-file proxies.txt \
  --proxy-rotation-interval 30
```

### Proxy Configuration

```bash
# Multiple proxy types
video-dl download "URL" \
  --http-proxy http://proxy1:8080 \
  --https-proxy https://proxy2:8443 \
  --socks-proxy socks5://proxy3:1080
```

## Authentication and Cookies

### Complex Authentication

```bash
# Using cookies and authentication
video-dl download "URL" \
  --cookies cookies.txt \
  --username "$USERNAME" \
  --password "$PASSWORD" \
  --two-factor "$2FA_CODE" \
  --netrc
```

### Cookie Management

```bash
# Export cookies from browser
video-dl cookies export \
  --browser chrome \
  --profile default \
  --output cookies.txt

# Use cookies with specific domains
video-dl download "URL" \
  --cookies-from-browser firefox \
  --cookies-domain youtube.com,google.com
```

## Advanced Error Handling

### Retry Mechanisms

```bash
# Configure retries
video-dl download "URL" \
  --retries 5 \
  --retry-sleep 10 \
  --retry-sleep-multiplier 2 \
  --retry-on-http 403,429,500-599
```

### Fragment Downloads

```bash
# Handle fragmented downloads
video-dl download "URL" \
  --fragment-retries 10 \
  --skip-unavailable-fragments \
  --abort-on-unavailable-fragment \
  --keep-fragments
```

## Monitoring and Logging

### Advanced Logging

```bash
# Detailed logging
video-dl download "URL" \
  --log-level debug \
  --log-file download.log \
  --progress-template "%(progress)s%(speed)s%(eta)s"

# With statistics
video-dl download "URL" \
  --print-traffic \
  --print-stats \
  --stats-interval 5
```

## Next Steps

- Explore the [API Reference](../api/downloader.md) for programmatic usage
- Learn about [Configuration](configuration.md) options
- Contribute to development - see [Contributing Guide](../contributing/development.md)