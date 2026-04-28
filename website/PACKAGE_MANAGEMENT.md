# Package Management Guide

This guide covers how to upload packages to various registries using GitHub Commander.

## Overview

GitHub Commander supports uploading packages to:
- npm (JavaScript/Node.js)
- PyPI (Python)
- Cargo (Rust)
- And other package registries

## Packages Panel Interface

The Packages Panel includes:

- **Package Type Selection** - Choose the registry (npm, pip, cargo)
- **Folder Selection** - Browse to package folder
- **Registry URL** - Configure registry endpoint
- **Upload Button** - Initiate package upload
- **Status Display** - Show upload progress and results

## Uploading npm Packages

### Prerequisites

Before uploading to npm:
- Have an npm account
- Be logged in to npm locally or have authentication token
- Package must have valid `package.json`
- Package name must be unique (or you must own it)

### Uploading to npm

1. Select a repository
2. Go to the Packages Panel
3. Select "npm" as the package type
4. Click "Browse..." to select the package folder
5. Enter the npm registry URL (default: https://registry.npmjs.org)
6. Click "Upload Package"
7. The package will be published to npm

### Package Requirements

Valid npm packages must have:
- `package.json` with:
  - `name` - Unique package name
  - `version` - Semantic version
  - `description` - Package description
  - `main` - Entry point file
  - `keywords` - Search terms (optional)
  - `author` - Author information (optional)
  - `license` - License information (optional)

### Authentication

npm authentication requires:
- Local npm login: `npm login`
- Or authentication token in `.npmrc`
- Token must have publish permissions

### Private Registries

To use a private npm registry:
1. Enter custom registry URL
2. Configure authentication for that registry
3. Ensure you have publish permissions

## Uploading Python Packages

### Prerequisites

Before uploading to PyPI:
- Have a PyPI account
- Enable 2FA on PyPI (required)
- Generate API token for uploads
- Package must have valid structure

### Uploading to PyPI

1. Select a repository
2. Go to the Packages Panel
3. Select "pip" as the package type
4. Click "Browse..." to select the package folder
5. Enter the PyPI repository URL (default: https://pypi.org/simple)
6. Click "Upload Package"
7. The package will be published to PyPI

### Package Requirements

Valid Python packages must have:
- `setup.py` or `pyproject.toml`
- `README.md` or `README.rst`
- `LICENSE` file
- Proper package structure:
  ```
  package-name/
  ├── setup.py
  ├── README.md
  ├── LICENSE
  └── package_name/
      ├── __init__.py
      └── module.py
  ```

### Authentication

PyPI authentication requires:
- API token from PyPI account settings
- Token stored in `~/.pypirc` or environment variable
- Or username/password (deprecated, use token instead)

### Test PyPI

To test uploads before production:
1. Use Test PyPI URL: https://test.pypi.org/simple
2. Separate account for Test PyPI
3. Verify package works before publishing to PyPI

## Uploading Cargo Packages

### Prerequisites

Before uploading to crates.io:
- Have a crates.io account
- Generate API token
- Package must have valid `Cargo.toml`

### Uploading to crates.io

1. Select a repository
2. Go to the Packages Panel
3. Select "cargo" as the package type
4. Click "Browse..." to select the package folder
5. Click "Upload Package"
6. The package will be published to crates.io

### Package Requirements

Valid Rust packages must have:
- `Cargo.toml` with:
  - `name` - Unique package name
  - `version` - Semantic version
  - `authors` - Author list
  - `description` - Package description
  - `license` - License information
  - `repository` - Repository URL (optional)
- `src/` directory with `main.rs` or `lib.rs`

### Authentication

Cargo authentication requires:
- API token from crates.io
- Token stored in `~/.cargo/credentials`
- Login with `cargo login`

## Registry Configuration

### Default Registries

- **npm**: https://registry.npmjs.org
- **PyPI**: https://pypi.org/simple
- **Test PyPI**: https://test.pypi.org/simple
- **crates.io**: https://crates.io

### Custom Registries

To use a custom registry:
1. Select the package type
2. Enter custom registry URL
3. Configure authentication for that registry
4. Ensure you have publish permissions

### Private Registries

For private registries:
1. Obtain registry URL from your organization
2. Configure authentication credentials
3. Set registry URL in the panel
4. Upload as normal

## Package Versioning

### Semantic Versioning

Follow semantic versioning (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- Increment MAJOR for incompatible changes
- Increment MINOR for new features (backwards compatible)
- Increment PATCH for bug fixes (backwards compatible)

### Pre-release Versions

Use pre-release identifiers:
- `1.0.0-alpha`
- `1.0.0-beta.1`
- `1.0.0-rc.1`

### Version Conflicts

If package name exists:
- You must own the package
- Or use a different name
- Or use scoped packages (npm): `@username/package-name`

## Troubleshooting

### "Failed to upload package"

**Common causes:**
- Invalid authentication
- Package name already exists
- Invalid package structure
- Network issues

**Solutions:**
- Verify authentication credentials
- Check package name availability
- Validate package structure
- Ensure internet connection

### "Package name already exists"

**Solutions:**
- Use a different package name
- Or if you own it, update version
- For npm, use scoped packages

### "Invalid package structure"

**Solutions:**
- Verify required files exist
- Check configuration file syntax
- Ensure proper directory structure
- Validate with registry tools locally

### Authentication Errors

**Solutions:**
- Verify API token is valid
- Check token permissions
- Ensure token is for correct registry
- Regenerate token if necessary

## Best Practices

### Before Uploading

1. Test package locally
2. Run all tests
3. Update documentation
4. Verify version number
5. Check CHANGELOG

### Package Quality

- Write comprehensive documentation
- Include examples
- Add tests
- Use semantic versioning
- Keep dependencies updated
- Respond to issues and PRs

### Security

- Don't commit secrets
- Use environment variables
- Keep dependencies secure
- Review third-party code
- Use vulnerability scanners

## Next Steps

After managing packages, explore:
- [Release Management](RELEASE_MANAGEMENT.md) - Create GitHub releases
- [Git Operations](GIT_OPERATIONS.md) - Version control your packages
