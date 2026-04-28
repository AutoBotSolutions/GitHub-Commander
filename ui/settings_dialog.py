"""
Settings Dialog - Configure application settings
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QCheckBox,
                             QTabWidget, QGroupBox, QSpinBox, QFileDialog,
                             QMessageBox)
from PySide6.QtCore import Qt
from config import Config

class SettingsDialog(QDialog):
    """Dialog for application settings"""
    
    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout()
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # General tab
        general_tab = self.create_general_tab()
        self.tab_widget.addTab(general_tab, "General")
        
        # Git tab
        git_tab = self.create_git_tab()
        self.tab_widget.addTab(git_tab, "Git")
        
        # GitHub tab
        github_tab = self.create_github_tab()
        self.tab_widget.addTab(github_tab, "GitHub")
        
        # Pages tab
        pages_tab = self.create_pages_tab()
        self.tab_widget.addTab(pages_tab, "Pages")
        
        # Packages tab
        packages_tab = self.create_packages_tab()
        self.tab_widget.addTab(packages_tab, "Packages")
        
        # UI tab
        ui_tab = self.create_ui_tab()
        self.tab_widget.addTab(ui_tab, "UI")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Save")
        save_button.setDefault(True)
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_general_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Clone directory
        clone_group = QGroupBox("Clone Directory")
        clone_layout = QVBoxLayout()
        
        clone_dir_layout = QHBoxLayout()
        clone_dir_layout.addWidget(QLabel("Default Clone Directory:"))
        self.clone_dir = QLineEdit()
        clone_dir_layout.addWidget(self.clone_dir)
        
        browse_clone = QPushButton("Browse...")
        browse_clone.clicked.connect(self.browse_clone_dir)
        clone_dir_layout.addWidget(browse_clone)
        
        clone_layout.addLayout(clone_dir_layout)
        clone_group.setLayout(clone_layout)
        layout.addWidget(clone_group)
        
        # Default branch
        branch_group = QGroupBox("Git")
        branch_layout = QVBoxLayout()
        
        branch_dir_layout = QHBoxLayout()
        branch_dir_layout.addWidget(QLabel("Default Branch:"))
        self.default_branch = QLineEdit()
        branch_dir_layout.addWidget(self.default_branch)
        branch_layout.addLayout(branch_dir_layout)
        
        self.auto_commit = QCheckBox("Auto-commit on upload")
        branch_layout.addWidget(self.auto_commit)
        
        branch_group.setLayout(branch_layout)
        layout.addWidget(branch_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_git_tab(self):
        """Create Git settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # User info
        user_group = QGroupBox("Git User Information")
        user_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("User Name:"))
        self.git_user_name = QLineEdit()
        name_layout.addWidget(self.git_user_name)
        user_layout.addLayout(name_layout)
        
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("User Email:"))
        self.git_user_email = QLineEdit()
        email_layout.addWidget(self.git_user_email)
        user_layout.addLayout(email_layout)
        
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)
        
        # Commit message
        commit_group = QGroupBox("Commit Messages")
        commit_layout = QVBoxLayout()
        
        commit_layout.addWidget(QLabel("Default Commit Message:"))
        self.commit_message = QLineEdit()
        commit_layout.addWidget(self.commit_message)
        
        commit_group.setLayout(commit_layout)
        layout.addWidget(commit_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_github_tab(self):
        """Create GitHub settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Token
        token_group = QGroupBox("Authentication")
        token_layout = QVBoxLayout()
        
        token_label = QLabel(
            "GitHub Personal Access Token. Leave empty to use stored token."
        )
        token_label.setWordWrap(True)
        token_layout.addWidget(token_label)
        
        token_input_layout = QHBoxLayout()
        token_input_layout.addWidget(QLabel("Token:"))
        self.github_token = QLineEdit()
        self.github_token.setEchoMode(QLineEdit.EchoMode.Password)
        token_input_layout.addWidget(self.github_token)
        token_layout.addLayout(token_input_layout)
        
        token_group.setLayout(token_layout)
        layout.addWidget(token_group)
        
        # API settings
        api_group = QGroupBox("API Settings")
        api_layout = QVBoxLayout()
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Request Timeout (seconds):"))
        self.api_timeout = QSpinBox()
        self.api_timeout.setMinimum(5)
        self.api_timeout.setMaximum(300)
        self.api_timeout.setValue(30)
        timeout_layout.addWidget(self.api_timeout)
        api_layout.addLayout(timeout_layout)
        
        self.retry_on_failure = QCheckBox("Retry on Failure")
        api_layout.addWidget(self.retry_on_failure)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_pages_tab(self):
        """Create GitHub Pages settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Default settings
        pages_group = QGroupBox("Default Pages Settings")
        pages_layout = QVBoxLayout()
        
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Default Source Branch:"))
        self.pages_source_branch = QLineEdit()
        source_layout.addWidget(self.pages_source_branch)
        pages_layout.addLayout(source_layout)
        
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Default Source Directory:"))
        self.pages_source_dir = QLineEdit()
        dir_layout.addWidget(self.pages_source_dir)
        pages_layout.addLayout(dir_layout)
        
        domain_layout = QHBoxLayout()
        domain_layout.addWidget(QLabel("Custom Domain:"))
        self.pages_custom_domain = QLineEdit()
        domain_layout.addWidget(self.pages_custom_domain)
        pages_layout.addLayout(domain_layout)
        
        pages_group.setLayout(pages_layout)
        layout.addWidget(pages_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_packages_tab(self):
        """Create Packages settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # NPM
        npm_group = QGroupBox("NPM")
        npm_layout = QVBoxLayout()
        
        npm_registry_layout = QHBoxLayout()
        npm_registry_layout.addWidget(QLabel("Registry:"))
        self.npm_registry = QLineEdit()
        npm_registry_layout.addWidget(self.npm_registry)
        npm_layout.addLayout(npm_registry_layout)
        
        npm_group.setLayout(npm_layout)
        layout.addWidget(npm_group)
        
        # PyPI
        pypi_group = QGroupBox("PyPI")
        pypi_layout = QVBoxLayout()
        
        pypi_repo_layout = QHBoxLayout()
        pypi_repo_layout.addWidget(QLabel("Repository:"))
        self.pypi_repository = QLineEdit()
        pypi_repo_layout.addWidget(self.pypi_repository)
        pypi_layout.addLayout(pypi_repo_layout)
        
        pypi_group.setLayout(pypi_layout)
        layout.addWidget(pypi_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_ui_tab(self):
        """Create UI settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Theme
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()
        
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light", "system"])
        theme_layout.addWidget(self.theme_combo)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_size = QSpinBox()
        self.font_size.setMinimum(8)
        self.font_size.setMaximum(24)
        self.font_size.setValue(10)
        font_layout.addWidget(self.font_size)
        theme_layout.addLayout(font_layout)
        
        self.show_hidden = QCheckBox("Show Hidden Files")
        theme_layout.addWidget(self.show_hidden)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def load_settings(self):
        """Load settings from config"""
        # General
        self.clone_dir.setText(self.config.get('clone_directory', ''))
        self.default_branch.setText(self.config.get('default_branch', 'main'))
        self.auto_commit.setChecked(self.config.get('auto_commit', False))
        
        # Git
        self.git_user_name.setText(self.config.get('git_config.user.name', ''))
        self.git_user_email.setText(self.config.get('git_config.user.email', ''))
        self.commit_message.setText(self.config.get('auto_commit_message', ''))
        
        # GitHub
        self.github_token.setText('')  # Don't load token for security
        
        # Pages
        self.pages_source_branch.setText(self.config.get('pages.source_branch', 'main'))
        self.pages_source_dir.setText(self.config.get('pages.source_dir', '/'))
        self.pages_custom_domain.setText(self.config.get('pages.custom_domain', ''))
        
        # Packages
        self.npm_registry.setText(self.config.get('packages.npm_registry', ''))
        self.pypi_repository.setText(self.config.get('packages.pypi_repository', ''))
        
        # UI
        self.theme_combo.setCurrentText(self.config.get('ui.theme', 'dark'))
        self.font_size.setValue(self.config.get('ui.font_size', 10))
        self.show_hidden.setChecked(self.config.get('ui.show_hidden_files', False))
    
    def save_settings(self):
        """Save settings to config"""
        # General
        self.config.set('clone_directory', self.clone_dir.text())
        self.config.set('default_branch', self.default_branch.text())
        self.config.set('auto_commit', self.auto_commit.isChecked())
        
        # Git
        self.config.set('git_config.user.name', self.git_user_name.text())
        self.config.set('git_config.user.email', self.git_user_email.text())
        self.config.set('auto_commit_message', self.commit_message.text())
        
        # GitHub
        if self.github_token.text():
            self.config.set('github_token', self.github_token.text())
        
        # Pages
        self.config.set('pages.source_branch', self.pages_source_branch.text())
        self.config.set('pages.source_dir', self.pages_source_dir.text())
        self.config.set('pages.custom_domain', self.pages_custom_domain.text())
        
        # Packages
        self.config.set('packages.npm_registry', self.npm_registry.text())
        self.config.set('packages.pypi_repository', self.pypi_repository.text())
        
        # UI
        self.config.set('ui.theme', self.theme_combo.currentText())
        self.config.set('ui.font_size', self.font_size.value())
        self.config.set('ui.show_hidden_files', self.show_hidden.isChecked())
        
        self.config.save()
        self.accept()
    
    def browse_clone_dir(self):
        """Browse for clone directory"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Clone Directory")
        
        if dialog.exec():
            directory = dialog.selectedFiles()[0]
            self.clone_dir.setText(directory)
