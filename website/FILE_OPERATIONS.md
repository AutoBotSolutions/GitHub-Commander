# File Operations Guide

This guide covers how to upload, download, and manage files using GitHub Commander's FTP-like interface.

## Overview

GitHub Commander provides a dual-pane interface for file operations:
- **GitHub File Browser** - Browse repository contents on GitHub
- **Local File Browser** - Browse local files on your system

Files can be transferred between panes using drag-and-drop or context menus.

## Uploading Files

### Method 1: Drag and Drop

1. Select a repository
2. Navigate to the Local File Browser
3. Select the file(s) you want to upload
4. Drag and drop to the GitHub File Browser
5. Enter a commit message
6. Click "Upload"

### Method 2: Context Menu

1. Select a repository
2. Navigate to the Local File Browser
3. Right-click the file you want to upload
4. Select "Upload to GitHub"
5. Choose the destination path in the repository
6. Enter a commit message
7. Click "Upload"

### Batch Upload

1. Select multiple files in the Local File Browser
2. Drag and drop or use context menu
3. All selected files will be uploaded
4. Enter a commit message for the batch
5. Click "Upload"

### Upload Options

- **Destination Path** - Where to place the file in the repository
- **Commit Message** - Description of the changes
- **Branch** - Which branch to commit to (default: main)
- **Overwrite** - Replace existing files (default: prompt)

### Upload Progress

- Progress bar shows upload status
- Success/failure notifications appear
- Failed uploads can be retried

## Downloading Files

### Method 1: Drag and Drop

1. Select a repository
2. Navigate to the GitHub File Browser
3. Select the file(s) you want to download
4. Drag and drop to the Local File Browser
5. Choose the destination folder
6. Click "Download"

### Method 2: Context Menu

1. Navigate to the GitHub File Browser
2. Right-click the file you want to download
3. Select "Download"
4. Choose the destination folder
5. Click "Download"

### Batch Download

1. Select multiple files in the GitHub File Browser
2. Drag and drop or use context menu
3. Choose destination folder
4. All selected files will be downloaded

### Download Options

- **Destination Folder** - Where to save files locally
- **Preserve Structure** - Maintain directory structure
- **Overwrite** - Replace existing local files (default: prompt)

## Deleting Files

### Deleting from Repository

1. Navigate to the GitHub File Browser
2. Right-click the file you want to delete
3. Select "Delete"
4. Confirm the deletion
5. Enter a commit message
6. Click "Delete"

**Warning:** This permanently deletes the file from the repository. The deletion can be undone by reverting the commit.

### Batch Delete

1. Select multiple files
2. Right-click and select "Delete"
3. Confirm deletion
4. Enter commit message
5. Click "Delete"

## Creating Files

### Create New File in Repository

1. Navigate to the GitHub File Browser
2. Right-click in the file list
3. Select "New File"
4. Enter the file name
5. The file editor will open
6. Enter file content
7. Click "Save"
8. Enter a commit message
9. Click "Commit"

### Create New Folder

1. Navigate to the GitHub File Browser
2. Right-click in the file list
3. Select "New Folder"
4. Enter the folder name
5. Click "Create"

## Renaming Files and Folders

### Rename File

1. Right-click the file
2. Select "Rename"
3. Enter the new name
4. Click "Rename"
5. Enter a commit message
6. Click "Commit"

### Rename Folder

1. Right-click the folder
2. Select "Rename"
3. Enter the new name
4. Click "Rename"
5. Enter a commit message
6. Click "Commit"

## Viewing Files

### View File Content

1. Double-click a file in either browser
2. The file will open in the built-in viewer
3. Supported formats:
   - Text files (.txt, .md, .py, .js, etc.)
   - Images (.png, .jpg, .gif, .svg)
   - Code files with syntax highlighting

### Edit File

1. Double-click a file to open it
2. Make changes in the editor
3. Click "Save"
4. Enter a commit message
5. Click "Commit"

## File Information

### Viewing File Details

Right-click a file and select "Properties" to see:
- File size
- Last modified date
- File type
- SHA (for repository files)
- Author (for repository files)

## Comparing Files

### Compare Local and Remote

1. Select a file in the Local File Browser
2. Right-click and select "Compare with Remote"
3. Differences will be highlighted
4. Choose which changes to keep

## File Permissions

### Viewing Permissions

File permissions are displayed in the file list:
- `r` - Read
- `w` - Write
- `x` - Execute

GitHub doesn't support executable permissions for most file types.

## Large Files

### Large File Warning

GitHub has a 100 MB file size limit. Attempting to upload larger files will:
- Show a warning
- Prevent the upload
- Suggest using Git LFS (Large File Storage)

### Using Git LFS

For files larger than 100 MB:
1. Install Git LFS on your system
2. Initialize LFS in the repository
3. Track large files with LFS
4. Upload normally - LFS handles the rest

## Binary Files

### Uploading Binary Files

Binary files (images, executables, etc.) can be uploaded:
1. Select the binary file
2. Upload using drag-and-drop or context menu
3. The file will be uploaded in binary mode

### Viewing Binary Files

Binary files can be viewed as:
- Hex dump
- Raw binary
- External application (if configured)

## Hidden Files

### Showing Hidden Files

1. Go to Settings
2. Enable "Show Hidden Files"
3. Hidden files (starting with `.`) will be visible

Hidden files include:
- `.gitignore`
- `.env`
- Configuration files
- System files

## File Search

### Searching in Local Browser

1. Use the search box in the Local File Browser
2. Enter file name or pattern
3. Results filter in real-time

### Searching in GitHub Browser

1. Use the search box in the GitHub File Browser
2. Enter file name or pattern
3. Results filter in real-time

### Advanced Search

Use wildcards for pattern matching:
- `*.py` - All Python files
- `test_*` - Files starting with "test_"
- `*.md` - All Markdown files

## Next Steps

After mastering file operations, explore:
- [Git Operations](GIT_OPERATIONS.md) - Commit and push your changes
- [Wiki Management](WIKI_MANAGEMENT.md) - Upload documentation
- [GitHub Pages](GITHUB_PAGES.md) - Deploy websites
