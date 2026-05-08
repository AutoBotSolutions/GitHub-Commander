# Settings Guide

This guide covers all configuration options available in GitHub Commander.

## Accessing Settings

Access settings via:
- Main menu → Settings
- Keyboard shortcut: `Ctrl+,`
- Or click the Settings button in the main interface

## GitHub Settings

### GitHub Token

**Description:** Your GitHub Personal Access Token for authentication.

**How to Set:**
1. Generate token from GitHub.com
2. Paste token into the field
3. Click "Save"

**Storage:** Saved in `~/.github-commander/config.json`

**Security:** Never share your token or commit it to repositories.

**See:** [Authentication Guide](AUTHENTICATION.md) for detailed token setup.

## Repository Settings

### Clone Directory

**Description:** Default folder for cloning repositories.

**Default:** `~/github-projects`

**How to Change:**
1. Enter new path or browse
2. Click "Save"

**Note:** You can still specify a different location during clone operations.

### Auto Commit Message

**Description:** Default commit message used when no custom message is provided.

**Default:** "Update via GitHub Commander"

**How to Change:**
1. Enter your preferred message
2. Click "Save"

**Tip:** Use a meaningful default message for your workflow.

## Git Configuration

### User Name

**Description:** Your Git user name for commit attribution.

**Default:** (Empty - uses system default)

**How to Set:**
1. Enter your name
2. Click "Save"

**Example:** "John Doe"

### User Email

**Description:** Your Git email for commit attribution.

**Default:** (Empty - uses system default)

**How to Set:**
1. Enter your email
2. Click "Save"

**Example:** "john.doe@example.com"

**Why Important:** Git uses this to identify commit authors.

## UI Settings

### Theme

**Description:** Application color theme.

**Options:**
- Dark - Dark theme (default)
- Light - Light theme

**How to Change:**
1. Select theme from dropdown
2. Click "Save"
3. Restart application for changes to take effect

### Font Size

**Description:** Interface font size in points.

**Default:** 10

**Range:** 8 - 24

**How to Change:**
1. Enter desired size
2. Click "Save"
3. Restart application for changes to take effect

### Show Hidden Files

**Description:** Show files starting with `.` in file browsers.

**Default:** False (hidden)

**How to Change:**
1. Check/uncheck the box
2. Click "Save"
3. Changes take effect immediately

**Hidden Files Include:**
- `.gitignore`
- `.env`
- Configuration files
- System files

## Pages Settings

### Source Branch

**Description:** Default branch for GitHub Pages deployment.

**Default:** main

**Options:** main, master, gh-pages, or custom

**How to Change:**
1. Enter branch name
2. Click "Save"

**Note:** Can be overridden per deployment.

### Custom Domain

**Description:** Default custom domain for GitHub Pages.

**Default:** (Empty)

**How to Set:**
1. Enter your domain (e.g., `example.com`)
2. Click "Save"

**See:** [GitHub Pages Guide](GITHUB_PAGES.md) for domain setup.

## Wiki Settings

### Default Home

**Description:** Default home page name for wikis.

**Default:** Home

**How to Change:**
1. Enter page name
2. Click "Save"

**Note:** This is a suggestion, not enforced.

## Package Settings

### npm Registry

**Description:** Default npm registry URL for package uploads.

**Default:** https://registry.npmjs.org

**How to Change:**
1. Enter registry URL
2. Click "Save"

**Private Registries:** Enter your organization's registry URL.

### PyPI Repository

**Description:** Default PyPI repository URL for package uploads.

**Default:** https://pypi.org/simple

**How to Change:**
1. Enter repository URL
2. Click "Save"

**Test PyPI:** Use https://test.pypi.org/simple for testing.

## Configuration File

### Location

Configuration is stored in:
```
~/.github-commander/config.json
```

### Format

The configuration file is JSON:

```json
{
  "github_token": "your-token-here",
  "default_branch": "main",
  "clone_directory": "/home/user/github-projects",
  "auto_commit_message": "Update via GitHub Commander",
  "git_config": {
    "user.name": "Your Name",
    "user.email": "your.email@example.com"
  },
  "ui": {
    "theme": "dark",
    "font_size": 10,
    "show_hidden_files": false
  },
  "pages": {
    "source_branch": "main",
    "custom_domain": ""
  },
  "wiki": {
    "default_home": "Home"
  },
  "packages": {
    "npm_registry": "https://registry.npmjs.org",
    "pypi_repository": "https://pypi.org/simple"
  }
}
```

### Manual Editing

You can edit the config file manually:
1. Open `~/.github-commander/config.json` in a text editor
2. Make your changes
3. Save the file
4. Restart GitHub Commander

**Warning:** Invalid JSON will cause errors. Validate your changes.

### Resetting Configuration

To reset all settings to defaults:
1. Close GitHub Commander
2. Delete the config file:
   ```bash
   rm ~/.github-commander/config.json
   ```
3. Restart GitHub Commander
4. Configure as needed

## Import/Export Settings

### Export Settings

To backup your settings:
1. Copy `~/.github-commander/config.json`
2. Save to a safe location

### Import Settings

To restore settings:
1. Close GitHub Commander
2. Copy your backup config to `~/.github-commander/config.json`
3. Restart GitHub Commander

## Troubleshooting

### Settings Not Saving

**Causes:**
- File permission issues
- Disk full
- Config file locked

**Solutions:**
- Check file permissions
- Ensure disk space available
- Close other instances of GitHub Commander

### Invalid Configuration

**Symptoms:**
- Application fails to start
- Settings not loading

**Solutions:**
- Validate JSON syntax
- Reset configuration to defaults
- Check for typos in config file

### Configuration File Location

If config file is not in expected location:
1. Check for environment variables
2. Look in home directory
3. Check application logs for actual path

## Best Practices

### Security

- Never commit config file to repositories
- Use environment variables for sensitive data (advanced)
- Regularly rotate GitHub tokens
- Keep backup of configuration

### Backup

- Export settings before major changes
- Keep config file in version control (with secrets removed)
- Document your preferred settings

### Organization

- Use meaningful commit messages
- Document custom configurations
- Keep settings consistent across machines

## Next Steps

After configuring settings, explore:
- [Authentication](AUTHENTICATION.md) - Set up your GitHub token
- [Repository Management](REPOSITORY_MANAGEMENT.md) - Start using the application
