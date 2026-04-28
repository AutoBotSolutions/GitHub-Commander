"""
GitHub Pages Panel - Deploy and manage GitHub Pages sites
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QCheckBox,
                             QTextEdit, QGroupBox, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt
from github.Repository import Repository
from github_client import GitHubClient
from config import Config
from pathlib import Path

class PagesPanel(QWidget):
    """Panel for GitHub Pages deployment and management"""
    
    def __init__(self, github_client: GitHubClient, config: Config, parent=None):
        super().__init__(parent)
        self.github_client = github_client
        self.config = config
        self.current_repo = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Pages status group
        status_group = QGroupBox("Pages Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("No repository selected")
        status_layout.addWidget(self.status_label)
        
        self.url_label = QLabel("")
        self.url_label.setOpenExternalLinks(True)
        status_layout.addWidget(self.url_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Deployment settings
        deploy_group = QGroupBox("Deployment Settings")
        deploy_layout = QVBoxLayout()
        
        # Source branch
        branch_layout = QHBoxLayout()
        branch_label = QLabel("Source Branch:")
        branch_layout.addWidget(branch_label)
        
        self.source_branch = QComboBox()
        self.source_branch.addItems(["main", "master", "gh-pages"])
        self.source_branch.setCurrentText(self.config.get('pages.source_branch', 'main'))
        branch_layout.addWidget(self.source_branch)
        
        deploy_layout.addLayout(branch_layout)
        
        # Source directory
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Source Directory:")
        dir_layout.addWidget(dir_label)
        
        self.source_dir = QLineEdit("/")
        dir_layout.addWidget(self.source_dir)
        
        deploy_layout.addLayout(dir_layout)
        
        # Custom domain
        domain_layout = QHBoxLayout()
        domain_label = QLabel("Custom Domain (optional):")
        domain_layout.addWidget(domain_label)
        
        self.custom_domain = QLineEdit()
        self.custom_domain.setText(self.config.get('pages.custom_domain', ''))
        domain_layout.addWidget(self.custom_domain)
        
        deploy_layout.addLayout(domain_layout)
        
        # HTTPS enforcement
        self.enforce_https = QCheckBox("Enforce HTTPS")
        deploy_layout.addWidget(self.enforce_https)
        
        deploy_group.setLayout(deploy_layout)
        layout.addWidget(deploy_group)
        
        # Build settings
        build_group = QGroupBox("Build Settings (for GitHub Actions)")
        build_layout = QVBoxLayout()
        
        self.use_actions = QCheckBox("Use GitHub Actions for building")
        self.use_actions.setChecked(True)
        build_layout.addWidget(self.use_actions)
        
        # Framework selection
        framework_layout = QHBoxLayout()
        framework_label = QLabel("Framework:")
        framework_layout.addWidget(framework_label)
        
        self.framework_combo = QComboBox()
        self.framework_combo.addItems([
            "None (Static)",
            "React",
            "Vue",
            "Angular",
            "Next.js",
            "Gatsby",
            "Hugo",
            "Jekyll",
            "Custom"
        ])
        framework_layout.addWidget(self.framework_combo)
        
        build_layout.addLayout(framework_layout)
        
        build_group.setLayout(build_layout)
        layout.addWidget(build_group)
        
        # Actions
        actions_layout = QHBoxLayout()
        
        self.enable_pages = QPushButton("Enable Pages")
        self.enable_pages.clicked.connect(self.enable_pages_site)
        self.enable_pages.setEnabled(False)
        actions_layout.addWidget(self.enable_pages)
        
        self.disable_pages = QPushButton("Disable Pages")
        self.disable_pages.clicked.connect(self.disable_pages_site)
        self.disable_pages.setEnabled(False)
        actions_layout.addWidget(self.disable_pages)
        
        self.deploy_button = QPushButton("Deploy")
        self.deploy_button.clicked.connect(self.deploy)
        self.deploy_button.setEnabled(False)
        actions_layout.addWidget(self.deploy_button)
        
        layout.addLayout(actions_layout)
        
        # Workflow editor
        workflow_group = QGroupBox("GitHub Actions Workflow")
        workflow_layout = QVBoxLayout()
        
        self.workflow_editor = QTextEdit()
        self.workflow_editor.setPlaceholderText("GitHub Actions workflow YAML will appear here...")
        self.workflow_editor.setMaximumHeight(200)
        workflow_layout.addWidget(self.workflow_editor)
        
        generate_workflow = QPushButton("Generate Workflow")
        generate_workflow.clicked.connect(self.generate_workflow)
        workflow_layout.addWidget(generate_workflow)
        
        workflow_group.setLayout(workflow_layout)
        layout.addWidget(workflow_group)
        
        # Logs
        logs_group = QGroupBox("Deployment Logs")
        logs_layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMaximumHeight(150)
        logs_layout.addWidget(self.logs_text)
        
        logs_group.setLayout(logs_layout)
        layout.addWidget(logs_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def set_repository(self, repo: Repository):
        """Set the current repository"""
        self.current_repo = repo
        self.enable_pages.setEnabled(True)
        self.disable_pages.setEnabled(True)
        self.deploy_button.setEnabled(True)
        self.status_label.setText(f"Repository: {repo.full_name}")
        
        # Check if Pages is enabled
        try:
            pages = repo.get_pages()
            if pages:
                self.status_label.setText(f"Pages Status: Active\nURL: {pages.html_url}")
                self.url_label.setText(f'<a href="{pages.html_url}">{pages.html_url}</a>')
            else:
                self.status_label.setText("Pages Status: Not enabled")
        except:
            self.status_label.setText("Pages Status: Unknown")
    
    def enable_pages_site(self):
        """Enable GitHub Pages for the repository"""
        if not self.current_repo:
            QMessageBox.warning(self, "No Repository", "Please select a repository first.")
            return
        
        branch = self.source_branch.currentText()
        path = self.source_dir.text() or "/"
        
        self.add_log(f"Enabling Pages for branch: {branch}, path: {path}")
        
        if self.github_client.enable_pages(self.current_repo, branch, path):
            self.status_label.setText("Pages enabled successfully")
            self.add_log("GitHub Pages enabled successfully")
            QMessageBox.information(self, "Success", "GitHub Pages enabled successfully")
        else:
            self.status_label.setText("Failed to enable Pages")
            self.add_log("Failed to enable GitHub Pages")
            QMessageBox.warning(self, "Error", "Failed to enable GitHub Pages. Check console for details.")
    
    def disable_pages_site(self):
        """Disable GitHub Pages"""
        if not self.current_repo:
            return
        
        # GitHub API doesn't have a direct disable method
        # This would require API calls to update settings
        QMessageBox.information(self, "Info", 
                               "To disable Pages, go to repository Settings → Pages")
    
    def deploy(self):
        """Deploy to GitHub Pages"""
        if not self.current_repo:
            QMessageBox.warning(self, "No Repository", "Please select a repository first.")
            return
        
        self.add_log("Starting deployment...")
        
        # Ask for content folder
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setWindowTitle("Select Folder to Deploy")
        
        if not dialog.exec():
            self.add_log("Deployment cancelled")
            return
        
        folder_path = Path(dialog.selectedFiles()[0])
        self.add_log(f"Selected folder: {folder_path}")
        
        source_branch = self.source_branch.currentText()
        source_dir = self.source_dir.text()
        
        if self.use_actions.isChecked():
            self.add_log("Using GitHub Actions for deployment")
            
            # Generate workflow
            self.generate_workflow()
            workflow_content = self.workflow_editor.toPlainText()
            
            # Create workflow file
            if self.github_client.create_pages_workflow(self.current_repo, workflow_content, source_branch):
                self.add_log("Workflow file created successfully")
            else:
                self.add_log("Failed to create workflow file")
                QMessageBox.warning(self, "Error", "Failed to create workflow file")
                return
            
            # Upload content
            self.add_log("Uploading content...")
            results = self.github_client.upload_pages_content(
                self.current_repo, 
                folder_path, 
                source_dir if source_dir != "/" else "",
                source_branch
            )
            
            if results:
                success_count = sum(1 for v in results.values() if v)
                fail_count = len(results) - success_count
                self.add_log(f"Uploaded {success_count} files, {fail_count} failed")
                
                if fail_count == 0:
                    self.add_log("Content uploaded successfully")
                    QMessageBox.information(self, "Success", 
                                           f"Workflow and content uploaded successfully.\nPush to trigger deployment.")
                else:
                    QMessageBox.warning(self, "Partial Success", 
                                       f"Uploaded {success_count} files, {fail_count} failed")
            else:
                self.add_log("Failed to upload content")
                QMessageBox.warning(self, "Error", "Failed to upload content")
        else:
            self.add_log("Manual deployment mode - uploading content only")
            results = self.github_client.upload_pages_content(
                self.current_repo, 
                folder_path, 
                source_dir if source_dir != "/" else "",
                source_branch
            )
            
            if results:
                success_count = sum(1 for v in results.values() if v)
                fail_count = len(results) - success_count
                self.add_log(f"Uploaded {success_count} files, {fail_count} failed")
                
                if fail_count == 0:
                    self.add_log("Content uploaded successfully")
                    QMessageBox.information(self, "Success", "Content uploaded successfully")
                else:
                    QMessageBox.warning(self, "Partial Success", 
                                       f"Uploaded {success_count} files, {fail_count} failed")
            else:
                self.add_log("Failed to upload content")
                QMessageBox.warning(self, "Error", "Failed to upload content")
    
    def generate_workflow(self):
        """Generate GitHub Actions workflow for Pages deployment"""
        framework = self.framework_combo.currentText()
        source_branch = self.source_branch.currentText()
        source_dir = self.source_dir.text()
        
        workflow = f"""name: Deploy to GitHub Pages

on:
  push:
    branches: [ {source_branch} ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{{ steps.deployment.outputs.page_url }}}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
"""
        
        if framework in ["React", "Vue", "Angular", "Next.js"]:
            workflow += f"""      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '{source_dir if source_dir != '/' else './dist'}'
"""
        elif framework in ["Hugo"]:
            workflow += """      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: 'latest'
          extended: true
      
      - name: Build
        run: hugo --minify
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './public'
"""
        elif framework in ["Jekyll"]:
            workflow += """      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      
      - name: Build with Jekyll
        run: bundle exec jekyll build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './_site'
"""
        else:
            workflow += f"""      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '{source_dir if source_dir != '/' else '.'}'
"""
        
        workflow += """      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
        
        self.workflow_editor.setText(workflow)
        self.add_log(f"Generated workflow for {framework}")
    
    def add_log(self, message: str):
        """Add a log message"""
        self.logs_text.append(f"[{self.get_timestamp()}] {message}")
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
