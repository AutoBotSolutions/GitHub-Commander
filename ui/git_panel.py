"""
Git Panel - Git operations (clone, commit, push, pull, branch management)
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QComboBox,
                             QGroupBox, QFileDialog, QMessageBox, QTabWidget,
                             QCheckBox, QSplitter)
from PySide6.QtCore import Qt
from github.Repository import Repository
from github_client import GitHubClient
from git_operations import GitOperations
from config import Config
from pathlib import Path

class GitPanel(QWidget):
    """Panel for Git operations"""
    
    def __init__(self, git_ops: GitOperations, github_client: GitHubClient, 
                 config: Config, parent=None):
        super().__init__(parent)
        self.git_ops = git_ops
        self.github_client = github_client
        self.config = config
        self.current_repo = None
        self.local_repo_path = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Repository info
        self.repo_label = QLabel("No repository selected")
        layout.addWidget(self.repo_label)
        
        # Tab widget for different Git operations
        self.tab_widget = QTabWidget()
        
        # Clone tab
        clone_tab = self.create_clone_tab()
        self.tab_widget.addTab(clone_tab, "Clone")
        
        # Commit tab
        commit_tab = self.create_commit_tab()
        self.tab_widget.addTab(commit_tab, "Commit")
        
        # Push/Pull tab
        sync_tab = self.create_sync_tab()
        self.tab_widget.addTab(sync_tab, "Sync")
        
        # Branch tab
        branch_tab = self.create_branch_tab()
        self.tab_widget.addTab(branch_tab, "Branches")
        
        # Remote tab
        remote_tab = self.create_remote_tab()
        self.tab_widget.addTab(remote_tab, "Remotes")
        
        layout.addWidget(self.tab_widget)
        
        # Status output
        status_group = QGroupBox("Git Status")
        status_layout = QVBoxLayout()
        
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setMaximumHeight(150)
        status_layout.addWidget(self.status_output)
        
        refresh_status = QPushButton("Refresh Status")
        refresh_status.clicked.connect(self.refresh_status)
        refresh_status.setEnabled(False)
        status_layout.addWidget(refresh_status)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        self.setLayout(layout)
    
    def create_clone_tab(self):
        """Create clone tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Clone from GitHub
        clone_group = QGroupBox("Clone Repository")
        clone_layout = QVBoxLayout()
        
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Repository URL:"))
        self.clone_url = QLineEdit()
        self.clone_url.setPlaceholderText("https://github.com/owner/repo.git")
        url_layout.addWidget(self.clone_url)
        clone_layout.addLayout(url_layout)
        
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Destination:"))
        self.clone_dest = QLineEdit()
        self.clone_dest.setPlaceholderText(str(Path.home() / "github-projects"))
        dest_layout.addWidget(self.clone_dest)
        
        browse_dest = QPushButton("Browse...")
        browse_dest.clicked.connect(self.browse_clone_dest)
        dest_layout.addWidget(browse_dest)
        
        clone_layout.addLayout(dest_layout)
        
        branch_layout = QHBoxLayout()
        branch_layout.addWidget(QLabel("Branch:"))
        self.clone_branch = QLineEdit()
        self.clone_branch.setText("main")
        branch_layout.addWidget(self.clone_branch)
        clone_layout.addLayout(branch_layout)
        
        self.clone_button = QPushButton("Clone Repository")
        self.clone_button.clicked.connect(self.clone_repository)
        clone_layout.addWidget(self.clone_button)
        
        clone_group.setLayout(clone_layout)
        layout.addWidget(clone_group)
        
        # Initialize new repository
        init_group = QGroupBox("Initialize New Repository")
        init_layout = QVBoxLayout()
        
        init_path_layout = QHBoxLayout()
        init_path_layout.addWidget(QLabel("Path:"))
        self.init_path = QLineEdit()
        init_path_layout.addWidget(self.init_path)
        
        browse_init = QPushButton("Browse...")
        browse_init.clicked.connect(self.browse_init_path)
        init_path_layout.addWidget(browse_init)
        
        init_layout.addLayout(init_path_layout)
        
        self.init_button = QPushButton("Initialize Repository")
        self.init_button.clicked.connect(self.init_repository)
        init_layout.addWidget(self.init_button)
        
        init_group.setLayout(init_layout)
        layout.addWidget(init_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_commit_tab(self):
        """Create commit tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Working directory
        work_group = QGroupBox("Working Directory")
        work_layout = QVBoxLayout()
        
        self.work_dir = QLineEdit()
        self.work_dir.setPlaceholderText("/path/to/local/repository")
        work_layout.addWidget(self.work_dir)
        
        browse_work = QPushButton("Browse...")
        browse_work.clicked.connect(self.browse_work_dir)
        work_layout.addWidget(browse_work)
        
        work_group.setLayout(work_layout)
        layout.addWidget(work_group)
        
        # Staging
        stage_group = QGroupBox("Stage Changes")
        stage_layout = QVBoxLayout()
        
        self.stage_all = QPushButton("Stage All Changes")
        self.stage_all.clicked.connect(self.stage_all_changes)
        self.stage_all.setEnabled(False)
        stage_layout.addWidget(self.stage_all)
        
        stage_file_layout = QHBoxLayout()
        stage_file_layout.addWidget(QLabel("Stage File:"))
        self.stage_file = QLineEdit()
        stage_file_layout.addWidget(self.stage_file)
        
        stage_single = QPushButton("Stage")
        stage_single.clicked.connect(self.stage_single_file)
        stage_single.setEnabled(False)
        stage_file_layout.addWidget(stage_single)
        
        stage_layout.addLayout(stage_file_layout)
        
        stage_group.setLayout(stage_layout)
        layout.addWidget(stage_group)
        
        # Commit
        commit_group = QGroupBox("Commit")
        commit_layout = QVBoxLayout()
        
        message_layout = QVBoxLayout()
        message_layout.addWidget(QLabel("Commit Message:"))
        self.commit_message = QTextEdit()
        self.commit_message.setMaximumHeight(80)
        self.commit_message.setPlaceholderText("Enter commit message...")
        message_layout.addWidget(self.commit_message)
        
        commit_layout.addLayout(message_layout)
        
        author_layout = QHBoxLayout()
        author_layout.addWidget(QLabel("Author Name:"))
        self.author_name = QLineEdit()
        self.author_name.setText(self.config.get('git_config.user.name', ''))
        author_layout.addWidget(self.author_name)
        
        author_layout.addWidget(QLabel("Email:"))
        self.author_email = QLineEdit()
        self.author_email.setText(self.config.get('git_config.user.email', ''))
        author_layout.addWidget(self.author_email)
        
        commit_layout.addLayout(author_layout)
        
        self.commit_button = QPushButton("Commit")
        self.commit_button.clicked.connect(self.commit_changes)
        self.commit_button.setEnabled(False)
        commit_layout.addWidget(self.commit_button)
        
        commit_group.setLayout(commit_layout)
        layout.addWidget(commit_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_sync_tab(self):
        """Create push/pull tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Working directory
        work_layout = QHBoxLayout()
        work_layout.addWidget(QLabel("Repository:"))
        self.sync_work_dir = QLineEdit()
        work_layout.addWidget(self.sync_work_dir)
        
        browse_sync = QPushButton("Browse...")
        browse_sync.clicked.connect(self.browse_sync_dir)
        work_layout.addWidget(browse_sync)
        
        layout.addLayout(work_layout)
        
        # Push
        push_group = QGroupBox("Push")
        push_layout = QVBoxLayout()
        
        remote_branch_layout = QHBoxLayout()
        remote_branch_layout.addWidget(QLabel("Remote:"))
        self.push_remote = QLineEdit()
        self.push_remote.setText("origin")
        remote_branch_layout.addWidget(self.push_remote)
        
        remote_branch_layout.addWidget(QLabel("Branch:"))
        self.push_branch = QLineEdit()
        self.push_branch.setText("main")
        remote_branch_layout.addWidget(self.push_branch)
        
        push_layout.addLayout(remote_branch_layout)
        
        self.force_push = QCheckBox("Force Push")
        push_layout.addWidget(self.force_push)
        
        self.push_button = QPushButton("Push")
        self.push_button.clicked.connect(self.push_changes)
        self.push_button.setEnabled(False)
        push_layout.addWidget(self.push_button)
        
        push_group.setLayout(push_layout)
        layout.addWidget(push_group)
        
        # Pull
        pull_group = QGroupBox("Pull")
        pull_layout = QVBoxLayout()
        
        pull_remote_layout = QHBoxLayout()
        pull_remote_layout.addWidget(QLabel("Remote:"))
        self.pull_remote = QLineEdit()
        self.pull_remote.setText("origin")
        pull_remote_layout.addWidget(self.pull_remote)
        
        pull_remote_layout.addWidget(QLabel("Branch:"))
        self.pull_branch = QLineEdit()
        self.pull_branch.setText("main")
        pull_remote_layout.addWidget(self.pull_branch)
        
        pull_layout.addLayout(pull_remote_layout)
        
        self.pull_button = QPushButton("Pull")
        self.pull_button.clicked.connect(self.pull_changes)
        self.pull_button.setEnabled(False)
        pull_layout.addWidget(self.pull_button)
        
        pull_group.setLayout(pull_layout)
        layout.addWidget(pull_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_branch_tab(self):
        """Create branch management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Working directory
        work_layout = QHBoxLayout()
        work_layout.addWidget(QLabel("Repository:"))
        self.branch_work_dir = QLineEdit()
        work_layout.addWidget(self.branch_work_dir)
        
        browse_branch = QPushButton("Browse...")
        browse_branch.clicked.connect(self.browse_branch_dir)
        work_layout.addWidget(browse_branch)
        
        layout.addLayout(work_layout)
        
        # Create branch
        create_group = QGroupBox("Create Branch")
        create_layout = QVBoxLayout()
        
        new_branch_layout = QHBoxLayout()
        new_branch_layout.addWidget(QLabel("New Branch Name:"))
        self.new_branch = QLineEdit()
        new_branch_layout.addWidget(self.new_branch)
        
        create_layout.addLayout(new_branch_layout)
        
        self.create_branch_button = QPushButton("Create Branch")
        self.create_branch_button.clicked.connect(self.create_branch)
        self.create_branch_button.setEnabled(False)
        create_layout.addWidget(self.create_branch_button)
        
        create_group.setLayout(create_layout)
        layout.addWidget(create_group)
        
        # Switch branch
        switch_group = QGroupBox("Switch Branch")
        switch_layout = QVBoxLayout()
        
        self.branch_list = QComboBox()
        switch_layout.addWidget(self.branch_list)
        
        self.switch_branch_button = QPushButton("Switch to Branch")
        self.switch_branch_button.clicked.connect(self.switch_branch)
        self.switch_branch_button.setEnabled(False)
        switch_layout.addWidget(self.switch_branch_button)
        
        refresh_branches = QPushButton("Refresh Branches")
        refresh_branches.clicked.connect(self.load_branches)
        refresh_branches.setEnabled(False)
        switch_layout.addWidget(refresh_branches)
        
        switch_group.setLayout(switch_layout)
        layout.addWidget(switch_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_remote_tab(self):
        """Create remote management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Working directory
        work_layout = QHBoxLayout()
        work_layout.addWidget(QLabel("Repository:"))
        self.remote_work_dir = QLineEdit()
        work_layout.addWidget(self.remote_work_dir)
        
        browse_remote = QPushButton("Browse...")
        browse_remote.clicked.connect(self.browse_remote_dir)
        work_layout.addWidget(browse_remote)
        
        layout.addLayout(work_layout)
        
        # Add remote
        add_group = QGroupBox("Add Remote")
        add_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.remote_name = QLineEdit()
        self.remote_name.setText("origin")
        name_layout.addWidget(self.remote_name)
        
        add_layout.addLayout(name_layout)
        
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.remote_url = QLineEdit()
        url_layout.addWidget(self.remote_url)
        
        add_layout.addLayout(url_layout)
        
        self.add_remote_button = QPushButton("Add Remote")
        self.add_remote_button.clicked.connect(self.add_remote)
        self.add_remote_button.setEnabled(False)
        add_layout.addWidget(self.add_remote_button)
        
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)
        
        # List remotes
        list_group = QGroupBox("Remotes")
        list_layout = QVBoxLayout()
        
        self.remotes_list = QComboBox()
        list_layout.addWidget(self.remotes_list)
        
        refresh_remotes = QPushButton("Refresh Remotes")
        refresh_remotes.clicked.connect(self.load_remotes)
        refresh_remotes.setEnabled(False)
        list_layout.addWidget(refresh_remotes)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def set_repository(self, repo: Repository):
        """Set the current repository"""
        self.current_repo = repo
        self.repo_label.setText(f"Repository: {repo.full_name}")
        
        # Enable buttons
        self.stage_all.setEnabled(True)
        self.stage_single.setEnabled(True)
        self.commit_button.setEnabled(True)
        self.push_button.setEnabled(True)
        self.pull_button.setEnabled(True)
        self.create_branch_button.setEnabled(True)
        self.switch_branch_button.setEnabled(True)
        self.add_remote_button.setEnabled(True)
        refresh_status = self.findChild(QPushButton, "Refresh Status")
        if refresh_status:
            refresh_status.setEnabled(True)
        
        # Set default clone URL
        self.clone_url.setText(repo.clone_url)
    
    def browse_clone_dest(self):
        """Browse for clone destination"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Clone Destination")
        
        if dialog.exec():
            dest = dialog.selectedFiles()[0]
            self.clone_dest.setText(dest)
    
    def browse_init_path(self):
        """Browse for init path"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Repository Path")
        
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.init_path.setText(path)
    
    def browse_work_dir(self):
        """Browse for working directory"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Repository")
        
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.work_dir.setText(path)
    
    def browse_sync_dir(self):
        """Browse for sync directory"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Repository")
        
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.sync_work_dir.setText(path)
    
    def browse_branch_dir(self):
        """Browse for branch directory"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Repository")
        
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.branch_work_dir.setText(path)
    
    def browse_remote_dir(self):
        """Browse for remote directory"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Repository")
        
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.remote_work_dir.setText(path)
    
    def clone_repository(self):
        """Clone a repository"""
        url = self.clone_url.text()
        dest = Path(self.clone_dest.text())
        branch = self.clone_branch.text()
        
        if not url or not dest:
            QMessageBox.warning(self, "Missing Information", 
                              "Please provide URL and destination.")
            return
        
        if self.git_ops.clone_repository(url, dest, branch):
            QMessageBox.information(self, "Success", 
                                   f"Repository cloned to {dest}")
            self.status_output.append(f"Cloned {url} to {dest}")
        else:
            QMessageBox.warning(self, "Error", "Failed to clone repository.")
    
    def init_repository(self):
        """Initialize a new repository"""
        path = Path(self.init_path.text())
        
        if not path:
            QMessageBox.warning(self, "Missing Path", 
                              "Please provide a path.")
            return
        
        if self.git_ops.init_repository(path):
            QMessageBox.information(self, "Success", 
                                   f"Repository initialized at {path}")
            self.status_output.append(f"Initialized repository at {path}")
        else:
            QMessageBox.warning(self, "Error", "Failed to initialize repository.")
    
    def stage_all_changes(self):
        """Stage all changes"""
        work_dir = Path(self.work_dir.text())
        if not work_dir.exists():
            QMessageBox.warning(self, "Invalid Path", "Repository path doesn't exist.")
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.add_all(repo):
                self.status_output.append("Staged all changes")
            else:
                QMessageBox.warning(self, "Error", "Failed to stage changes.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def stage_single_file(self):
        """Stage a single file"""
        work_dir = Path(self.work_dir.text())
        file = self.stage_file.text()
        
        if not work_dir.exists() or not file:
            QMessageBox.warning(self, "Missing Information", 
                              "Please provide repository path and file.")
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.add_file(repo, file):
                self.status_output.append(f"Staged {file}")
            else:
                QMessageBox.warning(self, "Error", "Failed to stage file.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def commit_changes(self):
        """Commit changes"""
        work_dir = Path(self.work_dir.text())
        message = self.commit_message.toPlainText()
        author_name = self.author_name.text()
        author_email = self.author_email.text()
        
        if not work_dir.exists() or not message:
            QMessageBox.warning(self, "Missing Information", 
                              "Please provide repository path and commit message.")
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.commit(repo, message, author_name, author_email):
                self.status_output.append(f"Committed: {message}")
            else:
                QMessageBox.warning(self, "Error", "Failed to commit.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def push_changes(self):
        """Push changes"""
        work_dir = Path(self.sync_work_dir.text())
        remote = self.push_remote.text()
        branch = self.push_branch.text()
        force = self.force_push.isChecked()
        
        if not work_dir.exists():
            QMessageBox.warning(self, "Invalid Path", "Repository path doesn't exist.")
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.push(repo, remote, branch, force):
                self.status_output.append(f"Pushed to {remote}/{branch}")
            else:
                QMessageBox.warning(self, "Error", "Failed to push.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def pull_changes(self):
        """Pull changes"""
        work_dir = Path(self.sync_work_dir.text())
        remote = self.pull_remote.text()
        branch = self.pull_branch.text()
        
        if not work_dir.exists():
            QMessageBox.warning(self, "Invalid Path", "Repository path doesn't exist.")
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.pull(repo, remote, branch):
                self.status_output.append(f"Pulled from {remote}/{branch}")
            else:
                QMessageBox.warning(self, "Error", "Failed to pull.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def create_branch(self):
        """Create a new branch"""
        work_dir = Path(self.branch_work_dir.text())
        branch_name = self.new_branch.text()
        
        if not work_dir.exists() or not branch_name:
            QMessageBox.warning(self, "Missing Information", 
                              "Please provide repository path and branch name.")
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.create_branch(repo, branch_name):
                self.status_output.append(f"Created branch: {branch_name}")
                self.load_branches()
            else:
                QMessageBox.warning(self, "Error", "Failed to create branch.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def switch_branch(self):
        """Switch to a branch"""
        work_dir = Path(self.branch_work_dir.text())
        branch_name = self.branch_list.currentText()
        
        if not work_dir.exists() or not branch_name:
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.checkout_branch(repo, branch_name):
                self.status_output.append(f"Switched to branch: {branch_name}")
            else:
                QMessageBox.warning(self, "Error", "Failed to switch branch.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def load_branches(self):
        """Load branches"""
        work_dir = Path(self.branch_work_dir.text())
        if not work_dir.exists():
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            branches = self.git_ops.get_branches(repo)
            self.branch_list.clear()
            self.branch_list.addItems(branches)
            self.status_output.append(f"Loaded {len(branches)} branches")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def add_remote(self):
        """Add a remote"""
        work_dir = Path(self.remote_work_dir.text())
        name = self.remote_name.text()
        url = self.remote_url.text()
        
        if not work_dir.exists() or not name or not url:
            QMessageBox.warning(self, "Missing Information", 
                              "Please provide all fields.")
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            if self.git_ops.add_remote(repo, name, url):
                self.status_output.append(f"Added remote: {name}")
                self.load_remotes()
            else:
                QMessageBox.warning(self, "Error", "Failed to add remote.")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def load_remotes(self):
        """Load remotes"""
        work_dir = Path(self.remote_work_dir.text())
        if not work_dir.exists():
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            remotes = self.git_ops.get_remotes(repo)
            self.remotes_list.clear()
            self.remotes_list.addItems(remotes)
            self.status_output.append(f"Loaded {len(remotes)} remotes")
        except:
            QMessageBox.warning(self, "Error", "Not a git repository.")
    
    def refresh_status(self):
        """Refresh git status"""
        work_dir = Path(self.work_dir.text())
        if not work_dir.exists():
            return
        
        try:
            from git import Repo
            repo = Repo(work_dir)
            status = self.git_ops.get_status(repo)
            self.status_output.setText(status)
        except:
            self.status_output.setText("Not a git repository.")
