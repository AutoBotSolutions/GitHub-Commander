"""
Wiki Panel - Upload and manage repository wikis
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox,
                             QFileDialog, QTabWidget, QGroupBox)
from PySide6.QtCore import Qt
from github.Repository import Repository
from github_client import GitHubClient
from config import Config
from pathlib import Path

class WikiPanel(QWidget):
    """Panel for Wiki management"""
    
    def __init__(self, github_client: GitHubClient, config: Config, parent=None):
        super().__init__(parent)
        self.github_client = github_client
        self.config = config
        self.current_repo = None
        self.wiki_pages = []
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Repository info
        self.repo_label = QLabel("No repository selected")
        layout.addWidget(self.repo_label)
        
        # Tab widget for different wiki operations
        self.tab_widget = QTabWidget()
        
        # Pages tab
        pages_tab = QWidget()
        pages_layout = QVBoxLayout()
        
        # Pages table
        self.pages_table = QTableWidget()
        self.pages_table.setColumnCount(3)
        self.pages_table.setHorizontalHeaderLabels(["Page Name", "Last Updated", "Actions"])
        self.pages_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.pages_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.pages_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        pages_layout.addWidget(self.pages_table)
        
        # Page actions
        page_actions = QHBoxLayout()
        
        self.refresh_pages = QPushButton("Refresh Pages")
        self.refresh_pages.clicked.connect(self.load_wiki_pages)
        self.refresh_pages.setEnabled(False)
        page_actions.addWidget(self.refresh_pages)
        
        self.create_page = QPushButton("Create New Page")
        self.create_page.clicked.connect(self.create_new_page)
        self.create_page.setEnabled(False)
        page_actions.addWidget(self.create_page)
        
        pages_layout.addLayout(page_actions)
        
        pages_tab.setLayout(pages_layout)
        self.tab_widget.addTab(pages_tab, "Pages")
        
        # Editor tab
        editor_tab = QWidget()
        editor_layout = QVBoxLayout()
        
        # Page title
        title_layout = QHBoxLayout()
        title_label = QLabel("Page Title:")
        title_layout.addWidget(title_label)
        
        self.page_title = QLineEdit()
        self.page_title.setPlaceholderText("Enter page title...")
        title_layout.addWidget(self.page_title)
        
        editor_layout.addLayout(title_layout)
        
        # Page content
        content_label = QLabel("Page Content (Markdown):")
        editor_layout.addWidget(content_label)
        
        self.page_content = QTextEdit()
        self.page_content.setPlaceholderText("Write your wiki page in Markdown...")
        editor_layout.addWidget(self.page_content)
        
        # Editor actions
        editor_actions = QHBoxLayout()
        
        self.save_page = QPushButton("Save Page")
        self.save_page.clicked.connect(self.save_current_page)
        self.save_page.setEnabled(False)
        editor_actions.addWidget(self.save_page)
        
        self.preview_page = QPushButton("Preview")
        self.preview_page.clicked.connect(self.preview_current_page)
        self.preview_page.setEnabled(False)
        editor_actions.addWidget(self.preview_page)
        
        editor_layout.addLayout(editor_actions)
        
        editor_tab.setLayout(editor_layout)
        self.tab_widget.addTab(editor_tab, "Editor")
        
        # Upload tab
        upload_tab = QWidget()
        upload_layout = QVBoxLayout()
        
        upload_group = QGroupBox("Upload Wiki Pages")
        upload_group_layout = QVBoxLayout()
        
        # Folder selection
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Wiki Folder:")
        folder_layout.addWidget(folder_label)
        
        self.wiki_folder = QLineEdit()
        self.wiki_folder.setPlaceholderText("/path/to/wiki/files")
        folder_layout.addWidget(self.wiki_folder)
        
        browse_folder = QPushButton("Browse...")
        browse_folder.clicked.connect(self.browse_wiki_folder)
        folder_layout.addWidget(browse_folder)
        
        upload_group_layout.addLayout(folder_layout)
        
        # Upload options
        self.upload_subfolders = QPushButton("Upload All Pages")
        self.upload_subfolders.clicked.connect(self.upload_all_pages)
        self.upload_subfolders.setEnabled(False)
        upload_group_layout.addWidget(self.upload_subfolders)
        
        upload_group.setLayout(upload_group_layout)
        upload_layout.addWidget(upload_group)
        
        # Batch upload info
        info_label = QLabel(
            "Wiki pages should be Markdown files (.md or .markdown).\n"
            "The filename will be used as the page title."
        )
        info_label.setWordWrap(True)
        upload_layout.addWidget(info_label)
        
        upload_layout.addStretch()
        upload_tab.setLayout(upload_layout)
        self.tab_widget.addTab(upload_tab, "Upload")
        
        layout.addWidget(self.tab_widget)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def set_repository(self, repo: Repository):
        """Set the current repository"""
        self.current_repo = repo
        self.repo_label.setText(f"Repository: {repo.full_name}")
        
        self.refresh_pages.setEnabled(True)
        self.create_page.setEnabled(True)
        self.save_page.setEnabled(True)
        self.preview_page.setEnabled(True)
        self.upload_subfolders.setEnabled(True)
        
        self.load_wiki_pages()
    
    def load_wiki_pages(self):
        """Load wiki pages from repository"""
        if not self.current_repo:
            return
        
        self.pages_table.setRowCount(0)
        self.status_label.setText("Loading wiki pages...")
        
        # Note: GitHub API doesn't directly support wiki operations
        # This would require cloning the wiki repository
        # Wiki repos are at: https://github.com/owner/repo.wiki.git
        
        self.status_label.setText("Wiki pages loaded (placeholder)")
    
    def create_new_page(self):
        """Create a new wiki page"""
        self.tab_widget.setCurrentIndex(1)  # Switch to editor tab
        self.page_title.clear()
        self.page_content.clear()
        self.page_title.setFocus()
        self.status_label.setText("Creating new page")
    
    def save_current_page(self):
        """Save the current page"""
        title = self.page_title.text().strip()
        content = self.page_content.toPlainText()
        
        if not title:
            QMessageBox.warning(self, "No Title", "Please enter a page title.")
            return
        
        if not content:
            QMessageBox.warning(self, "No Content", "Please enter page content.")
            return
        
        if not self.current_repo:
            QMessageBox.warning(self, "No Repository", "Please select a repository first.")
            return
        
        self.status_label.setText(f"Saving page '{title}'...")
        
        if self.github_client.upload_wiki_page(self.current_repo, title, content):
            self.status_label.setText(f"Page '{title}' saved successfully")
            QMessageBox.information(self, "Success", f"Page '{title}' saved successfully")
        else:
            self.status_label.setText(f"Failed to save page '{title}'")
            QMessageBox.warning(self, "Error", "Failed to save page. Check console for details.")
    
    def preview_current_page(self):
        """Preview the current page"""
        content = self.page_content.toPlainText()
        # Show a preview dialog with rendered markdown
        QMessageBox.information(self, "Preview", content)
    
    def browse_wiki_folder(self):
        """Browse for wiki folder"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Wiki Folder")
        
        if dialog.exec():
            folder = dialog.selectedFiles()[0]
            self.wiki_folder.setText(folder)
    
    def upload_all_pages(self):
        """Upload all pages from the selected folder"""
        folder_path = Path(self.wiki_folder.text())
        
        if not folder_path.exists():
            QMessageBox.warning(self, "Invalid Folder", "Please select a valid folder.")
            return
        
        if not self.current_repo:
            QMessageBox.warning(self, "No Repository", "Please select a repository first.")
            return
        
        # Find all markdown files
        md_files = list(folder_path.glob("*.md")) + list(folder_path.glob("*.markdown"))
        
        if not md_files:
            QMessageBox.information(self, "No Files", 
                                   "No Markdown files found in the selected folder.")
            return
        
        self.status_label.setText(f"Uploading {len(md_files)} pages...")
        
        results = self.github_client.upload_wiki_folder(self.current_repo, folder_path)
        
        if results:
            success_count = sum(1 for v in results.values() if v)
            fail_count = len(results) - success_count
            
            if fail_count == 0:
                self.status_label.setText(f"Successfully uploaded {success_count} pages")
                QMessageBox.information(self, "Success", f"Successfully uploaded {success_count} pages")
            else:
                self.status_label.setText(f"Uploaded {success_count} pages, {fail_count} failed")
                QMessageBox.warning(self, "Partial Success", 
                                   f"Uploaded {success_count} pages, {fail_count} failed")
        else:
            self.status_label.setText("Failed to upload pages")
            QMessageBox.warning(self, "Error", "Failed to upload pages. Check console for details.")
