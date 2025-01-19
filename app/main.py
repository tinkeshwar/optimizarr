import os
import time
from queue import Queue
from threading import Thread
from dotenv import load_dotenv
from collect import process_videos
from process import optimise_videos
from logger import logger

# Load environment variables
load_dotenv()

STORAGE_PATH = "/storage"
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", 60))

# Create a queue for video processing tasks
video_queue = Queue()

def process_worker() -> None:
    """Worker function to process videos from the queue"""
    logger.info("Worker started")
    while True:
        video_path = video_queue.get()
        if video_path is None:  # Sentinel value to stop the thread
            break
        try:
            logger.info(f"Processing video: {video_path}")
            optimise_videos(video_path)
        except FileNotFoundError as e:
            logger.error(f"Video file not found: {video_path}. Error: {str(e)}")
        except PermissionError as e:
            logger.error(f"Permission denied when processing video: {video_path}. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error processing video {video_path}: {str(e)}")
        finally:
            video_queue.task_done()
            logger.info(f"Finished processing video: {video_path}")

def main():
    # Start worker thread
    worker = Thread(target=process_worker, daemon=True)
    worker.start()

    try:
        while True:
            logger.info(f"Scanning directory: {STORAGE_PATH}")
            # Collect videos and add them to queue
            videos = process_videos(STORAGE_PATH)
            if videos:
                for video in videos:
                    logger.info(f"Adding video to queue: {video}")
                    video_queue.put(video)
            
            logger.info(f"Sleeping for {SCAN_INTERVAL} seconds...")
            time.sleep(SCAN_INTERVAL)
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Clean shutdown
        video_queue.put(None)
        logger.info("Shutting down gracefully...")
