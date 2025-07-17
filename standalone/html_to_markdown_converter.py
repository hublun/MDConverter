#!/usr/bin/env python3
"""
HTML Webpage Package to Markdown Converter

This script converts a complete webpage package (HTML file + assets folder) 
into a comprehensive markdown file. It extracts text content, preserves 
formatting, handles images, and creates a clean markdown document.

Usage:
    python html_to_markdown_converter.py <html_file_path> [output_file]

Example:
    python html_to_markdown_converter.py "Topic Model Labelling with LLMs _ Towards Data Science.html"
"""

import os
import sys
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse
import argparse
from typing import Optional, Dict, List, Tuple

try:
    from bs4 import BeautifulSoup, Tag, NavigableString
    import requests
    from markdownify import markdownify as md
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required packages:")
    print("pip install beautifulsoup4 requests markdownify lxml html5lib")
    sys.exit(1)


class WebpageToMarkdownConverter:
    """Converts HTML webpage packages to markdown format."""
    
    def __init__(self, html_file_path: str, output_file: Optional[str] = None):
        self.html_file_path = Path(html_file_path)
        self.base_dir = self.html_file_path.parent
        self.assets_folder = self._find_assets_folder()
        
        # Set output file with default to output subfolder
        if output_file:
            self.output_file = Path(output_file)
        else:
            # Create output directory if it doesn't exist
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            self.output_file = output_dir / f"{self.html_file_path.stem}.md"
        
        # Create images directory for markdown
        self.images_dir = self.output_file.parent / "images"
        self.images_dir.mkdir(exist_ok=True)
        
        # Track processed images
        self.processed_images: Dict[str, str] = {}
        
    def _find_assets_folder(self) -> Optional[Path]:
        """Find the assets folder associated with the HTML file."""
        # Common patterns for assets folders
        patterns = [
            f"{self.html_file_path.stem}_files",
            f"{self.html_file_path.stem}_assets",
            f"{self.html_file_path.name}_files",
        ]
        
        for pattern in patterns:
            assets_path = self.base_dir / pattern
            if assets_path.exists() and assets_path.is_dir():
                return assets_path
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        # Fix common HTML entities that might remain
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        
        return text
    
    def _process_image(self, img_src: str) -> str:
        """Process image and return markdown-compatible path."""
        if not img_src:
            return ""
        
        # Handle different types of image sources
        if img_src.startswith(('http://', 'https://')):
            # External image - keep as is
            return img_src
        
        if img_src.startswith('data:'):
            # Base64 encoded image - skip for now
            return ""
        
        # Local image file
        img_filename = os.path.basename(img_src)
        
        # Check if image exists in assets folder
        if self.assets_folder:
            potential_paths = [
                self.assets_folder / img_filename,
                self.assets_folder / img_src.lstrip('./'),
                self.base_dir / img_src.lstrip('./'),
            ]
            
            for img_path in potential_paths:
                if img_path.exists():
                    # Copy image to images directory
                    dest_path = self.images_dir / img_filename
                    if not dest_path.exists():
                        shutil.copy2(img_path, dest_path)
                    
                    # Return relative path for markdown
                    return f"images/{img_filename}"
        
        return img_src
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from HTML head."""
        metadata = {}
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = self._clean_text(title_tag.get_text())
        
        # Meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            
            if name and content:
                if name in ['description', 'og:description']:
                    metadata['description'] = content
                elif name in ['author', 'og:author']:
                    metadata['author'] = content
                elif name in ['keywords']:
                    metadata['keywords'] = content
                elif name in ['og:title']:
                    metadata['og_title'] = content
                elif name in ['og:url']:
                    metadata['url'] = content
                elif name in ['article:published_time', 'pubdate']:
                    metadata['published'] = content
        
        return metadata
    
    def _extract_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Extract main content from the webpage."""
        # Remove unwanted elements
        unwanted_selectors = [
            'script', 'style', 'nav', 'header', 'footer',
            '.advertisement', '.ad', '.popup', '.modal',
            '.cookie-banner', '.newsletter-signup',
            '[class*="ad-"]', '[id*="ad-"]',
            '.social-share', '.comments-section'
        ]
        
        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # Try to find main content area
        main_content_selectors = [
            'main', 'article', '[role="main"]',
            '.post-content', '.article-content', '.entry-content',
            '.content', '.main-content'
        ]
        
        for selector in main_content_selectors:
            main_element = soup.select_one(selector)
            if main_element:
                return main_element
        
        # Fallback: return body content
        body = soup.find('body')
        return body if body else soup
    
    def _process_code_blocks(self, soup: BeautifulSoup) -> None:
        """Process code blocks and preserve syntax highlighting info."""
        # Handle <pre><code> blocks
        for pre in soup.find_all('pre'):
            code = pre.find('code')
            if code:
                # Try to detect language from class names
                classes = code.get('class', [])
                language = ""
                
                for cls in classes:
                    if cls.startswith('language-'):
                        language = cls.replace('language-', '')
                        break
                    elif cls.startswith('lang-'):
                        language = cls.replace('lang-', '')
                        break
                
                # Wrap in proper markdown code block
                code_content = code.get_text()
                if language:
                    pre.string = f"```{language}\n{code_content}\n```"
                else:
                    pre.string = f"```\n{code_content}\n```"
                
                # Remove the code tag since we've processed it
                if code.parent == pre:
                    code.unwrap()
    
    def _fix_markdown_formatting(self, markdown_content: str) -> str:
        """Fix and improve markdown formatting."""
        # Fix multiple consecutive newlines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # Fix heading spacing
        markdown_content = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', markdown_content)
        markdown_content = re.sub(r'(#{1,6}.*)\n([^\n#])', r'\1\n\n\2', markdown_content)
        
        # Fix list formatting
        markdown_content = re.sub(r'\n(\*|\+|-|\d+\.)\s', r'\n\n\1 ', markdown_content)
        
        # Fix quote formatting
        markdown_content = re.sub(r'\n(>)', r'\n\n\1', markdown_content)
        
        # Remove extra spaces
        markdown_content = re.sub(r'[ \t]+', ' ', markdown_content)
        
        # Clean up beginning and end
        markdown_content = markdown_content.strip()
        
        return markdown_content
    
    def convert(self) -> str:
        """Convert HTML webpage to markdown."""
        print(f"Converting {self.html_file_path} to markdown...")
        
        # Read HTML file
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(self.html_file_path, 'r', encoding='latin-1') as f:
                html_content = f.read()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract metadata
        metadata = self._extract_metadata(soup)
        
        # Process images first
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src:
                new_src = self._process_image(src)
                if new_src:
                    img['src'] = new_src
                    
                # Add alt text if missing
                if not img.get('alt'):
                    img['alt'] = "Image"
        
        # Process code blocks
        self._process_code_blocks(soup)
        
        # Extract main content
        main_content = self._extract_main_content(soup)
        
        # Convert to markdown
        markdown_content = md(
            str(main_content),
            heading_style="ATX",
            bullets="-",
            strip=['script', 'style', 'nav', 'header', 'footer']
        )
        
        # Fix markdown formatting
        markdown_content = self._fix_markdown_formatting(markdown_content)
        
        # Create final markdown with metadata
        final_markdown = self._create_final_markdown(metadata, markdown_content)
        
        # Write to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(final_markdown)
        
        print(f"✅ Conversion complete! Output saved to: {self.output_file}")
        if self.processed_images:
            print(f"📸 Processed {len(self.processed_images)} images to: {self.images_dir}")
        
        return final_markdown
    
    def _create_final_markdown(self, metadata: Dict[str, str], content: str) -> str:
        """Create the final markdown document with metadata header."""
        lines = []
        
        # Add YAML frontmatter if we have metadata
        if metadata:
            lines.append("---")
            for key, value in metadata.items():
                # Escape quotes in values
                safe_value = value.replace('"', '\\"')
                lines.append(f'{key}: "{safe_value}"')
            lines.append("---")
            lines.append("")
        
        # Add title if available
        if 'title' in metadata:
            lines.append(f"# {metadata['title']}")
            lines.append("")
        
        # Add metadata info
        if any(key in metadata for key in ['author', 'published', 'url']):
            lines.append("## Article Information")
            lines.append("")
            
            if 'author' in metadata:
                lines.append(f"**Author:** {metadata['author']}")
            if 'published' in metadata:
                lines.append(f"**Published:** {metadata['published']}")
            if 'url' in metadata:
                lines.append(f"**Original URL:** {metadata['url']}")
            
            lines.append("")
            if 'description' in metadata:
                lines.append(f"**Description:** {metadata['description']}")
                lines.append("")
        
        # Add horizontal rule before content
        lines.append("---")
        lines.append("")
        
        # Add main content
        lines.append(content)
        
        return "\n".join(lines)


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert HTML webpage package to Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python html_to_markdown_converter.py "webpage.html"
  python html_to_markdown_converter.py "article.html" "output.md"
  python html_to_markdown_converter.py "/path/to/webpage.html" "/path/to/output.md"
        """
    )
    
    parser.add_argument(
        'html_file',
        help='Path to the HTML file to convert'
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Output markdown file path (optional)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"❌ Error: HTML file not found: {html_path}")
        sys.exit(1)
    
    try:
        # Create converter and run conversion
        converter = WebpageToMarkdownConverter(args.html_file, args.output_file)
        result = converter.convert()
        
        if args.verbose:
            print("\n📄 Conversion Summary:")
            print(f"   Input file: {converter.html_file_path}")
            print(f"   Output file: {converter.output_file}")
            print(f"   Assets folder: {converter.assets_folder}")
            print(f"   Images processed: {len(converter.processed_images)}")
            print(f"   Output size: {len(result)} characters")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()