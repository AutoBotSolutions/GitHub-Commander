"""
Configuration and settings management for GitHub Commander
"""

import json
import os
from pathlib import Path

class Config:
    """Configuration manager for the application"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.github-commander'
        self.config_file = self.config_dir / 'config.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        default_config = {
            'github_token': '',
            'default_branch': 'main',
            'clone_directory': str(Path.home() / 'github-projects'),
            'auto_commit_message': 'Update via GitHub Commander',
            'git_config': {
                'user.name': '',
                'user.email': ''
            },
            'ui': {
                'theme': 'dark',
                'font_size': 10,
                'show_hidden_files': False
            },
            'pages': {
                'source_branch': 'main',
                'custom_domain': ''
            },
            'wiki': {
                'default_home': 'Home'
            },
            'packages': {
                'npm_registry': 'https://registry.npmjs.org',
                'pypi_repository': 'https://pypi.org/simple'
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass
        
        return default_config
    
    def save(self):
        """Save configuration to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, key, default=None):
        """Get a configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default
    
    def set(self, key, value):
        """Set a configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()
