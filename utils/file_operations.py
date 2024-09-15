import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_file_tree(upload_folder):
    """
    Generate a file tree structure for the given upload folder.
    """
    try:
        upload_path = Path(upload_folder).resolve()
        if not upload_path.exists():
            raise FileNotFoundError(f"Upload folder does not exist: {upload_path}")
        if not upload_path.is_dir():
            raise NotADirectoryError(f"Upload path is not a directory: {upload_path}")

        tree = {}
        for root, dirs, files in os.walk(upload_path):
            current = tree
            for part in Path(root).relative_to(upload_path).parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current['__files__'] = files

        logger.info(f"Successfully generated file tree for {upload_path}")
        return tree
    except FileNotFoundError as e:
        logger.error(f"Upload folder not found: {e}")
        raise
    except NotADirectoryError as e:
        logger.error(f"Upload path is not a directory: {e}")
        raise
    except PermissionError as e:
        logger.error(f"Permission denied when accessing upload folder: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_file_tree: {e}")
        raise

def read_file_content(file_path):
    """
    Read and return the content of a file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise

def write_file_content(file_path, content):
    """
    Write content to a file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        logger.info(f"Successfully wrote content to {file_path}")
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {e}")
        raise
