import os
import ffmpeg
from utils import get_video_files, load_json, save_json
from typing import List, Dict
from logger import logger
from functools import lru_cache

@lru_cache(maxsize=128)
def get_raw_files() -> List[str]:
    metadata = load_json()
    return [item["file_path"] for item in metadata if item["status"] == "raw"]

def get_video_metadata(file_path: str) -> Dict:
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None
        )
        return {
            "file_path": file_path,
            "size": os.path.getsize(file_path),
            "filetype": os.path.splitext(file_path)[1][1:],
            "codec": video_stream["codec_name"] if video_stream else "unknown",
            "status": "raw"
        }
    except (ffmpeg.Error, OSError) as e:
        logger.error(f"Error getting metadata for file {file_path}: {e}")
        return None

def process_videos(storage_path: str) -> List[str]:
    metadata = load_json()
    existing_files = {item["file_path"] for item in metadata}
    new_files = []
    
    for file_path in filter(lambda x: x not in existing_files, get_video_files(storage_path)):
        logger.info(f"Found new file: {file_path}")
        try:
            if video_metadata := get_video_metadata(file_path):
                metadata.append(video_metadata)
                new_files.append(file_path)
            else:
                logger.warning(f"Skipping file {file_path} due to metadata retrieval failure")
        except ffmpeg.Error as e:
            logger.error(f"Error probing file {file_path}: {e}")
            
    save_json(metadata)      
    return get_raw_files()
