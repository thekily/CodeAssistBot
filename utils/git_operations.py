import os
import git

def initialize_repo(repo_path):
    """
    Initialize a new Git repository or reinitialize an existing one.
    """
    try:
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
        repo = git.Repo.init(repo_path)
        return "Git repository initialized successfully."
    except Exception as e:
        return f"Error initializing Git repository: {str(e)}"

def get_repo_status(repo_path):
    """
    Get the current status of the Git repository.
    """
    try:
        repo = git.Repo(repo_path)
        return repo.git.status()
    except Exception as e:
        return f"Error getting repository status: {str(e)}"

def stage_changes(repo_path, file_path=None):
    """
    Stage changes in the Git repository. If file_path is provided, stage only that file.
    """
    try:
        repo = git.Repo(repo_path)
        if file_path:
            repo.git.add(file_path)
        else:
            repo.git.add(A=True)
        return "Changes staged successfully."
    except Exception as e:
        return f"Error staging changes: {str(e)}"

def commit_changes(repo_path, message):
    """
    Commit staged changes with the provided commit message.
    """
    try:
        repo = git.Repo(repo_path)
        repo.git.commit(m=message)
        return "Changes committed successfully."
    except Exception as e:
        return f"Error committing changes: {str(e)}"

def get_commit_history(repo_path):
    """
    Get the commit history of the repository.
    """
    try:
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits())
        history = [{"hash": commit.hexsha, "message": commit.message, "author": str(commit.author), "date": commit.committed_datetime} for commit in commits]
        return history
    except Exception as e:
        return f"Error getting commit history: {str(e)}"
