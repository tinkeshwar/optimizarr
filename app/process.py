from logger import logger
from utils import convert_to_hevc, load_json, save_json
import shutil

OPTIMIZED_PATH = "/optimized"

def replace_video_file(original_file: str, optimized_file: str) -> bool:
    """
    Replace the original video file with the optimized one and update metadata
    
    Args:
        original_file (str): Path to the original video file
        optimized_file (str): Path to the optimized video file
        
    Returns:
        bool: True if replacement was successful, False otherwise
    """
    try:
        metadata = load_json()
        shutil.move(optimized_file, original_file)
        for item in metadata:
            if item["file_path"] == original_file:
                item.update({
                    "file_path": original_file,
                    "optimized": {
                        "file_path": optimized_file,
                        "status": "replaced"
                    }
                })
                break
        save_json(metadata)
        logger.info(f"Successfully replaced {original_file} with optimized version")
        return True
    except Exception as e:
        logger.error(f"Error replacing file {original_file}: {e}")
        return False

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
                        "status": "pending_replacement"
                    }
                })
                save_json(metadata)
                try:
                    replace_video_file(item["file_path"], optimized_file_path)
                    logger.info(f"Added {item['file_path']} to replacement")
                except Exception as e:
                    logger.error(f"Failed to replace video file: {item['file_path']}. Error: {e}")
            else:
                logger.error(f"Failed to optimize video: {item['file_path']}")

    save_json(metadata)
    logger.info("Video optimization process completed")
