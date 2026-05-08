# Contributing to GitHub Commander

Thank you for your interest in contributing to GitHub Commander! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Basic knowledge of Python and Qt/PySide6

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/github-commander.git
   cd github-commander
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # if available
   ```

5. Run the application:
   ```bash
   python main.py
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/add-new-feature`
- `bugfix/fix-specific-issue`
- `docs/update-documentation`
- `refactor/improve-code-structure`

### Making Changes

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Write tests for new functionality
4. Update documentation as needed
5. Commit your changes with descriptive messages

### Commit Messages

Follow conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example:
```
feat: add support for custom keyboard shortcuts

- Add keyboard shortcut configuration in settings
- Implement shortcut handling in main window
- Add documentation for default shortcuts
```

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Maximum line length: 100 characters

### Code Organization

- Separate concerns into modules
- Use type hints where appropriate
- Keep imports organized and grouped
- Remove unused imports

### Example Code Structure

```python
"""
Module description.
"""

from typing import Optional, List


class ExampleClass:
    """Class description."""

    def __init__(self, param: str):
        """Initialize the class."""
        self.param = param

    def method_name(self) -> bool:
        """Method description."""
        return True
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_module.py

# Run with coverage
pytest --cov=github_commander
```

### Writing Tests

- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases and error conditions

### Test Structure

```python
def test_feature_works():
    """Test that the feature works as expected."""
    # Arrange
    input_data = "test"
    
    # Act
    result = process_data(input_data)
    
    # Assert
    assert result == "expected"
```

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Document parameters and return values
- Include usage examples in docstrings

### User Documentation

- Update user guides for new features
- Add screenshots for UI changes
- Update README if needed
- Keep documentation in sync with code

### Documentation Location

- User guides: `/docs/` directory
- API documentation: In-code docstrings
- README: Project overview and quick start

## Submitting Changes

### Pull Request Process

1. Ensure your code passes all tests
2. Update documentation
3. Clean up commit history (squash related commits)
4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a pull request on GitHub
6. Fill out the pull request template
7. Wait for code review

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description explains the change

### Review Process

- Maintainers will review your PR
- Address feedback in a timely manner
- Be open to suggestions
- Keep discussion constructive

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Check if the issue is fixed in latest version
3. Try to reproduce the bug
4. Gather relevant information

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.11]
- GitHub Commander Version: [e.g., 1.0.0]

**Additional Context**
Add any other context about the problem.
```

## Feature Requests

### Proposing a Feature

1. Check existing feature requests
2. Open an issue describing the feature
3. Explain the use case
4. Provide implementation ideas if possible
5. Discuss with maintainers before implementing

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the Solution**
A clear description of what you want to happen.

**Describe Alternatives**
A clear description of any alternative solutions or features.

**Additional Context**
Add any other context or screenshots.
```

## Getting Help

- Ask questions in GitHub Discussions
- Check existing documentation
- Review similar issues
- Contact maintainers for complex questions

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to GitHub Commander!
