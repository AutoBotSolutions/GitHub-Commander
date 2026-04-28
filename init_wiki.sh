#!/bin/bash
# Script to initialize and upload wiki pages to GitHub

# Configuration
WIKI_REPO="https://github.com/AutoBotSolutions/GitHub-Commander.wiki.git"
WEBSITE_DIR="/home/robbie/Desktop/github-commander/website"
TEMP_DIR="/tmp/github-commander-wiki"

echo "Initializing wiki repository..."

# Create temporary directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

# Initialize git repository
git init

# Configure git
git config user.name "Robert Trenaman"
git config user.email "autobotsolution@gmail.com"

# Copy wiki pages
echo "Copying wiki pages..."
cp "$WEBSITE_DIR"/*.md .

# Add files to git
git add .

# Initial commit
git commit -m "Initialize GitHub Commander wiki documentation"

# Add remote
git remote add origin "$WIKI_REPO"

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin master

echo "Cleaning up..."
cd /
rm -rf "$TEMP_DIR"

echo "Wiki initialized and pages uploaded successfully!"
