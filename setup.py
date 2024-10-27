# setup.py
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Core dependencies
INSTALL_REQUIRES = [
    "yt-dlp>=2023.11.16",
    "ffmpeg-python>=0.2.0",
    "pysrt>=1.1.2",
    "webvtt-py>=0.4.6",
    "chardet>=4.0.0",
    "schedule>=1.1.0",
    "tqdm>=4.65.0",
    "requests>=2.28.0",
    "pyyaml>=6.0.1",
]

# Development dependencies
DEV_REQUIRES = [
    "pytest>=7.3.1",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "responses>=0.23.1",
]

# Linting dependencies
LINT_REQUIRES = [
    "black>=23.1.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

# Documentation dependencies
DOCS_REQUIRES = [
    "mkdocs>=1.6.1",
    "mkdocs-material>=9.5.42"
]

setup(
    name="video-dl",
    version="0.1.0",
    description="Advanced video and subtitle downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brett Yang",
    author_email="hello@brettyang.au",
    url="https://github.com/where-is-brett/video-dl",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
        "lint": LINT_REQUIRES,
        "docs": DOCS_REQUIRES,
        # Combine all development dependencies
        "all": DEV_REQUIRES + LINT_REQUIRES + DOCS_REQUIRES,
    },
    package_data={  # Package non-code data files
        "": ["LICENSE"],
    },
    entry_points={
        "console_scripts": [
            "video-dl=video_dl.cli.download:main",
            "subtitle-dl=video_dl.cli.subtitle:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    project_urls={
        "Bug Reports": "https://github.com/where-is-brett/video-dl/issues",
        "Source": "https://github.com/where-is-brett/video-dl",
        "Documentation": "https://video-dl.readthedocs.io/",
    },
)