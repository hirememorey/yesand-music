#!/bin/bash
# Quick script to update the concatenated markdown file
# Usage: ./update_markdown.sh [output_file]

echo "🔄 Updating all_markdown_content.txt..."
python3 concatenate_markdown.py "$@"
echo "✅ Done!"
