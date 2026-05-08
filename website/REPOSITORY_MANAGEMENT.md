# Repository Management Guide

This guide covers how to browse, clone, and create repositories using GitHub Commander.

## Main Interface Overview

The main interface consists of several panels accessible via tabs:

- **Git Panel** - Clone, commit, push, pull, and manage branches
- **GitHub File Browser** - Browse repository contents
- **Local File Browser** - Browse local files
- **Wiki Panel** - Manage repository wikis
- **Pages Panel** - Deploy GitHub Pages sites
- **Packages Panel** - Upload packages to registries
- **Releases Panel** - Create and manage releases

## Browsing Repositories

### Viewing Your Repositories

1. After authentication, your repositories will appear in the repository list
2. Click on a repository to select it
3. The repository details will be displayed in the info panel, including:
   - Repository name and description
   - Owner information
   - Branch information
   - Last updated date
   - Star and fork counts

### Searching Repositories

1. Use the search box in the repository panel
2. Enter repository name or keyword
3. Results will filter in real-time

### Repository Information Panel

When a repository is selected, you'll see:
- **Full Name** - owner/repository-name
- **Description** - Repository description
- **Language** - Primary programming language
- **Stars** - Number of stars
- **Forks** - Number of forks
- **Open Issues** - Number of open issues
- **Default Branch** - Usually "main" or "master"

## Cloning a Repository

### Basic Clone

1. Go to the Git Panel
2. Enter the repository URL or select from your repositories
3. Choose the destination folder (default: `~/github-projects`)
4. Click "Clone"
5. The repository will be cloned to your local machine

### Clone with Specific Branch

1. Go to the Git Panel
2. Enter the repository URL
3. Select the branch from the dropdown
4. Choose destination folder
5. Click "Clone"

### Clone from Repository List

1. Browse your repositories in the repository panel
2. Right-click on a repository
3. Select "Clone"
4. Confirm destination folder
5. Click "Clone"

### Clone Options

- **Destination Folder** - Where to clone the repository
- **Branch** - Which branch to clone (default: default branch)
- **Recursive** - Clone submodules (if applicable)

## Creating a New Repository

### Create on GitHub

1. Go to the Git Panel
2. Click "Create Repository"
3. Fill in the repository details:
   - **Repository Name** - Required, unique to your account
   - **Description** - Optional, describes the repository
   - **Visibility** - Public or Private
   - **Auto Initialize** - Create initial README and .gitignore
4. Click "Create"
5. The repository will be created on GitHub

### Repository Creation Options

- **Initialize with README** - Creates a README.md file
- **Add .gitignore** - Select a .gitignore template
- **Choose License** - Select an open source license
- **Private Repository** - Only you can access (requires paid plan for private repos on some accounts)

## Repository Actions

### Opening a Repository

1. Select a repository from the list
2. Click "Open" or double-click
3. The repository will open in the file browser

### Repository Settings

Access repository-specific settings by:
1. Selecting a repository
2. Clicking "Settings" button
3. Configure repository-specific options

### Deleting a Repository

**Warning:** This action cannot be undone.

1. Select the repository
2. Click "Delete Repository"
3. Confirm by typing the repository name
4. Click "Delete"

## Working with Local Repositories

### Adding Local Repository

1. Go to the Git Panel
2. Click "Add Local Repository"
3. Browse to the local repository folder
4. Click "Add"
5. The repository will appear in your local list

### Opening Local Repository

1. Go to the Git Panel
2. Select from "Local Repositories" tab
3. Click "Open"
4. The repository will open in the file browser

### Removing Local Repository

1. Go to the Git Panel
2. Select the local repository
3. Click "Remove"
4. This only removes it from the list, doesn't delete files

## Repository Branches

### Viewing Branches

1. Select a repository
2. Branches are displayed in the repository info panel
3. Current branch is highlighted

### Creating Branches

See [Git Operations](GIT_OPERATIONS.md) for detailed branch management.

## Repository Statistics

### Viewing Statistics

For any repository, you can view:
- Commit history
- Contributors
- Activity graphs
- Code frequency

Access these from the repository info panel.

## Next Steps

After managing repositories, explore:
- [File Operations](FILE_OPERATIONS.md) - Upload and download files
- [Git Operations](GIT_OPERATIONS.md) - Commit, push, and pull changes
- [Wiki Management](WIKI_MANAGEMENT.md) - Manage repository wikis
