"""
Releases Panel - Create and manage GitHub releases
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QCheckBox,
                             QGroupBox, QFileDialog, QMessageBox, QComboBox)
from PySide6.QtCore import Qt
from github.Repository import Repository
from github_client import GitHubClient
from config import Config

class ReleasesPanel(QWidget):
    """Panel for release management"""
    
    def __init__(self, github_client: GitHubClient, config: Config, parent=None):
        super().__init__(parent)
        self.github_client = github_client
        self.config = config
        self.current_repo = None
        self.releases = []
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Repository info
        self.repo_label = QLabel("No repository selected")
        layout.addWidget(self.repo_label)
        
        # Releases list
        list_group = QGroupBox("Releases")
        list_layout = QVBoxLayout()
        
        self.releases_table = QTableWidget()
        self.releases_table.setColumnCount(4)
        self.releases_table.setHorizontalHeaderLabels([
            "Tag", "Name", "Published", "Actions"
        ])
        self.releases_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.releases_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.releases_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.releases_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        list_layout.addWidget(self.releases_table)
        
        refresh_button = QPushButton("Refresh Releases")
        refresh_button.clicked.connect(self.load_releases)
        refresh_button.setEnabled(False)
        list_layout.addWidget(refresh_button)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Create release
        create_group = QGroupBox("Create Release")
        create_layout = QVBoxLayout()
        
        # Tag
        tag_layout = QHBoxLayout()
        tag_layout.addWidget(QLabel("Tag:"))
        self.release_tag = QLineEdit()
        self.release_tag.setPlaceholderText("v1.0.0")
        tag_layout.addWidget(self.release_tag)
        create_layout.addLayout(tag_layout)
        
        # Release name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.release_name = QLineEdit()
        self.release_name.setPlaceholderText("Version 1.0.0")
        name_layout.addWidget(self.release_name)
        create_layout.addLayout(name_layout)
        
        # Branch
        branch_layout = QHBoxLayout()
        branch_layout.addWidget(QLabel("Target Branch:"))
        self.release_branch = QComboBox()
        self.release_branch.addItems(["main", "master", "develop"])
        branch_layout.addWidget(self.release_branch)
        create_layout.addLayout(branch_layout)
        
        # Release notes
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("Release Notes:"))
        self.release_notes = QTextEdit()
        self.release_notes.setPlaceholderText("Describe the changes in this release...")
        self.release_notes.setMaximumHeight(150)
        notes_layout.addWidget(self.release_notes)
        create_layout.addLayout(notes_layout)
        
        # Options
        options_layout = QHBoxLayout()
        
        self.draft_release = QCheckBox("Draft")
        options_layout.addWidget(self.draft_release)
        
        self.prerelease = QCheckBox("Pre-release")
        options_layout.addWidget(self.prerelease)
        
        self.generate_notes = QCheckBox("Generate Notes")
        self.generate_notes.setChecked(True)
        options_layout.addWidget(self.generate_notes)
        
        create_layout.addLayout(options_layout)
        
        # Create button
        self.create_release_button = QPushButton("Create Release")
        self.create_release_button.clicked.connect(self.create_release)
        self.create_release_button.setEnabled(False)
        create_layout.addWidget(self.create_release_button)
        
        create_group.setLayout(create_layout)
        layout.addWidget(create_group)
        
        # Upload assets
        assets_group = QGroupBox("Upload Assets")
        assets_layout = QVBoxLayout()
        
        asset_file_layout = QHBoxLayout()
        asset_file_layout.addWidget(QLabel("Asset File:"))
        self.asset_file = QLineEdit()
        asset_file_layout.addWidget(self.asset_file)
        
        browse_asset = QPushButton("Browse...")
        browse_asset.clicked.connect(self.browse_asset)
        asset_file_layout.addWidget(browse_asset)
        
        assets_layout.addLayout(asset_file_layout)
        
        # Select release for asset upload
        asset_release_layout = QHBoxLayout()
        asset_release_layout.addWidget(QLabel("Upload to Release:"))
        self.asset_release_combo = QComboBox()
        asset_release_layout.addWidget(self.asset_release_combo)
        assets_layout.addLayout(asset_release_layout)
        
        self.upload_asset_button = QPushButton("Upload Asset")
        self.upload_asset_button.clicked.connect(self.upload_asset)
        self.upload_asset_button.setEnabled(False)
        assets_layout.addWidget(self.upload_asset_button)
        
        assets_group.setLayout(assets_layout)
        layout.addWidget(assets_group)
        
        # Status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def set_repository(self, repo: Repository):
        """Set the current repository"""
        self.current_repo = repo
        self.repo_label.setText(f"Repository: {repo.full_name}")
        
        # Enable buttons
        self.findChild(QPushButton, "Refresh Releases").setEnabled(True)
        self.create_release_button.setEnabled(True)
        self.upload_asset_button.setEnabled(True)
        
        # Load releases
        self.load_releases()
    
    def load_releases(self):
        """Load releases from repository"""
        if not self.current_repo:
            return
        
        self.releases_table.setRowCount(0)
        self.status_label.setText("Loading releases...")
        
        try:
            releases = list(self.current_repo.get_releases())
            self.releases = releases
            
            for release in releases:
                row = self.releases_table.rowCount()
                self.releases_table.insertRow(row)
                
                # Tag
                self.releases_table.setItem(row, 0, QTableWidgetItem(release.tag_name))
                
                # Name
                self.releases_table.setItem(row, 1, QTableWidgetItem(release.title))
                
                # Published
                published = "Yes" if release.published_at else "Draft"
                self.releases_table.setItem(row, 2, QTableWidgetItem(published))
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(4, 0, 4, 0)
                
                view_button = QPushButton("View")
                view_button.clicked.connect(lambda checked, r=release: self.view_release(r))
                actions_layout.addWidget(view_button)
                
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda checked, r=release: self.delete_release(r))
                actions_layout.addWidget(delete_button)
                
                self.releases_table.setCellWidget(row, 3, actions_widget)
            
            # Update asset release combo
            self.asset_release_combo.clear()
            self.asset_release_combo.addItems([r.tag_name for r in releases])
            
            self.status_label.setText(f"Loaded {len(releases)} releases")
            
        except Exception as e:
            self.status_label.setText(f"Error loading releases: {str(e)}")
    
    def create_release(self):
        """Create a new release"""
        if not self.current_repo:
            return
        
        tag = self.release_tag.text().strip()
        name = self.release_name.text().strip()
        notes = self.release_notes.toPlainText()
        draft = self.draft_release.isChecked()
        prerelease = self.prerelease.isChecked()
        
        if not tag:
            QMessageBox.warning(self, "Missing Tag", "Please enter a tag.")
            return
        
        if not name:
            name = tag
        
        self.status_label.setText("Creating release...")
        
        try:
            release = self.github_client.create_release(
                self.current_repo, tag, name, notes, draft, prerelease
            )
            
            if release:
                QMessageBox.information(self, "Success", 
                                       f"Release {tag} created successfully!")
                self.load_releases()
                self.status_label.setText(f"Created release: {tag}")
            else:
                QMessageBox.warning(self, "Error", "Failed to create release.")
                self.status_label.setText("Failed to create release")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create release: {str(e)}")
            self.status_label.setText(f"Error: {str(e)}")
    
    def view_release(self, release):
        """View release details"""
        # Open in browser or show dialog
        QMessageBox.information(self, "Release Details",
                              f"Tag: {release.tag_name}\n"
                              f"Name: {release.title}\n"
                              f"Published: {release.published_at}\n\n"
                              f"Notes:\n{release.body}")
    
    def delete_release(self, release):
        """Delete a release"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete release {release.tag_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                release.delete()
                self.load_releases()
                self.status_label.setText(f"Deleted release: {release.tag_name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete release: {str(e)}")
    
    def browse_asset(self):
        """Browse for asset file"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setWindowTitle("Select Asset File")
        
        if dialog.exec():
            file = dialog.selectedFiles()[0]
            self.asset_file.setText(file)
    
    def upload_asset(self):
        """Upload asset to a release"""
        if not self.current_repo:
            return
        
        asset_path = self.asset_file.text()
        tag = self.asset_release_combo.currentText()
        
        if not asset_path:
            QMessageBox.warning(self, "No File", "Please select an asset file.")
            return
        
        if not tag:
            QMessageBox.warning(self, "No Release", "Please select a release.")
            return
        
        self.status_label.setText("Uploading asset...")
        
        try:
            # Get the release
            releases = list(self.current_repo.get_releases())
            release = next((r for r in releases if r.tag_name == tag), None)
            
            if not release:
                QMessageBox.warning(self, "Release Not Found", 
                                  f"Release {tag} not found.")
                return
            
            # Upload asset
            if self.github_client.upload_asset_to_release(release, asset_path):
                QMessageBox.information(self, "Success", 
                                       "Asset uploaded successfully!")
                self.status_label.setText("Asset uploaded")
            else:
                QMessageBox.warning(self, "Error", "Failed to upload asset.")
                self.status_label.setText("Failed to upload asset")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to upload asset: {str(e)}")
            self.status_label.setText(f"Error: {str(e)}")
