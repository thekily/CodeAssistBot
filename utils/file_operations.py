import os
from pathlib import Path

def get_file_tree(repo_path):
    """
    Generate a file tree structure for the given repository path.
    """
    try:
        repo_path = Path(repo_path).resolve()
        if not repo_path.exists() or not repo_path.is_dir():
            raise ValueError(f"Invalid repository path: {repo_path}")

        tree = {}
        for root, dirs, files in os.walk(repo_path):
            current = tree
            for part in Path(root).relative_to(repo_path).parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current['__files__'] = files

        return tree
    except Exception as e:
        raise Exception(f"Error getting file tree: {str(e)}")

def read_file_content(file_path):
    """
    Read and return the content of a file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {str(e)}")

def write_file_content(file_path, content):
    """
    Write content to a file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        raise Exception(f"Error writing to file {file_path}: {str(e)}")
