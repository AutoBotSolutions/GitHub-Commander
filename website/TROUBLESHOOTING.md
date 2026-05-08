# Troubleshooting Guide

This guide covers common issues and their solutions when using GitHub Commander.

## Authentication Issues

### "Failed to authenticate" Error

**Possible Causes:**
- Invalid or expired GitHub token
- Token lacks required scopes
- Network connectivity issues

**Solutions:**
1. Verify your GitHub token is valid
2. Ensure the token has required scopes (repo, workflow, delete_repo)
3. Check your internet connection
4. Regenerate the token if necessary

### "Insufficient permissions" Error

**Solutions:**
1. Add additional scopes to your token
2. Ensure you have write access to the repository
3. Check organization permissions

## Clone Issues

### "Clone failed" Error

**Solutions:**
1. Verify the repository URL is correct
2. Check your internet connection
3. Ensure you have access to the repository
4. Check destination folder permissions

## Upload Issues

### "Upload failed" Error

**Solutions:**
1. Verify your authentication
2. Ensure file size is within 100 MB limit
3. Check write access to repository
4. Verify file path is correct

### "File too large" Error

**Solutions:**
1. Use Git LFS for large files
2. Split large files into smaller chunks
3. Compress files if possible

## Wiki Upload Issues

### "Failed to upload wiki page"

**Solutions:**
1. Enable wiki in repository settings
2. Verify file is valid Markdown
3. Check authentication
4. Ensure internet connection

## Pages Deployment Issues

### "Failed to deploy to Pages"

**Solutions:**
1. Ensure Pages is enabled for the repository
2. Verify workflow file syntax
3. Check that source branch exists
4. Verify source directory path

### Build Failures

**Solutions:**
1. Check GitHub Actions logs for detailed errors
2. Verify package.json or configuration
3. Test build locally first
4. Review framework documentation

## Package Upload Issues

### "Failed to upload package"

**Solutions:**
1. Verify registry credentials
2. Check package name availability
3. Validate package structure
4. Ensure internet connection

### "Package name already exists"

**Solutions:**
1. Use a different package name
2. If you own it, update version number
3. For npm, use scoped packages

## Git Operation Issues

### "Failed to commit"

**Solutions:**
1. Verify you have changes to commit
2. Resolve merge conflicts first
3. Check Git configuration

### "Failed to push"

**Solutions:**
1. Add remote if missing
2. Check authentication
3. Pull first, then push
4. Check internet connection

### Merge Conflicts

**Solutions:**
1. Open conflicting files
2. Look for conflict markers (<<<<<<<)
3. Choose which version to keep
4. Remove conflict markers
5. Mark as resolved
6. Commit the merge

## General Tips

1. **Check the Console:** Many errors print detailed messages to the console
2. **Verify Permissions:** Ensure you have necessary GitHub permissions
3. **Update Token:** If operations fail, try regenerating your GitHub token
4. **Check Network:** Ensure stable internet connection
5. **Clear Cache:** If experiencing issues, try clearing application cache
