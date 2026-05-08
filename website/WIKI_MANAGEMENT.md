# Wiki Management Guide

This guide covers how to create, edit, and manage repository wikis using GitHub Commander.

## Overview

GitHub wikis are separate git repositories that store documentation in Markdown format. Each repository can have its own wiki at:
```
https://github.com/owner/repo.wiki.git
```

GitHub Commander provides a full-featured wiki editor and batch upload capabilities.

## Wiki Panel Interface

The Wiki Panel has three tabs:

1. **Pages Tab** - List and manage existing wiki pages
2. **Editor Tab** - Create and edit individual pages
3. **Upload Tab** - Batch upload multiple pages from a folder

## Creating Wiki Pages

### Creating a New Page

1. Select a repository
2. Go to the Wiki Panel
3. Click "Create New Page"
4. The Editor tab will open
5. Enter the page title
6. Write your content in Markdown format
7. Click "Save Page"

### Page Title Guidelines

- Use descriptive, unique titles
- Spaces in titles are converted to hyphens in filenames
- Example: "Getting Started" becomes "Getting-Started.md"

### Writing Content

The editor supports full Markdown syntax:

```markdown
# Heading 1
## Heading 2

**Bold text**
*Italic text*

- List item 1
- List item 2

[Link text](url)

`inline code`

```
code block
```
```

### Saving Pages

1. Enter a page title
2. Write your content
3. Click "Save Page"
4. The page will be:
   - Created as a Markdown file
   - Committed to the wiki repository
   - Pushed to GitHub

### Previewing Pages

1. Write your content
2. Click "Preview" button
3. A preview dialog shows rendered Markdown
4. Make adjustments as needed

## Editing Existing Pages

### Editing a Page

1. Go to the Pages tab
2. Click on a page in the table
3. The Editor tab opens with the page content
4. Make your changes
5. Click "Save Page"

### Page History

GitHub wikis maintain a full history of changes. To view history:
1. Go to the wiki on GitHub.com
2. Click "Page History"
3. View and revert changes as needed

## Batch Upload

### Uploading from a Folder

1. Select a repository
2. Go to the Wiki Panel
3. Switch to the "Upload" tab
4. Click "Browse..." to select a folder
5. Select a folder containing Markdown files
6. Click "Upload All Pages"

### Supported File Formats

The upload supports:
- `.md` files
- `.markdown` files

### Upload Process

The application will:
1. Clone the wiki repository
2. Copy all Markdown files from your folder
3. Stage the files for commit
4. Commit with message "Upload wiki pages"
5. Push changes to GitHub

### Upload Results

After upload, you'll see:
- Success/failure count
- Which pages uploaded successfully
- Any pages that failed to upload

## Managing Wiki Pages

### Viewing Page List

1. Go to the Pages tab
2. Click "Refresh Pages"
3. Pages are displayed in a table with:
   - Page Name
   - Last Updated
   - Actions

### Deleting Pages

To delete a wiki page:
1. Go to the wiki on GitHub.com
2. Navigate to the page
3. Click "Edit"
4. Delete all content
5. Commit the change

**Note:** GitHub Commander doesn't currently support deleting wiki pages directly. Use the GitHub web interface.

### Renaming Pages

To rename a wiki page:
1. Go to the wiki on GitHub.com
2. Navigate to the page
3. Click "Edit"
4. Copy the content
5. Create a new page with the new name
6. Paste the content
7. Delete the old page

## Wiki Best Practices

### Content Organization

- Use a clear hierarchy with headings
- Create a "Home" or "Index" page as the main navigation
- Link between related pages
- Use consistent formatting

### Naming Conventions

- Use descriptive titles
- Keep titles concise
- Avoid special characters
- Use title case for main pages

### Markdown Tips

- Use `##` for section headings (not `#` - that's the page title)
- Use `###` for subsections
- Include code blocks with language specification
- Use tables for structured data
- Add images with descriptive alt text

### Linking Between Pages

Use relative links to connect wiki pages:

```markdown
[Getting Started](Getting-Started)
[API Reference](API-Reference)
```

The link text is the page name with spaces replaced by hyphens.

## Wiki Home Page

### Setting the Home Page

The first page you create (typically named "Home") becomes the wiki's home page. To change it:

1. Go to the wiki on GitHub.com
2. Click "Edit" on the desired home page
3. Move it to the top of the page list
4. Save

### Default Home Page

You can configure a default home page name in Settings:
1. Go to Settings
2. Find "Wiki Settings"
3. Set "Default Home" to your preferred page name
4. Click "Save"

## Wiki Permissions

### Access Control

Wiki access follows repository permissions:
- **Public repositories** - Anyone can view and edit
- **Private repositories** - Only collaborators can view and edit
- **Organization repositories** - Organization members with access

### Restricting Edits

To restrict who can edit the wiki:
1. Go to repository Settings on GitHub.com
2. Navigate to "Collaborators & teams"
3. Manage who has write access

## Troubleshooting

### "Failed to upload wiki page"

**Possible causes:**
- Repository doesn't have wiki enabled
- Invalid Markdown file
- Authentication issues
- Network problems

**Solutions:**
- Enable wiki in repository settings
- Verify file is valid Markdown
- Check your authentication
- Ensure internet connection

### "Wiki pages loaded (placeholder)"

The GitHub API doesn't directly support wiki page listing. To view pages:
- Use the GitHub web interface
- Or clone the wiki repository manually

### "No Markdown files found"

**Solutions:**
- Ensure files have `.md` or `.markdown` extension
- Check the selected folder path
- Verify files exist in the folder

## Next Steps

After managing wikis, explore:
- [GitHub Pages](GITHUB_PAGES.md) - Deploy documentation websites
- [File Operations](FILE_OPERATIONS.md) - Manage other repository files
