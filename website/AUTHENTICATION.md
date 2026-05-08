# Authentication Guide

GitHub Commander requires authentication with GitHub to access most features. This guide will help you set up authentication using a GitHub Personal Access Token.

## Why Authentication is Required

GitHub Commander needs authentication to:
- Access your repositories
- Upload and download files
- Manage wikis and pages
- Create releases
- Perform Git operations

## Setting Up Your GitHub Token

### Step 1: Generate a Personal Access Token

1. Go to [GitHub.com](https://github.com)
2. Click on your profile picture → Settings
3. Navigate to Developer settings → Personal access tokens → Tokens (classic)
4. Click "Generate new token (classic)"
5. Enter a descriptive note (e.g., "GitHub Commander")
6. Select the following scopes:

   **Required Scopes:**
   - `repo` - Full control of private repositories
   - `workflow` - Update GitHub Action workflows
   - `delete_repo` - Delete repositories

   **Optional Scopes:**
   - `user` - Access user information
   - `admin:org` - Manage organization repositories

7. Select an expiration period (recommended: 90 days or less)
8. Click "Generate token"
9. **Important:** Copy the token immediately - you won't be able to see it again

### Step 2: Add Token to GitHub Commander

1. Launch GitHub Commander
2. Click on "Settings" in the main menu or press `Ctrl+,`
3. Find the "GitHub Token" field
4. Paste your Personal Access Token
5. Click "Save"

The token will be saved securely in `~/.github-commander/config.json`.

## Token Security

### Best Practices

- **Never share your token** with anyone
- **Don't commit tokens** to repositories
- **Use short expiration periods** (30-90 days)
- **Rotate tokens regularly** for better security
- **Use different tokens** for different applications
- **Revoke unused tokens** from GitHub settings

### Where Tokens Are Stored

Your token is stored locally in:
```
~/.github-commander/config.json
```

This file is only accessible by your user account. Ensure your system is secured with proper permissions.

### Revoking a Token

If your token is compromised or no longer needed:

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Find the token you want to revoke
3. Click "Delete" or "Revoke"
4. Generate a new token if needed
5. Update the token in GitHub Commander settings

## Verifying Authentication

After adding your token, verify it works:

1. Try to list your repositories
2. If successful, your token is working correctly
3. If you get an error, check:
   - Token is correct (no extra spaces)
   - Token has required scopes
   - Token hasn't expired
   - You have internet connection

## Common Authentication Issues

### "Failed to authenticate" Error

**Possible causes:**
- Invalid or expired token
- Token lacks required scopes
- Network connectivity issues

**Solutions:**
- Verify token is correct
- Check token expiration date
- Ensure token has `repo`, `workflow`, and `delete_repo` scopes
- Test your internet connection
- Regenerate the token if necessary

### "Insufficient permissions" Error

**Possible causes:**
- Token lacks specific scope for the operation
- Repository access restrictions
- Organization policies

**Solutions:**
- Add additional scopes to your token
- Ensure you have access to the repository
- Check organization permissions
- Contact repository owner if needed

### Two-Factor Authentication

If you have 2FA enabled on GitHub:
- Personal Access Tokens bypass 2FA
- No additional configuration needed
- Tokens work the same way with or without 2FA

## Using Environment Variables (Advanced)

For enhanced security, you can use environment variables instead of storing the token in config:

1. Set environment variable:
```bash
export GITHUB_TOKEN="your-token-here"
```

2. Modify the application to read from environment (requires code changes)

This is an advanced configuration and not enabled by default.

## Next Steps

After successful authentication, proceed to [Repository Management](REPOSITORY_MANAGEMENT.md) to start using GitHub Commander.
