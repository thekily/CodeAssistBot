import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def initialize_git_repo(repo_path):
    """
    Initialize a Git repository in the given path.
    """
    try:
        subprocess.run(['git', 'init'], cwd=repo_path, check=True, capture_output=True, text=True)
        logger.info(f"Git repository initialized in {repo_path}")
        return "Git repository initialized successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error initializing Git repository: {e.stderr}")
        raise Exception(f"Error initializing Git repository: {e.stderr}")

def git_add_all(repo_path):
    """
    Stage all changes in the repository.
    """
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True, text=True)
        logger.info(f"All changes staged in {repo_path}")
        return "All changes staged successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error staging changes: {e.stderr}")
        raise Exception(f"Error staging changes: {e.stderr}")

def git_commit(repo_path, message):
    """
    Commit staged changes with the given message.
    """
    try:
        subprocess.run(['git', 'commit', '-m', message], cwd=repo_path, check=True, capture_output=True, text=True)
        logger.info(f"Changes committed in {repo_path} with message: {message}")
        return f"Changes committed successfully with message: {message}"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error committing changes: {e.stderr}")
        raise Exception(f"Error committing changes: {e.stderr}")

def git_status(repo_path):
    """
    Get the current status of the Git repository.
    """
    try:
        result = subprocess.run(['git', 'status'], cwd=repo_path, check=True, capture_output=True, text=True)
        logger.info(f"Git status retrieved for {repo_path}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting Git status: {e.stderr}")
        raise Exception(f"Error getting Git status: {e.stderr}")
