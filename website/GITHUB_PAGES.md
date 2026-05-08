# GitHub Pages Guide

This guide covers how to deploy and manage GitHub Pages sites using GitHub Commander.

## Overview

GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files from a repository and publishes them as a website.

GitHub Commander supports:
- Enabling/disabling Pages
- Deploying with GitHub Actions
- Manual deployment
- Framework-specific workflows

## Pages Panel Interface

The Pages Panel includes:

- **Pages Status** - Shows if Pages is enabled and the URL
- **Deployment Settings** - Configure branch, directory, and domain
- **Build Settings** - Framework and GitHub Actions configuration
- **Actions** - Enable, disable, and deploy buttons
- **Workflow Editor** - View and edit GitHub Actions workflow
- **Deployment Logs** - Track deployment progress

## Enabling GitHub Pages

### Basic Enablement

1. Select a repository
2. Go to the Pages Panel
3. Configure deployment settings:
   - **Source Branch** - Branch to deploy from (default: main)
   - **Source Directory** - Folder to deploy (default: /)
   - **Custom Domain** - Optional custom domain
   - **Enforce HTTPS** - Enable HTTPS for custom domains
4. Click "Enable Pages"
5. Pages will be enabled for the repository

### Source Branch Options

Common choices:
- **main** - Main production branch
- **master** - Legacy default branch
- **gh-pages** - Dedicated Pages branch

### Source Directory Options

- **/** - Root of repository
- **/docs** - Documentation folder
- **/dist** - Build output folder
- **/build** - Alternative build folder

### Custom Domain

1. Enter your domain in "Custom Domain" field
2. Configure DNS records on your domain provider:
   - Add A record pointing to GitHub's IP
   - Or add CNAME record to `[username].github.io`
3. Wait for DNS propagation
4. Enable "Enforce HTTPS" once DNS is verified

## Deploying with GitHub Actions

### What is GitHub Actions?

GitHub Actions is GitHub's automation platform. For Pages, it can:
- Build your site automatically
- Run tests before deployment
- Deploy on every push
- Support complex build processes

### Deploying with Actions

1. Select a repository
2. Go to the Pages Panel
3. In Build Settings:
   - Check "Use GitHub Actions for building"
   - Select your framework from the dropdown
4. Click "Generate Workflow" to preview the workflow
5. Click "Deploy"
6. Select the folder containing your built site files
7. The workflow file will be created at `.github/workflows/deploy-pages.yml`
8. Files will be uploaded to the repository
9. Push to trigger the deployment

### Framework-Specific Workflows

#### Static Sites (HTML/CSS/JS)

- No build step required
- Direct upload of files
- Simplest option for basic sites

#### React / Vue / Angular / Next.js

Workflow includes:
1. `npm ci` - Install dependencies
2. `npm run build` - Build the application
3. Upload `dist/` or `build/` folder

**Requirements:**
- `package.json` with build scripts
- Dependencies in `package-lock.json`

#### Hugo

Workflow includes:
1. Setup Hugo extended
2. `hugo --minify` - Build site
3. Upload `public/` folder

**Requirements:**
- Hugo content in `content/` folder
- Configuration in `config.toml`

#### Jekyll

Workflow includes:
1. Setup Ruby
2. `bundle install` - Install dependencies
3. `bundle exec jekyll build` - Build site
4. Upload `_site/` folder

**Requirements:**
- Jekyll configuration files
- Gemfile with dependencies

#### Custom Framework

- Upload specified directory
- No automatic build
- Suitable for pre-built sites

### Workflow File Location

The workflow is created at:
```
.github/workflows/deploy-pages.yml
```

You can edit this file manually or regenerate it from the panel.

## Manual Deployment

### When to Use Manual Deployment

- Simple static sites without build steps
- Pre-built sites
- Testing without Actions
- Quick deployments

### Manual Deployment Process

1. Select a repository
2. Go to the Pages Panel
3. Uncheck "Use GitHub Actions for building"
4. Configure source branch and directory
5. Click "Deploy"
6. Select the folder containing your site files
7. Files will be uploaded directly to the repository
8. Changes are committed to the configured branch

### Manual vs Actions

| Feature | Manual | Actions |
|---------|--------|---------|
| Build step | No | Yes |
| Automatic deployment | No | Yes (on push) |
| Testing | No | Yes |
| Framework support | Limited | Extensive |
| Complexity | Low | Medium |

## Deployment Settings

### Source Branch

The branch that triggers deployment:
- **main** - Most common for production
- **master** - Legacy default
- **gh-pages** - Dedicated Pages branch
- Custom branches supported

### Source Directory

The folder containing your site:
- **/** - Entire repository
- **/docs** - Documentation
- **/dist** - Build output
- **/build** - Alternative build output
- Custom paths supported

### Custom Domain

Setting up a custom domain:

1. Purchase a domain
2. Configure DNS:
   - **A Record**: Points to `185.199.108.153` (and other IPs)
   - **CNAME**: Points to `[username].github.io`
3. Enter domain in Pages settings
4. Wait for DNS propagation (up to 48 hours)
5. Enable HTTPS once verified

### HTTPS Enforcement

- Automatically provisions SSL certificate
- Redirects HTTP to HTTPS
- Recommended for all sites
- Requires DNS to be configured first

## Deployment Logs

### Viewing Logs

1. Go to the Pages Panel
2. View "Deployment Logs" section
3. All actions are logged with timestamps

### Log Entries Include

- Deployment start
- Workflow generation
- File upload progress
- Success/failure status
- Error messages if applicable

### GitHub Actions Logs

For detailed build logs:
1. Go to repository on GitHub.com
2. Click "Actions" tab
3. Select the workflow run
4. View detailed logs for each step

## Troubleshooting

### "Failed to enable Pages"

**Solutions:**
- Verify repository has Pages enabled in settings
- Check authentication
- Ensure branch exists
- Verify source directory path

### "Failed to deploy to Pages"

**Solutions:**
- Ensure Pages is enabled
- Verify workflow file syntax
- Check that source branch exists
- Verify source directory path
- Check GitHub Actions logs for errors

### Build Failures

**Common causes:**
- Missing dependencies
- Incorrect build commands
- Syntax errors in code
- Missing configuration files

**Solutions:**
- Check GitHub Actions logs
- Verify `package.json` or equivalent
- Test build locally first
- Review framework documentation

### DNS Issues

**Symptoms:**
- Custom domain not resolving
- HTTPS not working

**Solutions:**
- Wait for DNS propagation (up to 48 hours)
- Verify DNS records are correct
- Check domain registrar settings
- Use dig/nslookup to verify

### 404 Errors

**Solutions:**
- Verify source directory path
- Check file paths in repository
- Ensure index.html exists
- Verify branch is correct

## Best Practices

### Deployment Workflow

1. Test locally before deploying
2. Use feature branches for changes
3. Review workflow before committing
4. Monitor deployment logs
5. Test deployed site

### Performance

- Minimize file sizes
- Optimize images
- Use CDN for assets
- Enable caching
- Minify CSS/JS

### Security

- Keep dependencies updated
- Use HTTPS
- Don't commit sensitive data
- Review third-party code
- Use environment variables for secrets

## Next Steps

After deploying Pages, explore:
- [Wiki Management](WIKI_MANAGEMENT.md) - Add documentation
- [File Operations](FILE_OPERATIONS.md) - Update site content
