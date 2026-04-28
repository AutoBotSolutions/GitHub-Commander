# Installation Guide

This guide will help you install and set up GitHub Commander on your Linux system.

## Prerequisites

Before installing GitHub Commander, ensure you have the following:

- **Python 3.8 or higher** - Required for running the application
- **Git** - Required for Git operations
- **A GitHub account** - Required for accessing GitHub features

### Checking Prerequisites

```bash
# Check Python version
python3 --version

# Check Git installation
git --version
```

## Installation Steps

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd github-commander
```

Or download and extract the archive from GitHub.

### 2. Install Dependencies

GitHub Commander uses a virtual environment for dependency management. You have two options:

#### Option A: Using the Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: System-wide Installation

```bash
pip install -r requirements.txt
```

### 3. Run the Application

#### Using Virtual Environment

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the application
python main.py
```

#### Using System Python

```bash
python3 main.py
```

## Dependencies

The following dependencies are included in `requirements.txt`:

- **PySide6==6.11.0** - Qt framework for the GUI
- **PyGithub==2.1.1** - GitHub API library
- **GitPython==3.1.40** - Git operations library
- **requests==2.31.0** - HTTP library
- **keyring==24.2.0** - Secure credential storage
- **pyperclip==1.8.2** - Clipboard operations

## Troubleshooting Installation

### Python Not Found

If you get "python3: command not found", install Python:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Git Not Found

If you get "git: command not found", install Git:

```bash
sudo apt update
sudo apt install git
```

### Permission Denied

If you get permission errors, try:

```bash
pip install --user -r requirements.txt
python3 main.py
```

### PySide6 Installation Issues

If PySide6 fails to install, try:

```bash
pip install --upgrade pip
pip install PySide6
```

## Upgrading

To upgrade GitHub Commander to the latest version:

```bash
# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Uninstallation

To remove GitHub Commander:

```bash
# Deactivate virtual environment
deactivate

# Remove the application directory
rm -rf github-commander

# Optionally, remove the configuration directory
rm -rf ~/.github-commander
```

## Next Steps

After installation, proceed to [Authentication](AUTHENTICATION.md) to configure your GitHub token.
