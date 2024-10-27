# src/video_dl/cli/download.py
import click
from pathlib import Path
from ..models.config import DownloadConfig, ProcessingConfig
from ..core.downloader import VideoDownloader
from ..logging.logger import get_logger
from ..utils.validation import validate_url

logger = get_logger(__name__)

@click.group()
def cli():
    """Video Downloader CLI"""
    pass

@cli.command()
@click.argument('url')
@click.option('-o', '--output', type=click.Path(), default='downloads',
              help='Output directory for downloaded files')
@click.option('-q', '--quality', default='best',
              help='Video quality (e.g., 720p, 1080p, best)')
@click.option('-f', '--format', 'format_id',
              help='Specific format ID to download')
@click.option('--proxy', help='Proxy URL')
@click.option('--limit-speed', help='Download speed limit (e.g., 1M, 500K)')
@click.option('--username', help='Account username')
@click.option('--password', help='Account password')
@click.option('--cookies_file', type=click.Path(exists=True),
              help='Path to cookies file')
@click.option('--process/--no-process', default=False,
              help='Enable video processing')
@click.option('--crop', help='Crop video (width:height:x:y)')
@click.option('--resize', help='Resize video (widthxheight)')
@click.option('--rotate', type=int, help='Rotate video (degrees)')
@click.option('--fps', type=int, help='Target FPS')
@click.option('--remove-audio/--keep-audio', default=False,
              help='Remove audio track')
@click.option('--extract-audio/--no-extract-audio', default=False,
              help='Extract audio only')
@click.option('--audio-format', default='mp3',
              help='Audio format for extraction')
def download(url, **kwargs):
    """Download video from URL"""
    try:
        if not validate_url(url):
            raise click.BadParameter(f"Invalid URL: {url}")

        # Prepare ProcessingConfig if processing is enabled
        processing_config = None
        if kwargs.pop('process', False):
            processing_config = ProcessingConfig(
                crop=kwargs.pop('crop', None),  # Pop the crop parameter
                resize=kwargs.pop('resize', None),
                rotate=kwargs.pop('rotate', None),
                fps=kwargs.pop('fps', None),
                remove_audio=kwargs.pop('remove_audio', False),
                extract_audio=kwargs.pop('extract_audio', False),
                audio_format=kwargs.pop('audio_format', 'mp3')
            )

        # Prepare main config
        config = DownloadConfig(
            url=url,
            output_path=Path(kwargs.pop('output', 'downloads')),
            quality=kwargs.pop('quality', 'best'),
            format_id=kwargs.pop('format_id', None),
            processing=processing_config,
            proxy=kwargs.pop('proxy', None),
            limit_speed=kwargs.pop('limit_speed', None),
            username=kwargs.pop('username', None),
            password=kwargs.pop('password', None),
            cookies_file=kwargs.pop('cookies_file', None)
        )

        # Initialize and run downloader
        downloader = VideoDownloader(config)
        result = downloader.download(url)

        if result.success:
            click.echo(click.style(
                f"Download successful: {result.filepath}",
                fg='green'
            ))
            click.echo(f"Download time: {result.download_time:.1f}s")
            click.echo(f"File size: {result.filesize / 1024 / 1024:.1f}MB")
        else:
            click.echo(click.style(
                f"Download failed: {result.error}",
                fg='red'
            ))

    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'))
        raise click.Abort()

def main():
    cli()