"""
Main Window - FTP-like dual-pane interface for GitHub Commander
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QMenuBar, QToolBar, QStatusBar,
                             QTabWidget, QDockWidget, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon
from config import Config
from github_client import GitHubClient
from git_operations import GitOperations
from .auth_dialog import AuthDialog
from .local_file_browser import LocalFileBrowser
from .github_file_browser import GitHubFileBrowser
from .pages_panel import PagesPanel
from .wiki_panel import WikiPanel
from .packages_panel import PackagesPanel
from .git_panel import GitPanel
from .releases_panel import ReleasesPanel
from .settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    """Main application window with FTP-like interface"""
    
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.github_client = GitHubClient(self.config)
        self.git_ops = GitOperations(self.config)
        self.current_repo = None
        
        self.init_ui()
        self.check_authentication()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("GitHub Commander")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create main splitter for dual-pane interface
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Local file browser (left pane)
        self.local_browser = LocalFileBrowser(self.config, self.git_ops)
        self.main_splitter.addWidget(self.local_browser)
        
        # GitHub file browser (right pane)
        self.github_browser = GitHubFileBrowser(self.github_client, self.config)
        self.main_splitter.addWidget(self.github_browser)
        
        # Set splitter proportions
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(self.main_splitter)
        
        # Create tab widget for additional panels
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.South)
        main_layout.addWidget(self.tab_widget)
        
        # Add panels
        self.git_panel = GitPanel(self.git_ops, self.github_client, self.config)
        self.tab_widget.addTab(self.git_panel, "Git Operations")
        
        self.pages_panel = PagesPanel(self.github_client, self.config)
        self.tab_widget.addTab(self.pages_panel, "GitHub Pages")
        
        self.wiki_panel = WikiPanel(self.github_client, self.config)
        self.tab_widget.addTab(self.wiki_panel, "Wiki")
        
        self.packages_panel = PackagesPanel(self.github_client, self.config)
        self.tab_widget.addTab(self.packages_panel, "Packages")
        
        self.releases_panel = ReleasesPanel(self.github_client, self.config)
        self.tab_widget.addTab(self.releases_panel, "Releases")
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Connect signals
        self.github_browser.repository_changed.connect(self.on_repository_changed)
        self.local_browser.file_selected.connect(self.on_local_file_selected)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        auth_action = QAction("Authenticate", self)
        auth_action.triggered.connect(self.authenticate)
        file_menu.addAction(auth_action)
        
        file_menu.addSeparator()
        
        clone_action = QAction("Clone Repository", self)
        clone_action.triggered.connect(self.clone_repository)
        file_menu.addAction(clone_action)
        
        create_repo_action = QAction("Create Repository", self)
        create_repo_action.triggered.connect(self.create_repository)
        file_menu.addAction(create_repo_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Transfer menu
        transfer_menu = menubar.addMenu("Transfer")
        
        upload_action = QAction("Upload Selected", self)
        upload_action.setShortcut("Ctrl+U")
        upload_action.triggered.connect(self.upload_selected)
        transfer_menu.addAction(upload_action)
        
        download_action = QAction("Download Selected", self)
        download_action.setShortcut("Ctrl+D")
        download_action.triggered.connect(self.download_selected)
        transfer_menu.addAction(download_action)
        
        upload_folder_action = QAction("Upload Folder", self)
        upload_folder_action.triggered.connect(self.upload_folder)
        transfer_menu.addAction(upload_folder_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Authentication
        auth_action = QAction("Authenticate", self)
        auth_action.triggered.connect(self.authenticate)
        toolbar.addAction(auth_action)
        
        toolbar.addSeparator()
        
        # File operations
        upload_action = QAction("Upload", self)
        upload_action.triggered.connect(self.upload_selected)
        toolbar.addAction(upload_action)
        
        download_action = QAction("Download", self)
        download_action.triggered.connect(self.download_selected)
        toolbar.addAction(download_action)
        
        toolbar.addSeparator()
        
        # Refresh
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # Settings
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)
    
    def check_authentication(self):
        """Check if user is authenticated"""
        token = self.config.get('github_token')
        if token:
            if self.github_client.authenticate(token):
                self.status_bar.showMessage("Authenticated with GitHub")
                self.github_browser.load_repositories()
            else:
                self.status_bar.showMessage("Authentication failed. Please re-authenticate.")
        else:
            self.status_bar.showMessage("Not authenticated. Please authenticate to use GitHub features.")
    
    def authenticate(self):
        """Open authentication dialog"""
        dialog = AuthDialog(self.config, self)
        if dialog.exec():
            token = dialog.get_token()
            if self.github_client.authenticate(token):
                self.status_bar.showMessage("Authenticated with GitHub")
                self.github_browser.load_repositories()
            else:
                QMessageBox.warning(self, "Authentication Failed", 
                                  "Invalid GitHub token. Please try again.")
    
    def clone_repository(self):
        """Clone a repository"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Clone Destination")
        
        if dialog.exec():
            dest_dir = dialog.selectedFiles()[0]
            # TODO: Show repository selection dialog
            self.status_bar.showMessage(f"Clone destination: {dest_dir}")
    
    def create_repository(self):
        """Create a new repository"""
        # TODO: Implement repository creation dialog
        self.status_bar.showMessage("Repository creation feature coming soon")
    
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self.config, self)
        if dialog.exec():
            self.status_bar.showMessage("Settings saved")
    
    def upload_selected(self):
        """Upload selected files from local to GitHub"""
        if not self.github_client.authenticated:
            QMessageBox.warning(self, "Not Authenticated", 
                              "Please authenticate with GitHub first.")
            return
        
        if not self.current_repo:
            QMessageBox.warning(self, "No Repository Selected", 
                              "Please select a GitHub repository first.")
            return
        
        selected_files = self.local_browser.get_selected_files()
        if not selected_files:
            QMessageBox.information(self, "No Selection", 
                                   "Please select files to upload.")
            return
        
        # TODO: Implement upload logic
        self.status_bar.showMessage(f"Uploading {len(selected_files)} file(s)...")
    
    def download_selected(self):
        """Download selected files from GitHub to local"""
        if not self.github_client.authenticated:
            QMessageBox.warning(self, "Not Authenticated", 
                              "Please authenticate with GitHub first.")
            return
        
        selected_files = self.github_browser.get_selected_files()
        if not selected_files:
            QMessageBox.information(self, "No Selection", 
                                   "Please select files to download.")
            return
        
        # TODO: Implement download logic
        self.status_bar.showMessage(f"Downloading {len(selected_files)} file(s)...")
    
    def upload_folder(self):
        """Upload entire folder"""
        if not self.github_client.authenticated:
            QMessageBox.warning(self, "Not Authenticated", 
                              "Please authenticate with GitHub first.")
            return
        
        folder_path = self.local_browser.get_current_path()
        # TODO: Implement folder upload logic
        self.status_bar.showMessage(f"Uploading folder: {folder_path}")
    
    def refresh(self):
        """Refresh all views"""
        self.local_browser.refresh()
        self.github_browser.refresh()
        self.status_bar.showMessage("Refreshed")
    
    def on_repository_changed(self, repo):
        """Handle repository change"""
        self.current_repo = repo
        self.status_bar.showMessage(f"Repository: {repo.full_name}")
        
        # Update panels
        self.git_panel.set_repository(repo)
        self.pages_panel.set_repository(repo)
        self.wiki_panel.set_repository(repo)
        self.packages_panel.set_repository(repo)
        self.releases_panel.set_repository(repo)
    
    def on_local_file_selected(self, file_path):
        """Handle local file selection"""
        self.status_bar.showMessage(f"Selected: {file_path}")
    
    def about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About GitHub Commander",
                         "GitHub Commander v1.0\n\n"
                         "A comprehensive GitHub desktop application for Linux\n"
                         "with FTP-like interface and full deployment capabilities.")
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.config.save()
        event.accept()
