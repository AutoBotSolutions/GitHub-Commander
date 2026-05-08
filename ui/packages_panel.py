"""
Packages Panel - Upload and manage packages
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QTextEdit,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFileDialog, QMessageBox, QTabWidget,
                             QCheckBox)
from PySide6.QtCore import Qt
from github.Repository import Repository
from github_client import GitHubClient
from config import Config
from pathlib import Path

class PackagesPanel(QWidget):
    """Panel for package management and uploads"""
    
    def __init__(self, github_client: GitHubClient, config: Config, parent=None):
        super().__init__(parent)
        self.github_client = github_client
        self.config = config
        self.current_repo = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Repository info
        self.repo_label = QLabel("No repository selected")
        layout.addWidget(self.repo_label)
        
        # Tab widget for different package types
        self.tab_widget = QTabWidget()
        
        # NPM tab
        npm_tab = self.create_npm_tab()
        self.tab_widget.addTab(npm_tab, "NPM")
        
        # PyPI tab
        pypi_tab = self.create_pypi_tab()
        self.tab_widget.addTab(pypi_tab, "PyPI")
        
        # Cargo tab
        cargo_tab = self.create_cargo_tab()
        self.tab_widget.addTab(cargo_tab, "Cargo")
        
        # Docker tab
        docker_tab = self.create_docker_tab()
        self.tab_widget.addTab(docker_tab, "Docker")
        
        # Generic tab
        generic_tab = self.create_generic_tab()
        self.tab_widget.addTab(generic_tab, "Generic")
        
        layout.addWidget(self.tab_widget)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def create_npm_tab(self):
        """Create NPM package tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Package info
        info_group = QGroupBox("NPM Package Information")
        info_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Package Name:"))
        self.npm_name = QLineEdit()
        self.npm_name.setPlaceholderText("@scope/package-name")
        name_layout.addWidget(self.npm_name)
        info_layout.addLayout(name_layout)
        
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("Version:"))
        self.npm_version = QLineEdit()
        self.npm_version.setPlaceholderText("1.0.0")
        version_layout.addWidget(self.npm_version)
        info_layout.addLayout(version_layout)
        
        registry_layout = QHBoxLayout()
        registry_layout.addWidget(QLabel("Registry:"))
        self.npm_registry = QLineEdit()
        self.npm_registry.setText(self.config.get('packages.npm_registry', 'https://registry.npmjs.org'))
        registry_layout.addWidget(self.npm_registry)
        info_layout.addLayout(registry_layout)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Build and publish
        build_group = QGroupBox("Build & Publish")
        build_layout = QVBoxLayout()
        
        self.npm_install = QPushButton("Install Dependencies")
        self.npm_install.clicked.connect(lambda: self.run_npm_command("npm install"))
        self.npm_install.setEnabled(False)
        build_layout.addWidget(self.npm_install)
        
        self.npm_build = QPushButton("Build Package")
        self.npm_build.clicked.connect(lambda: self.run_npm_command("npm run build"))
        self.npm_build.setEnabled(False)
        build_layout.addWidget(self.npm_build)
        
        self.npm_publish = QPushButton("Publish to NPM")
        self.npm_publish.clicked.connect(self.publish_npm)
        self.npm_publish.setEnabled(False)
        build_layout.addWidget(self.npm_publish)
        
        build_group.setLayout(build_layout)
        layout.addWidget(build_group)
        
        # Package.json editor
        editor_group = QGroupBox("package.json Editor")
        editor_layout = QVBoxLayout()
        
        self.npm_package_json = QTextEdit()
        self.npm_package_json.setPlaceholderText("package.json content...")
        self.npm_package_json.setMaximumHeight(150)
        editor_layout.addWidget(self.npm_package_json)
        
        load_package = QPushButton("Load package.json")
        load_package.clicked.connect(self.load_package_json)
        load_package.setEnabled(False)
        editor_layout.addWidget(load_package)
        
        editor_group.setLayout(editor_layout)
        layout.addWidget(editor_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_pypi_tab(self):
        """Create PyPI package tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Package info
        info_group = QGroupBox("PyPI Package Information")
        info_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Package Name:"))
        self.pypi_name = QLineEdit()
        name_layout.addWidget(self.pypi_name)
        info_layout.addLayout(name_layout)
        
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("Version:"))
        self.pypi_version = QLineEdit()
        version_layout.addWidget(self.pypi_version)
        info_layout.addLayout(version_layout)
        
        repository_layout = QHBoxLayout()
        repository_layout.addWidget(QLabel("Repository:"))
        self.pypi_repository = QLineEdit()
        self.pypi_repository.setText(self.config.get('packages.pypi_repository', 'https://pypi.org/simple'))
        repository_layout.addWidget(self.pypi_repository)
        info_layout.addLayout(repository_layout)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Build and publish
        build_group = QGroupBox("Build & Publish")
        build_layout = QVBoxLayout()
        
        self.pypi_build = QPushButton("Build Distribution")
        self.pypi_build.clicked.connect(self.build_pypi)
        self.pypi_build.setEnabled(False)
        build_layout.addWidget(self.pypi_build)
        
        self.pypi_upload = QPushButton("Upload to PyPI")
        self.pypi_upload.clicked.connect(self.upload_pypi)
        self.pypi_upload.setEnabled(False)
        build_layout.addWidget(self.pypi_upload)
        
        self.pypi_test_upload = QPushButton("Upload to TestPyPI")
        self.pypi_test_upload.clicked.connect(self.upload_test_pypi)
        self.pypi_test_upload.setEnabled(False)
        build_layout.addWidget(self.pypi_test_upload)
        
        build_group.setLayout(build_layout)
        layout.addWidget(build_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_cargo_tab(self):
        """Create Cargo/Rust package tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Package info
        info_group = QGroupBox("Cargo Package Information")
        info_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Package Name:"))
        self.cargo_name = QLineEdit()
        name_layout.addWidget(self.cargo_name)
        info_layout.addLayout(name_layout)
        
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("Version:"))
        self.cargo_version = QLineEdit()
        version_layout.addWidget(self.cargo_version)
        info_layout.addLayout(version_layout)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Build and publish
        build_group = QGroupBox("Build & Publish")
        build_layout = QVBoxLayout()
        
        self.cargo_build = QPushButton("Build Package")
        self.cargo_build.clicked.connect(lambda: self.run_cargo_command("cargo build --release"))
        self.cargo_build.setEnabled(False)
        build_layout.addWidget(self.cargo_build)
        
        self.cargo_test = QPushButton("Run Tests")
        self.cargo_test.clicked.connect(lambda: self.run_cargo_command("cargo test"))
        self.cargo_test.setEnabled(False)
        build_layout.addWidget(self.cargo_test)
        
        self.cargo_publish = QPushButton("Publish to crates.io")
        self.cargo_publish.clicked.connect(self.publish_cargo)
        self.cargo_publish.setEnabled(False)
        build_layout.addWidget(self.cargo_publish)
        
        build_group.setLayout(build_layout)
        layout.addWidget(build_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_docker_tab(self):
        """Create Docker tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Docker info
        info_group = QGroupBox("Docker Image")
        info_layout = QVBoxLayout()
        
        image_layout = QHBoxLayout()
        image_layout.addWidget(QLabel("Image Name:"))
        self.docker_image = QLineEdit()
        self.docker_image.setPlaceholderText("username/imagename:tag")
        image_layout.addWidget(self.docker_image)
        info_layout.addLayout(image_layout)
        
        registry_layout = QHBoxLayout()
        registry_layout.addWidget(QLabel("Registry:"))
        self.docker_registry = QLineEdit()
        self.docker_registry.setPlaceholderText("docker.io, ghcr.io, etc.")
        registry_layout.addWidget(self.docker_registry)
        info_layout.addLayout(registry_layout)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Dockerfile
        dockerfile_group = QGroupBox("Dockerfile")
        dockerfile_layout = QVBoxLayout()
        
        self.dockerfile_editor = QTextEdit()
        self.dockerfile_editor.setPlaceholderText("Dockerfile content...")
        self.dockerfile_editor.setMaximumHeight(200)
        dockerfile_layout.addWidget(self.dockerfile_editor)
        
        load_dockerfile = QPushButton("Load Dockerfile")
        load_dockerfile.clicked.connect(self.load_dockerfile)
        load_dockerfile.setEnabled(False)
        dockerfile_layout.addWidget(load_dockerfile)
        
        dockerfile_group.setLayout(dockerfile_layout)
        layout.addWidget(dockerfile_group)
        
        # Build and push
        action_group = QGroupBox("Actions")
        action_layout = QVBoxLayout()
        
        self.docker_build = QPushButton("Build Image")
        self.docker_build.clicked.connect(self.build_docker)
        self.docker_build.setEnabled(False)
        action_layout.addWidget(self.docker_build)
        
        self.docker_push = QPushButton("Push to Registry")
        self.docker_push.clicked.connect(self.push_docker)
        self.docker_push.setEnabled(False)
        action_layout.addWidget(self.docker_push)
        
        self.docker_login = QPushButton("Login to Registry")
        self.docker_login.clicked.connect(self.docker_login_registry)
        self.docker_login.setEnabled(False)
        action_layout.addWidget(self.docker_login)
        
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_generic_tab(self):
        """Create generic file upload tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # File selection
        file_group = QGroupBox("Upload Files")
        file_layout = QVBoxLayout()
        
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Source Folder:"))
        self.generic_folder = QLineEdit()
        folder_layout.addWidget(self.generic_folder)
        
        browse_folder = QPushButton("Browse...")
        browse_folder.clicked.connect(self.browse_generic_folder)
        folder_layout.addWidget(browse_folder)
        
        file_layout.addLayout(folder_layout)
        
        # Upload options
        self.generic_recursive = QCheckBox("Include subdirectories")
        file_layout.addWidget(self.generic_recursive)
        
        self.generic_upload = QPushButton("Upload Files")
        self.generic_upload.clicked.connect(self.upload_generic)
        self.generic_upload.setEnabled(False)
        file_layout.addWidget(self.generic_upload)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def set_repository(self, repo: Repository):
        """Set the current repository"""
        self.current_repo = repo
        self.repo_label.setText(f"Repository: {repo.full_name}")
        
        # Enable all buttons
        self.npm_install.setEnabled(True)
        self.npm_build.setEnabled(True)
        self.npm_publish.setEnabled(True)
        self.pypi_build.setEnabled(True)
        self.pypi_upload.setEnabled(True)
        self.pypi_test_upload.setEnabled(True)
        self.cargo_build.setEnabled(True)
        self.cargo_test.setEnabled(True)
        self.cargo_publish.setEnabled(True)
        self.docker_build.setEnabled(True)
        self.docker_push.setEnabled(True)
        self.docker_login.setEnabled(True)
        self.generic_upload.setEnabled(True)
        
        # Load package files
        self.load_package_json()
    
    def load_package_json(self):
        """Load package.json if it exists"""
        # In a real implementation, this would read from the cloned repository
        self.npm_package_json.setText("{}")
    
    def run_npm_command(self, command: str):
        """Run an npm command"""
        self.status_label.setText(f"Running: {command}")
        # In a real implementation, this would execute the command
    
    def publish_npm(self):
        """Publish to NPM"""
        self.status_label.setText("Publishing to NPM...")
        # In a real implementation, this would run: npm publish
    
    def build_pypi(self):
        """Build PyPI distribution"""
        self.status_label.setText("Building PyPI distribution...")
        # In a real implementation, this would run: python -m build
    
    def upload_pypi(self):
        """Upload to PyPI"""
        self.status_label.setText("Uploading to PyPI...")
        # In a real implementation, this would run: twine upload dist/*
    
    def upload_test_pypi(self):
        """Upload to TestPyPI"""
        self.status_label.setText("Uploading to TestPyPI...")
        # In a real implementation, this would run: twine upload --repository testpypi dist/*
    
    def run_cargo_command(self, command: str):
        """Run a cargo command"""
        self.status_label.setText(f"Running: {command}")
        # In a real implementation, this would execute the command
    
    def publish_cargo(self):
        """Publish to crates.io"""
        self.status_label.setText("Publishing to crates.io...")
        # In a real implementation, this would run: cargo publish
    
    def load_dockerfile(self):
        """Load Dockerfile"""
        # In a real implementation, this would read the Dockerfile
        self.dockerfile_editor.setText("FROM alpine:latest\n")
    
    def build_docker(self):
        """Build Docker image"""
        image = self.docker_image.text()
        self.status_label.setText(f"Building Docker image: {image}")
        # In a real implementation, this would run: docker build -t image .
    
    def push_docker(self):
        """Push Docker image"""
        image = self.docker_image.text()
        self.status_label.setText(f"Pushing Docker image: {image}")
        # In a real implementation, this would run: docker push image
    
    def docker_login_registry(self):
        """Login to Docker registry"""
        self.status_label.setText("Login to registry...")
        # In a real implementation, this would run: docker login
    
    def browse_generic_folder(self):
        """Browse for folder"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Folder")
        
        if dialog.exec():
            folder = dialog.selectedFiles()[0]
            self.generic_folder.setText(folder)
    
    def upload_generic(self):
        """Upload generic files"""
        folder = self.generic_folder.text()
        self.status_label.setText(f"Uploading from: {folder}")
        # In a real implementation, this would upload the files
