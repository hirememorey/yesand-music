#!/usr/bin/env python3
"""
Markdown Concatenation Script

This script concatenates all markdown files in the project into a single
all_markdown_content.txt file for easy reference and context.

Usage:
    python concatenate_markdown.py [output_file]

If no output file is specified, defaults to 'all_markdown_content.txt'
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple


def find_markdown_files(root_dir: str) -> List[Tuple[str, str]]:
    """
    Find all markdown files in the project.
    
    Args:
        root_dir: Root directory to search
        
    Returns:
        List of tuples (file_path, relative_path)
    """
    markdown_files = []
    root_path = Path(root_dir)
    
    # Find all .md files recursively
    for md_file in root_path.rglob("*.md"):
        # Skip files in hidden directories
        if any(part.startswith('.') for part in md_file.parts):
            continue
            
        # Get relative path for display
        relative_path = md_file.relative_to(root_path)
        markdown_files.append((str(md_file), str(relative_path)))
    
    # Sort by relative path for consistent ordering
    markdown_files.sort(key=lambda x: x[1])
    
    return markdown_files


def read_file_content(file_path: str) -> str:
    """
    Read file content with error handling.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File content as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: Could not read {file_path}: {e}\n"


def concatenate_markdown_files(root_dir: str, output_file: str) -> None:
    """
    Concatenate all markdown files into a single file.
    
    Args:
        root_dir: Root directory to search for markdown files
        output_file: Output file path
    """
    print(f"Searching for markdown files in: {root_dir}")
    
    # Find all markdown files
    markdown_files = find_markdown_files(root_dir)
    
    if not markdown_files:
        print("No markdown files found!")
        return
    
    print(f"Found {len(markdown_files)} markdown files:")
    for _, relative_path in markdown_files:
        print(f"  - {relative_path}")
    
    # Create output content
    output_content = []
    output_content.append("=" * 80)
    output_content.append("YESAND MUSIC PROJECT - ALL MARKDOWN CONTENT")
    output_content.append("=" * 80)
    output_content.append(f"Generated: {os.popen('date').read().strip()}")
    output_content.append(f"Total files: {len(markdown_files)}")
    output_content.append("=" * 80)
    output_content.append("")
    
    # Process each markdown file
    for file_path, relative_path in markdown_files:
        print(f"Processing: {relative_path}")
        
        # Add file header
        output_content.append("=" * 80)
        output_content.append(f"FILE: {relative_path}")
        output_content.append("=" * 80)
        output_content.append("")
        
        # Add file content
        content = read_file_content(file_path)
        output_content.append(content)
        
        # Add separator
        output_content.append("")
        output_content.append("=" * 80)
        output_content.append("")
    
    # Write output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_content))
        print(f"\n✅ Successfully created: {output_file}")
        content_length = len('\n'.join(output_content))
        print(f"📊 Total content length: {content_length:,} characters")
    except Exception as e:
        print(f"❌ Error writing output file: {e}")


def main():
    """Main function."""
    # Get root directory (current directory)
    root_dir = os.getcwd()
    
    # Get output file from command line or use default
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = "all_markdown_content.txt"
    
    print("Markdown Concatenation Script")
    print("=" * 40)
    print(f"Root directory: {root_dir}")
    print(f"Output file: {output_file}")
    print()
    
    # Run concatenation
    concatenate_markdown_files(root_dir, output_file)


if __name__ == "__main__":
    main()
