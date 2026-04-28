#!/usr/bin/env python3
"""
Script to upload wiki pages to GitHub
"""

import sys
from pathlib import Path
from github import Github
from config import Config

def main():
    # Load configuration
    config = Config()
    token = config.get('github_token')
    
    if not token:
        print("Error: No GitHub token found in config")
        print("Please set your GitHub token in settings first")
        sys.exit(1)
    
    # Authenticate with GitHub
    github = Github(token)
    
    try:
        # Get the repository
        repo = github.get_repo("AutoBotSolutions/GitHub-Commander")
        print(f"Connected to repository: {repo.full_name}")
        
        # Import git operations for wiki upload
        from git import Repo
        import tempfile
        import shutil
        
        # Wiki repo URL
        wiki_url = f"{repo.url}.wiki"
        print(f"Wiki URL: {wiki_url}")
        
        # Create temp directory
        temp_dir = Path(tempfile.mkdtemp())
        print(f"Cloning wiki to: {temp_dir}")
        
        try:
            # Clone the wiki repository
            Repo.clone_from(wiki_url, temp_dir)
            wiki_repo = Repo(temp_dir)
            
            # Videos directory
            videos_dir = Path("/home/robbie/Desktop/github-commander/videos")
            
            # Find all markdown files
            md_files = list(videos_dir.glob("*.md"))
            print(f"Found {len(md_files)} markdown files to upload")
            
            # Copy files to wiki repo
            for md_file in md_files:
                try:
                    filename = md_file.name
                    dest_path = temp_dir / filename
                    shutil.copy2(md_file, dest_path)
                    print(f"Copied: {filename}")
                except Exception as e:
                    print(f"Error copying {md_file}: {e}")
            
            # Stage all files
            wiki_repo.index.add([f.name for f in temp_dir.glob("*.md")])
            
            # Commit
            git_config = config.get('git_config', {})
            author_name = git_config.get('user.name', 'Robert Trenaman')
            author_email = git_config.get('user.email', 'autobotsolution@gmail.com')
            
            from git import Actor
            author = Actor(author_name, author_email)
            
            wiki_repo.index.commit("Update wiki documentation", author=author, committer=author)
            
            # Push with authentication
            auth_url = wiki_url.replace('https://', f'https://{token}@')
            wiki_repo.remotes.origin.set_url(auth_url)
            
            print("Pushing to GitHub...")
            wiki_repo.remotes.origin.push()
            
            print("Wiki pages uploaded successfully!")
            
        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
