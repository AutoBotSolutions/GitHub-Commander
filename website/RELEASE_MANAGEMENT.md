# Release Management Guide

This guide covers how to create and manage GitHub releases using GitHub Commander.

## Overview

GitHub releases are versioned snapshots of your code. They include:
- Git tags
- Release notes
- Binary assets
- Source code archives

GitHub Commander provides:
- Create releases
- Upload release assets
- View release history

## Releases Panel Interface

The Releases Panel includes:

- **Release List** - View all releases
- **Create Release** - Form to create new releases
- **Upload Asset** - Attach files to releases
- **Release Details** - View release information

## Creating a Release

### Basic Release Creation

1. Select a repository
2. Go to the Releases Panel
3. Enter release details:
   - **Tag Version** - e.g., v1.0.0
   - **Release Title** - e.g., "Version 1.0.0"
   - **Release Notes** - Description of changes
4. Check/uncheck options:
   - **Draft** - Save as draft (not published)
   - **Pre-release** - Mark as pre-release
5. Click "Create Release"
6. The release will be created on GitHub

### Tag Version Format

Use semantic versioning:
- **v1.0.0** - Major version 1, minor 0, patch 0
- **v1.2.3** - Major 1, minor 2, patch 3
- **v2.0.0-beta.1** - Pre-release version

### Release Title Guidelines

- Match tag version (e.g., "Version 1.0.0")
- Or use descriptive title (e.g., "Initial Release")
- Keep it concise and clear

### Writing Release Notes

Good release notes include:
- Summary of changes
- New features
- Bug fixes
- Breaking changes
- Upgrade instructions
- Known issues

Example:
```
## Version 1.0.0

This is the initial release of GitHub Commander.

### New Features
- Repository browsing and cloning
- File upload and download
- Wiki management
- GitHub Pages deployment

### Bug Fixes
- Fixed authentication issues
- Resolved upload failures

### Known Issues
- Wiki page listing not fully supported
- Large file uploads may timeout

### Upgrade Instructions
No previous version to upgrade from.
```

### Draft Releases

Draft releases are:
- Not visible to the public
- Can be edited before publishing
- Useful for preparation
- Published when ready

### Pre-release Releases

Pre-release releases are:
- Marked as pre-release on GitHub
- Not shown as latest
- Useful for beta/alpha versions
- Can be promoted to stable later

## Uploading Release Assets

### What Are Release Assets?

Release assets are files attached to a release:
- Compiled binaries
- Installation packages
- Documentation archives
- Source code archives
- Checksum files

### Uploading an Asset

1. Select a repository
2. Go to the Releases Panel
3. Select an existing release from the list
4. Click "Upload Asset"
5. Select the file to upload
6. The asset will be attached to the release

### Asset Guidelines

- Keep file sizes reasonable (GitHub has limits)
- Use descriptive filenames
- Include version in filename
- Provide checksums for verification
- Include installation instructions

### Multiple Assets

You can upload multiple assets to a single release:
1. Select the release
2. Upload each asset one at a time
3. All assets appear on the release page

## Viewing Releases

### Release List

1. Select a repository
2. Go to the Releases Panel
3. All releases are listed with:
   - Tag name
   - Release title
   - Published date
   - Draft/Pre-release status

### Release Details

Click on a release to view:
- Release notes
- Attached assets
- Source code archive
- Commit information

## Release Best Practices

### Versioning

Follow semantic versioning:
- **MAJOR** - Incompatible changes
- **MINOR** - New features (backwards compatible)
- **PATCH** - Bug fixes (backwards compatible)

Example progression:
- v1.0.0 → v1.0.1 → v1.1.0 → v2.0.0

### Release Workflow

1. Create release branch
2. Implement changes
3. Update version numbers
4. Update CHANGELOG
5. Tag the commit
6. Create release
7. Upload assets
8. Publish release

### Release Notes

Write comprehensive notes:
- Group changes by category
- Use consistent formatting
- Include upgrade instructions
- Highlight breaking changes
- Link to relevant issues/PRs

### Asset Management

- Include source code archive (auto-generated)
- Upload compiled binaries
- Provide checksums (SHA256)
- Include installation guides
- Keep assets organized

## Release Workflow Example

### For a New Feature

1. Create feature branch: `feature/new-feature`
2. Implement and test the feature
3. Merge to main branch
4. Bump version: v1.1.0
5. Update CHANGELOG
6. Tag commit: `git tag v1.1.0`
7. Push tag: `git push origin v1.1.0`
8. Create release in GitHub Commander
9. Write release notes
10. Upload assets if needed
11. Publish release

### For a Bug Fix

1. Create fix branch: `bugfix/critical-issue`
2. Implement and test the fix
3. Merge to main branch
4. Bump version: v1.0.1
5. Update CHANGELOG
6. Tag commit: `git tag v1.0.1`
7. Push tag
8. Create release
9. Write release notes
10. Publish release

## Troubleshooting

### "Failed to create release"

**Causes:**
- Tag already exists
- Invalid tag format
- Authentication issues
- Repository permissions

**Solutions:**
- Use unique tag version
- Use semantic versioning format
- Check authentication
- Verify write permissions

### "Failed to upload asset"

**Causes:**
- File too large
- Invalid file type
- Network issues
- Authentication issues

**Solutions:**
- Keep files under 2GB (GitHub limit)
- Use supported file types
- Check internet connection
- Verify authentication

### "Tag already exists"

**Solutions:**
- Delete existing tag: `git tag -d v1.0.0`
- Delete remote tag: `git push origin :refs/tags/v1.0.0`
- Use different version
- Or update existing release

## Next Steps

After managing releases, explore:
- [Package Management](PACKAGE_MANAGEMENT.md) - Publish packages
- [Git Operations](GIT_OPERATIONS.md) - Tag and version control
