# Optimizarr

Optimizarr is a video optimization tool that automatically processes and converts video files to the HEVC (H.265) format for improved compression and quality.

## Features

- Automatic scanning of specified directories for new video files
- Conversion of video files to HEVC format using FFmpeg
- Metadata tracking of processed videos
- Docker support for easy deployment

## Prerequisites

- Docker and Docker Compose
- FFmpeg (installed automatically in the Docker container)
- Python 3.9 or later

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/optimizarr.git
   cd optimizarr
   ```

2. Create a `.env` file in the project root and set the `SCAN_INTERVAL` (in seconds):
   ```
   SCAN_INTERVAL=3600
   ```

## Usage

To start Optimizarr using Docker Compose:

```
docker-compose up -d
```

This will build the Docker image and start the container in detached mode.

## Configuration

You can configure the following settings:

- `SCAN_INTERVAL`: The interval (in seconds) between scans for new video files. Set this in the `.env` file or the `docker-compose.yml` file.
- Input and output directories: Modify the volume mappings in `docker-compose.yml` to set your desired input and output directories.

## Docker Deployment

The project includes a `Dockerfile` and `docker-compose.yml` for easy deployment. The Docker setup:

- Uses Python 3.9 as the base image
- Installs FFmpeg
- Sets up the working directory as `/app`
- Installs Python dependencies from `requirements.txt`
- Mounts three volumes:
  - `./app:/app`: Application code
  - `<your file path>:/storage/path1`: Input directory for raw videos
  - `<your file path>:/storage/path2`: Input directory for raw videos
  - `/Users/tinkeshwar/Downloads/Optimized:/optimized`: Output directory for optimized videos

To customize the input and output directories, modify the volume mappings in `docker-compose.yml`.