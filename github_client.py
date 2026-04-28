"""
GitHub API Client - Handles all GitHub operations
"""

from github import Github, GithubException
from github.Repository import Repository
from pathlib import Path
import os
from typing import Optional, List, Dict, Any
from config import Config

class GitHubClient:
    """Client for interacting with GitHub API"""
    
    def __init__(self, config: Config):
        self.config = config
        self.github: Optional[Github] = None
        self.authenticated = False
    
    def authenticate(self, token: str) -> bool:
        """Authenticate with GitHub token"""
        try:
            self.github = Github(token)
            # Test authentication by getting user
            user = self.github.get_user()
            _ = user.login  # Access property to validate token
            self.config.set('github_token', token)
            self.authenticated = True
            return True
        except GithubException as e:
            self.authenticated = False
            return False
    
    def get_user(self):
        """Get authenticated user"""
        if not self.authenticated:
            return None
        return self.github.get_user()
    
    def get_repositories(self) -> List[Repository]:
        """Get all repositories for authenticated user"""
        if not self.authenticated:
            return []
        user = self.github.get_user()
        return list(user.get_repos())
    
    def get_repository(self, owner: str, repo_name: str) -> Optional[Repository]:
        """Get a specific repository"""
        if not self.authenticated:
            return None
        try:
            return self.github.get_repo(f"{owner}/{repo_name}")
        except GithubException:
            return None
    
    def create_repository(self, name: str, description: str = "", 
                         private: bool = False, auto_init: bool = True) -> Optional[Repository]:
        """Create a new repository"""
        if not self.authenticated:
            return None
        user = self.github.get_user()
        try:
            return user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init
            )
        except GithubException:
            return None
    
    def get_repository_contents(self, repo: Repository, path: str = "") -> List[Any]:
        """Get contents of a repository path"""
        try:
            contents = repo.get_contents(path)
            if isinstance(contents, list):
                return contents
            return [contents]
        except GithubException:
            return []
    
    def upload_file(self, repo: Repository, path: str, content: str, 
                   message: str, branch: str = "main") -> bool:
        """Upload or update a file in repository"""
        try:
            # Check if file exists
            try:
                file_content = repo.get_contents(path, ref=branch)
                repo.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=file_content.sha,
                    branch=branch
                )
            except GithubException:
                # File doesn't exist, create it
                repo.create_file(
                    path=path,
                    message=message,
                    content=content,
                    branch=branch
                )
            return True
        except GithubException as e:
            print(f"Error uploading file: {e}")
            return False
    
    def delete_file(self, repo: Repository, path: str, 
                   message: str, branch: str = "main") -> bool:
        """Delete a file from repository"""
        try:
            file_content = repo.get_contents(path, ref=branch)
            repo.delete_file(
                path=path,
                message=message,
                sha=file_content.sha,
                branch=branch
            )
            return True
        except GithubException:
            return False
    
    def create_branch(self, repo: Repository, branch_name: str, 
                     source_branch: str = "main") -> bool:
        """Create a new branch"""
        try:
            source = repo.get_branch(source_branch)
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source.commit.sha
            )
            return True
        except GithubException:
            return False
    
    def get_branches(self, repo: Repository) -> List[Any]:
        """Get all branches of a repository"""
        try:
            return list(repo.get_branches())
        except GithubException:
            return []
    
    def create_release(self, repo: Repository, tag: str, name: str, 
                      message: str, draft: bool = False, 
                      prerelease: bool = False) -> Optional[Any]:
        """Create a GitHub release"""
        try:
            return repo.create_git_release(
                tag=tag,
                name=name,
                message=message,
                draft=draft,
                prerelease=prerelease,
                generate_release_notes=True
            )
        except GithubException:
            return None
    
    def upload_asset_to_release(self, release, asset_path: str) -> bool:
        """Upload an asset to a release"""
        try:
            release.upload_asset(asset_path)
            return True
        except GithubException:
            return False
    
    def enable_pages(self, repo: Repository, branch: str = "main", 
                    path: str = "/") -> bool:
        """Enable GitHub Pages for repository"""
        try:
            # Use the repository's API to enable/update Pages
            # The PyGithub library may not have direct support for this
            # so we use the underlying request method
            import requests
            headers = {
                "Authorization": f"token {self.config.get('github_token')}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "source": {
                    "branch": branch,
                    "path": path
                }
            }
            response = requests.post(
                f"{repo.url}/pages",
                headers=headers,
                json=data
            )
            return response.status_code in [200, 201, 204]
        except Exception:
            return False
    
    def create_pages_workflow(self, repo: Repository, workflow_content: str, 
                             branch: str = "main", message: str = "Add GitHub Actions workflow for Pages") -> bool:
        """Create or update GitHub Actions workflow file for Pages"""
        try:
            workflow_path = ".github/workflows/deploy-pages.yml"
            return self.upload_file(repo, workflow_path, workflow_content, message, branch)
        except Exception as e:
            print(f"Error creating Pages workflow: {e}")
            return False
    
    def upload_pages_content(self, repo: Repository, local_folder: Path, 
                            repo_path: str = "", branch: str = "main") -> Dict[str, bool]:
        """Upload local folder contents to repository for Pages deployment"""
        try:
            results = {}
            
            # Get all files in the local folder
            if local_folder.is_file():
                files = [local_folder]
            else:
                files = list(local_folder.rglob("*"))
                files = [f for f in files if f.is_file()]
            
            for file_path in files:
                try:
                    # Calculate relative path
                    relative_path = file_path.relative_to(local_folder)
                    repo_file_path = str(Path(repo_path) / relative_path).replace("\\", "/")
                    
                    # Read file content
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    # For binary files, we need to encode as base64
                    # For text files, we can upload as string
                    try:
                        content_str = content.decode('utf-8')
                        success = self.upload_file(
                            repo, 
                            repo_file_path, 
                            content_str, 
                            f"Upload {relative_path} for Pages", 
                            branch
                        )
                    except UnicodeDecodeError:
                        # Binary file - skip for now or handle with base64
                        print(f"Skipping binary file: {file_path}")
                        success = False
                    
                    results[str(relative_path)] = success
                except Exception as e:
                    print(f"Error uploading {file_path}: {e}")
                    results[str(file_path.relative_to(local_folder))] = False
            
            return results
        except Exception as e:
            print(f"Error uploading Pages content: {e}")
            return {}
    
    def get_wiki_pages(self, repo: Repository) -> List[str]:
        """Get list of wiki pages"""
        try:
            # GitHub API doesn't directly support wiki, need to use git
            # This is a placeholder for wiki functionality
            return []
        except GithubException:
            return []
    
    def upload_wiki_page(self, repo: Repository, title: str, content: str, 
                        message: str = "Update wiki page") -> bool:
        """Upload or update a wiki page"""
        try:
            from git import Repo
            import tempfile
            import shutil
            from pathlib import Path
            
            # Wiki repos are at: https://github.com/owner/repo.wiki.git
            wiki_url = f"{repo.url}.wiki"
            
            # Create temp directory for cloning
            temp_dir = Path(tempfile.mkdtemp())
            
            try:
                # Clone the wiki repository
                Repo.clone_from(wiki_url, temp_dir)
                wiki_repo = Repo(temp_dir)
                
                # Create/update the markdown file
                # Wiki pages use the title as filename with .md extension
                # Spaces are replaced with hyphens
                filename = f"{title.replace(' ', '-')}.md"
                file_path = temp_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Stage, commit and push
                wiki_repo.index.add([filename])
                
                # Configure git if needed
                git_config = self.config.get('git_config', {})
                author_name = git_config.get('user.name', 'GitHub Commander')
                author_email = git_config.get('user.email', 'github-commander@example.com')
                
                from git import Actor
                author = Actor(author_name, author_email)
                
                wiki_repo.index.commit(message, author=author, committer=author)
                
                # Set up remote with authentication
                token = self.config.get('github_token', '')
                if token:
                    auth_url = wiki_url.replace('https://', f'https://{token}@')
                    wiki_repo.remotes.origin.set_url(auth_url)
                
                wiki_repo.remotes.origin.push()
                
                return True
            finally:
                # Clean up temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                
        except Exception as e:
            print(f"Error uploading wiki page: {e}")
            return False
    
    def upload_wiki_folder(self, repo: Repository, folder_path: Path, 
                          message: str = "Upload wiki pages") -> Dict[str, bool]:
        """Upload all markdown files from a folder to wiki"""
        try:
            from git import Repo
            import tempfile
            import shutil
            from pathlib import Path
            
            wiki_url = f"{repo.url}.wiki"
            temp_dir = Path(tempfile.mkdtemp())
            results = {}
            
            try:
                Repo.clone_from(wiki_url, temp_dir)
                wiki_repo = Repo(temp_dir)
                
                # Find all markdown files
                md_files = list(folder_path.glob("*.md")) + list(folder_path.glob("*.markdown"))
                
                for md_file in md_files:
                    try:
                        # Copy file to wiki repo
                        filename = md_file.name
                        dest_path = temp_dir / filename
                        shutil.copy2(md_file, dest_path)
                        
                        # Use filename (without extension) as page title
                        title = md_file.stem
                        results[title] = True
                    except Exception as e:
                        print(f"Error copying {md_file}: {e}")
                        results[md_file.stem] = False
                
                # Stage all files
                wiki_repo.index.add([f.name for f in temp_dir.glob("*.md")])
                wiki_repo.index.add([f.name for f in temp_dir.glob("*.markdown")])
                
                # Commit
                git_config = self.config.get('git_config', {})
                author_name = git_config.get('user.name', 'GitHub Commander')
                author_email = git_config.get('user.email', 'github-commander@example.com')
                
                from git import Actor
                author = Actor(author_name, author_email)
                
                wiki_repo.index.commit(message, author=author, committer=author)
                
                # Push with authentication
                token = self.config.get('github_token', '')
                if token:
                    auth_url = wiki_url.replace('https://', f'https://{token}@')
                    wiki_repo.remotes.origin.set_url(auth_url)
                
                wiki_repo.remotes.origin.push()
                
                return results
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
                
        except Exception as e:
            print(f"Error uploading wiki folder: {e}")
            return {}
    
    def search_repositories(self, query: str) -> List[Repository]:
        """Search for repositories"""
        if not self.authenticated:
            return []
        try:
            return list(self.github.search_repositories(query))
        except GithubException:
            return []
