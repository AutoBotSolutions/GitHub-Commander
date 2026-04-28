"""
GitHub File Browser - Right pane for GitHub repositories
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                             QTreeWidgetItem, QHeaderView, QPushButton, 
                             QLineEdit, QLabel, QComboBox, QMenu, QMessageBox,
                             QStyle)
from PySide6.QtCore import Qt, Signal
from github.Repository import Repository
from github_client import GitHubClient
from config import Config

class GitHubFileBrowser(QWidget):
    """File browser for GitHub repositories"""
    
    repository_changed = Signal(object)
    
    def __init__(self, github_client: GitHubClient, config: Config, parent=None):
        super().__init__(parent)
        self.github_client = github_client
        self.config = config
        self.current_repo = None
        self.current_path = ""
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Repository selector
        repo_layout = QHBoxLayout()
        
        repo_label = QLabel("Repository:")
        repo_layout.addWidget(repo_label)
        
        self.repo_combo = QComboBox()
        self.repo_combo.setMinimumWidth(300)
        self.repo_combo.currentIndexChanged.connect(self.on_repo_changed)
        repo_layout.addWidget(self.repo_combo)
        
        refresh_repos_button = QPushButton("Refresh")
        refresh_repos_button.clicked.connect(self.load_repositories)
        repo_layout.addWidget(refresh_repos_button)
        
        layout.addLayout(repo_layout)
        
        # Branch selector
        branch_layout = QHBoxLayout()
        
        branch_label = QLabel("Branch:")
        branch_layout.addWidget(branch_label)
        
        self.branch_combo = QComboBox()
        self.branch_combo.setMinimumWidth(200)
        self.branch_combo.currentIndexChanged.connect(self.on_branch_changed)
        branch_layout.addWidget(self.branch_combo)
        
        layout.addLayout(branch_layout)
        
        # File tree
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Name", "Size", "Type"])
        self.file_tree.setSortingEnabled(True)
        self.file_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.file_tree.setSelectionMode(
            QTreeWidget.SelectionMode.ExtendedSelection
        )
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.file_tree.itemClicked.connect(self.on_file_clicked)
        
        header = self.file_tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.file_tree)
        
        # Path display
        self.path_label = QLabel("Path: /")
        layout.addWidget(self.path_label)
        
        # Status bar
        self.status_label = QLabel("No repository selected")
        layout.addWidget(self.status_label)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        self.upload_button = QPushButton("Upload to Here")
        self.upload_button.setEnabled(False)
        actions_layout.addWidget(self.upload_button)
        
        self.download_button = QPushButton("Download Selected")
        self.download_button.setEnabled(False)
        actions_layout.addWidget(self.download_button)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)
        actions_layout.addWidget(refresh_button)
        
        layout.addLayout(actions_layout)
        
        self.setLayout(layout)
    
    def load_repositories(self):
        """Load repositories from GitHub"""
        if not self.github_client.authenticated:
            self.status_label.setText("Not authenticated")
            return
        
        self.repo_combo.clear()
        self.repo_combo.addItem("Select a repository...")
        
        repos = self.github_client.get_repositories()
        for repo in repos:
            self.repo_combo.addItem(repo.full_name, repo)
        
        self.status_label.setText(f"Loaded {len(repos)} repositories")
    
    def on_repo_changed(self, index):
        """Handle repository selection change"""
        if index <= 0:
            self.current_repo = None
            self.file_tree.clear()
            self.branch_combo.clear()
            self.upload_button.setEnabled(False)
            self.status_label.setText("No repository selected")
            return
        
        self.current_repo = self.repo_combo.currentData()
        self.repository_changed.emit(self.current_repo)
        
        # Load branches
        self.load_branches()
        
        # Load root contents
        self.current_path = ""
        self.load_contents()
        
        self.upload_button.setEnabled(True)
        self.status_label.setText(f"Repository: {self.current_repo.full_name}")
    
    def load_branches(self):
        """Load branches for current repository"""
        if not self.current_repo:
            return
        
        self.branch_combo.clear()
        branches = self.github_client.get_branches(self.current_repo)
        for branch in branches:
            self.branch_combo.addItem(branch.name, branch.name)
    
    def on_branch_changed(self, index):
        """Handle branch selection change"""
        if self.current_repo:
            self.load_contents()
    
    def load_contents(self, path: str = ""):
        """Load contents of a path in the repository"""
        if not self.current_repo:
            return
        
        branch = self.branch_combo.currentData()
        if not branch:
            branch = self.config.get('default_branch', 'main')
        
        self.file_tree.clear()
        self.current_path = path
        self.path_label.setText(f"Path: /{path}")
        
        try:
            contents = self.github_client.get_repository_contents(
                self.current_repo, path
            )
            
            for item in contents:
                tree_item = QTreeWidgetItem()
                tree_item.setText(0, item.name)
                
                if item.type == "dir":
                    tree_item.setText(1, "")
                    tree_item.setText(2, "Directory")
                    # Store path for navigation
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, item.path)
                else:
                    size = str(item.size) if hasattr(item, 'size') else ""
                    tree_item.setText(1, size)
                    tree_item.setText(2, "File")
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, item.path)
                
                self.file_tree.addTopLevelItem(tree_item)
            
            self.status_label.setText(f"Loaded {len(contents)} items")
            
        except Exception as e:
            self.status_label.setText(f"Error loading contents: {str(e)}")
    
    def on_file_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle file/directory click"""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if item.text(2) == "Directory":
            # Navigate into directory
            self.load_contents(path)
        else:
            self.status_label.setText(f"Selected: {item.text(0)}")
    
    def show_context_menu(self, position):
        """Show context menu"""
        item = self.file_tree.itemAt(position)
        if not item:
            return
        
        menu = QMenu()
        
        if item.text(2) == "Directory":
            menu.addAction("Enter Directory", lambda: self.enter_directory(item))
            menu.addAction("Upload to This Directory", lambda: self.upload_to_directory(item))
        else:
            menu.addAction("Download File", lambda: self.download_file(item))
            menu.addAction("Delete File", lambda: self.delete_file(item))
        
        menu.exec(self.file_tree.viewport().mapToGlobal(position))
    
    def enter_directory(self, item: QTreeWidgetItem):
        """Enter a directory"""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        self.load_contents(path)
    
    def upload_to_directory(self, item: QTreeWidgetItem):
        """Upload files to this directory"""
        # Signal to main window to upload
        self.status_label.setText("Upload functionality - select files in local pane")
    
    def download_file(self, item: QTreeWidgetItem):
        """Download a file"""
        # Signal to main window to download
        self.status_label.setText("Download functionality")
    
    def delete_file(self, item: QTreeWidgetItem):
        """Delete a file"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {item.text(0)}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            path = item.data(0, Qt.ItemDataRole.UserRole)
            branch = self.branch_combo.currentData() or "main"
            message = f"Delete {item.text(0)}"
            
            if self.github_client.delete_file(
                self.current_repo, path, message, branch
            ):
                self.load_contents(self.current_path)
                self.status_label.setText(f"Deleted {item.text(0)}")
            else:
                self.status_label.setText("Failed to delete file")
    
    def refresh(self):
        """Refresh the current view"""
        self.load_contents(self.current_path)
        self.status_label.setText("Refreshed")
    
    def get_selected_files(self):
        """Get selected file paths"""
        selected = self.file_tree.selectedItems()
        return [item.data(0, Qt.ItemDataRole.UserRole) for item in selected]
