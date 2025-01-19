import os
import json
import ffmpeg
from utils import get_video_files
from typing import List, Dict
from logger import logger

JSON_FILE = "videos.json"

def load_json() -> List[Dict]:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return []

def save_json(data: List[Dict]) -> None:
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_raw_files() -> List[str]:
    metadata = load_json()
    return [item["file_path"] for item in metadata if item["status"] == "raw"]  

def get_video_metadata(file_path: str) -> Dict:
    probe = ffmpeg.probe(file_path)
    return {
        "file_path": file_path,
        "size": os.path.getsize(file_path),
        "filetype": os.path.splitext(file_path)[1][1:],
        "codec": next(
            (stream["codec_name"] for stream in probe["streams"] if stream["codec_type"] == "video"),
            "unknown"
        ),
        "status": "raw"
    }

def process_videos(storage_path: str) -> List[str]:
    metadata = load_json()
    existing_files = {item["file_path"] for item in metadata}
    new_files = []
    for file_path in get_video_files(storage_path):
        if file_path not in existing_files:
            logger.info(f"Found new file: {file_path}")
            try:
                metadata.append(get_video_metadata(file_path))
                new_files.append(file_path)
            except ffmpeg.Error as e:
                logger.error(f"Error probing file {file_path}: {e}")
                
    save_json(metadata)      
    return get_raw_files()
