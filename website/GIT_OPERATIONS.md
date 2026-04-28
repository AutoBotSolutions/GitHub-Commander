# Git Operations Guide

This guide covers Git operations including commit, push, pull, and branch management using GitHub Commander.

## Overview

The Git Panel provides comprehensive Git operations for local repositories:
- Commit changes
- Push to remote
- Pull from remote
- Create and manage branches
- View repository status

## Git Panel Interface

The Git Panel includes:

- **Repository Selection** - Choose local repository
- **Status Display** - Show current branch and changes
- **Commit Message** - Enter commit message
- **Action Buttons** - Commit, Push, Pull, Create Branch
- **Branch List** - View and switch branches
- **File Changes** - View modified and untracked files

## Committing Changes

### Viewing Changes

1. Go to the Git Panel
2. Select a local repository
3. The status area shows:
   - Current branch
   - Modified files (in red)
   - Untracked files (in blue)
   - Staged changes (in green)

### Staging Files

Files are automatically staged when you commit. To stage specific files:
1. Select files in the status area
2. They will be included in the commit

### Committing

1. Go to the Git Panel
2. Select a local repository
3. Review the changes in the status area
4. Enter a commit message
5. Click "Commit"
6. Changes will be committed to the local repository

### Commit Message Guidelines

Write clear, descriptive commit messages:

```
Good: "Add user authentication feature"
Bad: "update files"

Good: "Fix login bug with special characters"
Bad: "fix stuff"

Good: "Update dependencies to latest versions"
Bad: "deps"
```

### Commit Message Format

Consider using conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Example:
```
feat: add user authentication

- Add login form
- Implement OAuth
- Add session management
```

## Pushing Changes

### Pushing to Remote

1. Go to the Git Panel
2. Select a local repository
3. Click "Push"
4. Changes will be pushed to the remote repository

### Push Options

- **Branch** - Which branch to push (default: current)
- **Force Push** - Overwrite remote (use with caution)

### Force Push

Force push overwrites remote history. Use only when:
- You know what you're doing
- Collaborators are aware
- History needs to be rewritten

**Warning:** Force push can cause issues for collaborators.

### Push to Specific Branch

1. Select branch from dropdown
2. Click "Push"
3. Changes pushed to selected branch

## Pulling Changes

### Pulling from Remote

1. Go to the Git Panel
2. Select a local repository
3. Click "Pull"
4. Changes from remote will be merged into your local branch

### Pull Options

- **Branch** - Which branch to pull from (default: current)
- **Strategy** - Merge or rebase (future feature)

### Handling Merge Conflicts

If conflicts occur during pull:
1. Conflicting files will be marked
2. Open files and resolve conflicts
3. Mark conflicts as resolved
4. Commit the merge

## Branch Management

### Creating Branches

1. Go to the Git Panel
2. Select a local repository
3. Enter the new branch name
4. Select the source branch
5. Click "Create Branch"
6. The new branch will be created

### Branch Naming Conventions

Use descriptive branch names:
- `feature/add-login`
- `bugfix/fix-auth-error`
- `hotfix/security-patch`
- `docs/update-readme`
- `refactor/cleanup-code`

### Switching Branches

1. Go to the Git Panel
2. Select a local repository
3. Select the branch from the dropdown
4. Click "Checkout"
5. You will switch to the selected branch

**Note:** Uncommitted changes may cause issues. Commit or stash before switching.

### Viewing Branches

1. Go to the Git Panel
2. Select a local repository
3. All local branches are displayed
4. Current branch is highlighted

### Deleting Branches

To delete a branch:
1. Switch to a different branch
2. Use Git command line: `git branch -D branch-name`
3. Or use GitHub web interface

## Repository Status

### Viewing Status

1. Go to the Git Panel
2. Select a local repository
3. The status area shows:
   - **On branch** - Current branch name
   - **Changes not staged** - Modified files
   - **Untracked files** - New files
   - **Changes to be committed** - Staged files

### Status Indicators

- **Modified (M)** - File has changes
- **Added (A)** - New file staged
- **Deleted (D)** - File deleted
- **Renamed (R)** - File renamed
- **Untracked (??)** - New file not tracked

## Git Configuration

### Setting User Name and Email

Configure in Settings:
1. Go to Settings
2. Find "Git Configuration"
3. Set:
   - **User Name** - Your name
   - **User Email** - Your email
4. Click "Save"

Or use Git command line:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Why Configuration Matters

Git uses this information for:
- Commit author attribution
- Commit history
- Collaboration identification

## Advanced Operations

### Stashing Changes

To temporarily save changes:
```bash
git stash
```

To restore stashed changes:
```bash
git stash pop
```

### Viewing History

To view commit history:
```bash
git log
```

To view file history:
```bash
git log --follow filename
```

### Resetting Changes

To discard local changes:
```bash
git checkout -- filename
```

To reset to previous commit:
```bash
git reset --hard HEAD~1
```

**Warning:** These operations can't be undone.

## Troubleshooting

### "Failed to commit"

**Causes:**
- No changes to commit
- Merge conflicts
- File locked by another process

**Solutions:**
- Verify you have changes
- Resolve conflicts first
- Close files that might be locked

### "Failed to push"

**Causes:**
- No remote configured
- Authentication issues
- Diverged history
- Network issues

**Solutions:**
- Add remote: `git remote add origin url`
- Check authentication
- Pull first, then push
- Check internet connection

### "Failed to pull"

**Causes:**
- Merge conflicts
- Authentication issues
- Network issues
- Diverged history

**Solutions:**
- Resolve conflicts
- Check authentication
- Check internet connection
- Consider rebase instead of merge

### Merge Conflicts

**Symptoms:**
- Pull fails with conflict messages
- Files marked with conflict markers

**Solutions:**
1. Open conflicting files
2. Look for `<<<<<<<` markers
3. Choose which version to keep
4. Remove conflict markers
5. Mark as resolved
6. Commit the merge

## Best Practices

### Commit Workflow

1. Make small, frequent commits
2. Write descriptive messages
3. Commit related changes together
4. Review before committing
5. Test after committing

### Branch Workflow

1. Create feature branches
2. Work on features in branches
3. Test thoroughly
4. Merge back to main when done
5. Delete feature branches

### Collaboration

1. Pull before pushing
2. Resolve conflicts promptly
3. Communicate with team
4. Use pull requests for review
5. Keep main branch stable

## Next Steps

After mastering Git operations, explore:
- [File Operations](FILE_OPERATIONS.md) - Upload and download files
- [Release Management](RELEASE_MANAGEMENT.md) - Create releases
