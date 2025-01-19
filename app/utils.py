import os
import ffmpeg
from logger import logger
from typing import Dict, List, Optional
import json


JSON_FILE = "app/videos.json"

def get_video_files(base_path: str) -> List[str]:
    """
    Recursively find all video files in the given directory
    """
    logger.info(f"Scanning for video files in {base_path}")
    video_extensions = {".mp4", ".mkv", ".avi", ".mov"}
    video_files = []
    
    try:
        for root, _, files in os.walk(base_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    video_files.append(os.path.join(root, file))
        
        logger.info(f"Found {len(video_files)} video files")
        return video_files
    
    except OSError as e:
        logger.error(f"Error scanning directory: {e}")
        return []

def convert_to_hevc(input_file: str, output_dir: str, crf: int = 28, preset: str = "slow") -> Optional[str]:
    """
    Convert a video file to HEVC/H.265 format using FFmpeg-Python.

    Args:
        input_file (str): Path to the input video file.
        output_dir (str): Directory where the converted file will be saved.
        crf (int): Constant Rate Factor for quality (lower is better quality). Default is 28.
        preset (str): Encoding preset for compression speed/quality tradeoff. Default is 'slow'.

    Returns:
        Optional[str]: Path to the converted video file, or None if conversion fails.
    """
    if not os.path.exists(input_file):
        logger.error(f"Input file '{input_file}' does not exist")
        return None

    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Construct the output file path
        base_name, _ = os.path.splitext(os.path.basename(input_file))
        output_file = os.path.join(output_dir, f"{base_name}.mp4")

        logger.info(f"Converting '{input_file}' to HEVC format...")

        # Perform the conversion using FFmpeg-Python
        ffmpeg.input(input_file).output(
            output_file,
            vcodec="libx265",    # Use HEVC codec
            preset=preset,       # Compression speed/quality tradeoff
            crf=crf,             # Constant Rate Factor
            acodec="aac",        # Audio codec
            audio_bitrate="128k" # Audio bitrate
        ).run(overwrite_output=True)

        logger.info(f"Successfully converted to '{output_file}'")
        return output_file

    except ffmpeg.Error as e:
        logger.error(f"FFmpeg conversion failed: {e.stderr.decode()}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return None

def load_json() -> List[Dict]:
    """Load JSON data from file or return empty list"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            logger.info(f"Loading JSON data from {JSON_FILE}")
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")
                return []
    logger.warning(f"JSON file {JSON_FILE} not found, returning empty list")
    return []

def save_json(data: List[Dict]) -> None:
    """Save JSON data to file"""
    os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
    with open(JSON_FILE, "w") as f:
        logger.info(f"Saving JSON data to {JSON_FILE}")
        json.dump(data, f, indent=4)