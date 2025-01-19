import os
import json
from logger import logger
from utils import convert_to_hevc
from typing import List, Dict

JSON_FILE = "videos.json"
OPTIMIZED_PATH = "/optimized"

def load_json() -> List[Dict]:
    """Load JSON data from file or return empty list"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            logger.info(f"Loading JSON data from {JSON_FILE}")
            return json.load(f)
    logger.warning(f"JSON file {JSON_FILE} not found, returning empty list")
    return []

def save_json(data: List[Dict]) -> None:
    """Save JSON data to file"""
    with open(JSON_FILE, "w") as f:
        logger.info(f"Saving JSON data to {JSON_FILE}")
        json.dump(data, f, indent=4)

def optimise_videos(item_path: str) -> None:
    """Process and optimize video files to HEVC format"""
    logger.info(f"Starting video optimization for {item_path}")
    metadata = load_json()

    for item in metadata:
        if item_path == item["file_path"] and item["status"] == "raw" and item["codec"] != "hevc":
            logger.info(f"Processing video file: {item['file_path']}")
            if optimized_file_path := convert_to_hevc(item["file_path"], OPTIMIZED_PATH):
                logger.info(f"Successfully optimized video to: {optimized_file_path}")
                item.update({
                    "optimized": {
                        "file_path": optimized_file_path,
                        "size": os.path.getsize(optimized_file_path),
                        "filetype": os.path.splitext(optimized_file_path)[1][1:],
                        "codec": "hevc",
                    },
                    "status": "done"
                })
            else:
                logger.error(f"Failed to optimize video: {item['file_path']}")

    save_json(metadata)
    logger.info("Video optimization process completed")
