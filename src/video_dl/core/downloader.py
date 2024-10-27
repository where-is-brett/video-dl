# src/video_dl/core/downloader.py
import re
import time
from typing import Dict
from pathlib import Path
import yt_dlp
from ..models.config import DownloadConfig
from ..models.video import DownloadResult, VideoMetadata
from ..exceptions.errors import DownloadError, ValidationError
from ..utils.filesystem import calculate_checksum

class VideoDownloader:
    def __init__(self, config: DownloadConfig):
        self.config = config
        self._validate_url(self.config.url)
        self.ydl_opts = self._prepare_ydl_opts()
    
    SUPPORTED_PLATFORMS = [
            'youtube.com',
            'youtu.be',
            'vimeo.com',
            'dailymotion.com'
        ]

    def _validate_url(self, url: str) -> None:
        """Validate URL format."""
        if not url or not isinstance(url, str):
            raise ValidationError("URL cannot be empty")
        
        # Basic URL validation for video platforms
        valid_domains = r'(?:' + '|'.join(re.escape(p) for p in self.SUPPORTED_PLATFORMS) + ')'
        url_pattern = fr'https?://(?:www\.)?{valid_domains}/\S+'
        
        if not re.match(url_pattern, url):
            raise ValidationError(
                f"Invalid URL format or unsupported platform: {url}\n"
                f"Supported platforms: {', '.join(self.SUPPORTED_PLATFORMS)}"
            )
    
    def _parse_size_string(self, size_str: str) -> int:
        """Parse size string with units (e.g., '1M', '500K') to bytes."""
        units = {
            'K': 1024,
            'M': 1024 * 1024,
            'G': 1024 * 1024 * 1024
        }
        
        # Remove whitespace and convert to uppercase for consistency
        size_str = size_str.strip().upper()
        
        # Parse value and unit
        match = re.match(r'^([\d.]+)([KMG])?$', size_str)
        if not match:
            raise ValidationError(f"Invalid size format: {size_str}")
        
        value, unit = match.groups()
        try:
            value = float(value)
        except ValueError:
            raise ValidationError(f"Invalid numeric value: {value}")
            
        # Convert to bytes
        return int(value * (units.get(unit, 1) if unit else 1))

    def _prepare_ydl_opts(self) -> Dict:
        """Prepare yt-dlp options from configuration."""
        # Handle quality setting
        if self.config.quality == 'best':
            format_spec = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else:
            # Extract numeric height from quality string (e.g., '1080p' -> '1080')
            height = self.config.quality.rstrip('p')
            format_spec = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best'

        opts = {
            'format': self.config.format_id or format_spec,
            'outtmpl': str(self.config.output_path / '%(title)s.%(ext)s'),
            'retries': getattr(self.config, 'retries', 3),
            'quiet': False,
            'progress_hooks': [self._progress_hook],
            'merge_output_format': 'mp4',
        }
        
        if self.config.proxy:
            opts['proxy'] = self.config.proxy
        
        if self.config.limit_speed:
            try:
                opts['ratelimit'] = self._parse_size_string(self.config.limit_speed)
            except ValidationError as e:
                raise ValidationError(f"Invalid rate limit: {str(e)}")
        
        return opts
    
    def _parse_quality(self, quality: str) -> str:
        """Parse quality string to determine video resolution limit."""
        if isinstance(quality, str):
            match = re.match(r'(\d+)', quality)
            if match:
                return match.group(1)  # Extracts the numeric part, like 720 from "720p"
        return 'best'  # Default to "best" if no resolution is specified

    def download(self, url: str) -> DownloadResult:
        """Download video from URL."""
        self._validate_url(url)
        start_time = time.time()
        last_error = None
        
        for attempt in range(self.config.retries):
            try:
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    print(f"Starting download: {url}")
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    filepath = Path(filename)
                    
                    if not filepath.exists():
                        raise DownloadError(f"Download completed but file not found: {filepath}")
                    
                    metadata = self._extract_metadata(info)
                    filesize = filepath.stat().st_size
                    checksum = calculate_checksum(filepath)
                    
                    return DownloadResult(
                        success=True,
                        filepath=filepath,
                        error=None,
                        metadata=metadata,
                        download_time=time.time() - start_time,
                        filesize=filesize,
                        checksum=checksum
                    )
                    
            except Exception as e:
                last_error = str(e)
                if attempt < self.config.retries - 1:
                    print(f"Download failed: {last_error}. Retrying... ({attempt + 1}/{self.config.retries})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Download failed: {last_error}")
                    
        return DownloadResult(
            success=False,
            filepath=None,
            error=last_error,
            metadata=None,
            download_time=time.time() - start_time,
            filesize=0,
            checksum=None
        )

    def _extract_metadata(self, info: Dict) -> VideoMetadata:
        """Extract metadata from downloaded video info."""
        return VideoMetadata(
            title=info.get('title', ''),
            duration=info.get('duration'),
            upload_date=info.get('upload_date'),
            uploader=info.get('uploader'),
            view_count=info.get('view_count'),
            like_count=info.get('like_count'),
            description=info.get('description'),
            tags=info.get('tags', []),
            categories=info.get('categories', []),
            thumbnail_url=info.get('thumbnail'),
            webpage_url=info.get('webpage_url', ''),
            extractor=info.get('extractor', ''),
            format_id=info.get('format_id', ''),
            width=info.get('width'),
            height=info.get('height'),
            fps=info.get('fps'),
            vcodec=info.get('vcodec'),
            acodec=info.get('acodec'),
            filesize=info.get('filesize')
        )

    def _progress_hook(self, d: Dict) -> None:
        """Handle download progress updates."""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                print(f"\rDownload progress: {percentage:.1f}%", end='')
            else:
                print(f"\rDownloaded: {d['downloaded_bytes'] / (1024*1024):.1f}MB", end='')
        elif d['status'] == 'finished':
            print("\nDownload completed, processing file...")