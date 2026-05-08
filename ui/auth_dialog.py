"""
Authentication Dialog - GitHub token authentication
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QCheckBox)
from PySide6.QtCore import Qt
from config import Config

class AuthDialog(QDialog):
    """Dialog for GitHub authentication"""
    
    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.token_input = QLineEdit()
        self.remember_token = QCheckBox("Remember token")
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("GitHub Authentication")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Instructions
        info_label = QLabel(
            "Enter your GitHub Personal Access Token (PAT).\n\n"
            "To create a token:\n"
            "1. Go to GitHub Settings → Developer settings → Personal access tokens\n"
            "2. Click 'Generate new token' (classic)\n"
            "3. Select required scopes: repo, workflow, read:org, admin:org\n"
            "4. Copy the generated token"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Token input
        token_label = QLabel("Personal Access Token:")
        layout.addWidget(token_label)
        
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setPlaceholderText("ghp_xxxxxxxxxxxx")
        layout.addWidget(self.token_input)
        
        # Remember token checkbox
        self.remember_token.setChecked(bool(self.config.get('github_token')))
        layout.addWidget(self.remember_token)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        authenticate_button = QPushButton("Authenticate")
        authenticate_button.setDefault(True)
        authenticate_button.clicked.connect(self.authenticate)
        button_layout.addWidget(authenticate_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def authenticate(self):
        """Authenticate with the provided token"""
        token = self.token_input.text().strip()
        
        if not token:
            QMessageBox.warning(self, "Empty Token", 
                              "Please enter a GitHub token.")
            return
        
        if not token.startswith("ghp_") and not token.startswith("github_pat_"):
            reply = QMessageBox.question(
                self, "Invalid Token Format",
                "The token doesn't appear to be a valid GitHub token format.\n"
                "Continue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        self.accept()
    
    def get_token(self):
        """Get the entered token"""
        return self.token_input.text().strip()
    
    def should_remember(self):
        """Check if token should be remembered"""
        return self.remember_token.isChecked()
