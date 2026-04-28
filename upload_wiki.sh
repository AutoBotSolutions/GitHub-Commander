#!/bin/bash
# Script to upload wiki pages to GitHub

# Configuration
WIKI_REPO="https://github.com/AutoBotSolutions/GitHub-Commander.wiki.git"
WEBSITE_DIR="/home/robbie/Desktop/github-commander/website"
TEMP_DIR="/tmp/github-commander-wiki"

echo "Cloning wiki repository..."
git clone "$WIKI_REPO" "$TEMP_DIR"

echo "Copying wiki pages..."
cp "$WEBSITE_DIR"/*.md "$TEMP_DIR/"

cd "$TEMP_DIR"

echo "Adding files to git..."
git add .

echo "Committing changes..."
git commit -m "Update wiki documentation"

echo "Pushing to GitHub..."
git push origin master

echo "Cleaning up..."
cd /
rm -rf "$TEMP_DIR"

echo "Wiki pages uploaded successfully!"
