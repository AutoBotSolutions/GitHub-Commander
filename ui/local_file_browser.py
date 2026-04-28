"""
Local File Browser - Left pane for local file system
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeView, 
                             QHeaderView, QPushButton, QLineEdit, QLabel,
                             QFileDialog, QMenu, QFileSystemModel)
from PySide6.QtCore import Qt, QDir, Signal
from pathlib import Path
from git_operations import GitOperations
from config import Config

class LocalFileBrowser(QWidget):
    """File browser for local file system"""
    
    file_selected = Signal(str)
    
    def __init__(self, config: Config, git_ops: GitOperations, parent=None):
        super().__init__(parent)
        self.config = config
        self.git_ops = git_ops
        self.current_path = Path.home()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Path navigation
        nav_layout = QHBoxLayout()
        
        self.path_input = QLineEdit()
        self.path_input.setText(str(self.current_path))
        self.path_input.returnPressed.connect(self.navigate_to_path)
        nav_layout.addWidget(self.path_input)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_directory)
        nav_layout.addWidget(browse_button)
        
        layout.addLayout(nav_layout)
        
        # File tree
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        
        # Show hidden files based on settings
        self.file_model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
        )
        
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(str(self.current_path)))
        self.file_tree.setSortingEnabled(True)
        self.file_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        
        # Hide columns except name
        for col in range(1, 4):
            self.file_tree.hideColumn(col)
        
        self.file_tree.header().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        
        self.file_tree.setSelectionMode(
            QTreeView.SelectionMode.ExtendedSelection
        )
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.file_tree.clicked.connect(self.on_file_clicked)
        
        layout.addWidget(self.file_tree)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        up_button = QPushButton("Up")
        up_button.clicked.connect(self.go_up)
        actions_layout.addWidget(up_button)
        
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        actions_layout.addWidget(home_button)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)
        actions_layout.addWidget(refresh_button)
        
        layout.addLayout(actions_layout)
        
        self.setLayout(layout)
    
    def navigate_to_path(self):
        """Navigate to the path in the input"""
        path = Path(self.path_input.text())
        if path.exists() and path.is_dir():
            self.current_path = path
            self.file_tree.setRootIndex(self.file_model.index(str(path)))
            self.status_label.setText(f"Directory: {path}")
        else:
            self.status_label.setText("Invalid directory")
    
    def browse_directory(self):
        """Browse for a directory"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Directory")
        
        if dialog.exec():
            selected = dialog.selectedFiles()[0]
            self.current_path = Path(selected)
            self.path_input.setText(str(self.current_path))
            self.file_tree.setRootIndex(self.file_model.index(selected))
            self.status_label.setText(f"Directory: {self.current_path}")
    
    def go_up(self):
        """Go up one directory"""
        parent = self.current_path.parent
        if parent != self.current_path:
            self.current_path = parent
            self.path_input.setText(str(self.current_path))
            self.file_tree.setRootIndex(self.file_model.index(str(parent)))
            self.status_label.setText(f"Directory: {self.current_path}")
    
    def go_home(self):
        """Go to home directory"""
        self.current_path = Path.home()
        self.path_input.setText(str(self.current_path))
        self.file_tree.setRootIndex(self.file_model.index(str(Path.home())))
        self.status_label.setText(f"Directory: {self.current_path}")
    
    def refresh(self):
        """Refresh the file tree"""
        self.file_model.setRootPath("")  # Force refresh
        self.file_tree.setRootIndex(self.file_model.index(str(self.current_path)))
        self.status_label.setText("Refreshed")
    
    def on_file_clicked(self, index):
        """Handle file click"""
        path = self.file_model.filePath(index)
        self.file_selected.emit(path)
        self.status_label.setText(f"Selected: {Path(path).name}")
    
    def show_context_menu(self, position):
        """Show context menu"""
        index = self.file_tree.indexAt(position)
        if not index.isValid():
            return
        
        path = Path(self.file_model.filePath(index))
        menu = QMenu()
        
        if path.is_dir():
            menu.addAction("Open in Terminal", lambda: self.open_in_terminal(path))
            menu.addAction("Set as Upload Root", lambda: self.set_as_upload_root(path))
        
        menu.exec(self.file_tree.viewport().mapToGlobal(position))
    
    def open_in_terminal(self, path: Path):
        """Open directory in terminal"""
        # This would open a terminal - implementation depends on desktop environment
        self.status_label.setText(f"Terminal: {path}")
    
    def set_as_upload_root(self, path: Path):
        """Set directory as upload root"""
        self.current_path = path
        self.path_input.setText(str(path))
        self.file_tree.setRootIndex(self.file_model.index(str(path)))
        self.status_label.setText(f"Upload root: {path}")
    
    def get_selected_files(self):
        """Get selected file paths"""
        selected = self.file_tree.selectionModel().selectedIndexes()
        files = set()
        for index in selected:
            if index.column() == 0:  # Only get file name column
                path = self.file_model.filePath(index)
                files.add(path)
        return list(files)
    
    def get_current_path(self):
        """Get current directory path"""
        return str(self.current_path)
