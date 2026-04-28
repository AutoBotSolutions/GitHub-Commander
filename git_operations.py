"""
Git Operations - Handles local git operations
"""

import os
from pathlib import Path
from git import Repo, GitCommandError, Actor
from typing import Optional, List
from config import Config

class GitOperations:
    """Handles local git operations"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def clone_repository(self, url: str, destination: Path, 
                       branch: str = "main") -> bool:
        """Clone a repository"""
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            Repo.clone_from(url, destination, branch=branch)
            return True
        except GitCommandError as e:
            print(f"Clone error: {e}")
            return False
    
    def init_repository(self, path: Path) -> Optional[Repo]:
        """Initialize a new git repository"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return Repo.init(path)
        except GitCommandError:
            return None
    
    def add_all(self, repo: Repo) -> bool:
        """Stage all changes"""
        try:
            repo.index.add([item for item in repo.untracked_files] + [item.a_path for item in repo.index.diff(None)])
            return True
        except GitCommandError:
            return False
    
    def add_file(self, repo: Repo, file_path: str) -> bool:
        """Stage a specific file"""
        try:
            repo.index.add([file_path])
            return True
        except GitCommandError:
            return False
    
    def commit(self, repo: Repo, message: str, 
              author_name: str = "", author_email: str = "") -> bool:
        """Commit staged changes"""
        try:
            author = None
            if author_name and author_email:
                author = Actor(author_name, author_email)
            
            repo.index.commit(message, author=author, committer=author)
            return True
        except GitCommandError:
            return False
    
    def push(self, repo: Repo, remote_name: str = "origin", 
            branch: str = "main", force: bool = False) -> bool:
        """Push changes to remote"""
        try:
            if force:
                repo.git.push(remote_name, branch, "--force")
            else:
                repo.git.push(remote_name, branch)
            return True
        except GitCommandError as e:
            print(f"Push error: {e}")
            return False
    
    def pull(self, repo: Repo, remote_name: str = "origin", 
            branch: str = "main") -> bool:
        """Pull changes from remote"""
        try:
            repo.git.pull(f"{remote_name}/{branch}")
            return True
        except GitCommandError as e:
            print(f"Pull error: {e}")
            return False
    
    def create_branch(self, repo: Repo, branch_name: str) -> bool:
        """Create a new branch"""
        try:
            repo.git.checkout("-b", branch_name)
            return True
        except GitCommandError:
            return False
    
    def checkout_branch(self, repo: Repo, branch_name: str) -> bool:
        """Switch to a branch"""
        try:
            repo.heads[branch_name].checkout()
            return True
        except GitCommandError:
            return False
    
    def get_current_branch(self, repo: Repo) -> str:
        """Get current branch name"""
        try:
            return repo.active_branch.name
        except GitCommandError:
            return ""
    
    def get_branches(self, repo: Repo) -> List[str]:
        """Get all local branches"""
        try:
            return [h.name for h in repo.heads]
        except GitCommandError:
            return []
    
    def get_remote_branches(self, repo: Repo) -> List[str]:
        """Get all remote branches"""
        try:
            return [ref.name.split('/')[-1] for ref in repo.references 
                   if 'remote' in ref.name]
        except GitCommandError:
            return []
    
    def add_remote(self, repo: Repo, name: str, url: str) -> bool:
        """Add a remote repository"""
        try:
            repo.create_remote(name, url)
            return True
        except GitCommandError:
            return False
    
    def get_status(self, repo: Repo) -> str:
        """Get git status"""
        try:
            return repo.git.status()
        except GitCommandError:
            return ""
    
    def get_remotes(self, repo: Repo) -> List[str]:
        """Get all remotes"""
        try:
            return [remote.name for remote in repo.remotes]
        except GitCommandError:
            return []
    
    def get_remote_url(self, repo: Repo, remote_name: str = "origin") -> Optional[str]:
        """Get remote URL"""
        try:
            remote = repo.remote(remote_name)
            return remote.url
        except GitCommandError:
            return None
    
    def stage_folder(self, repo: Repo, folder_path: str) -> bool:
        """Stage all files in a folder"""
        try:
            repo.index.add([folder_path])
            return True
        except GitCommandError:
            return False
