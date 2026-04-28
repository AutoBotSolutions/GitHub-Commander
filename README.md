# GitHub Commander - Linux Desktop GUI

A comprehensive GitHub desktop application for Linux that provides FTP-like functionality with full GitHub deployment capabilities.

## Features

- **FTP-like Interface**: Dual-pane browser for local files and GitHub repositories
- **File Operations**: Upload/download files and folders with drag & drop
- **GitHub Pages**: Deploy and manage GitHub Pages sites
- **Wiki Management**: Upload and manage repository wikis
- **Package Management**: Upload packages by folder (npm, pip, cargo, etc.)
- **Git Operations**: Clone, commit, push, pull, branch management
- **Release Management**: Create and manage GitHub releases
- **Comprehensive Settings**: Configure all GitHub options and preferences
- **Authentication**: Secure GitHub token management

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Requirements

- Python 3.8+
- PyQt6
- PyGithub
- GitPython
- requests
- keyring
- pyperclip

## Usage

1. Launch the application
2. Authenticate with your GitHub token
3. Browse repositories or clone new ones
4. Upload/download files using the FTP-like interface
5. Deploy to GitHub Pages, manage wikis, or upload packages

## License

MIT License
