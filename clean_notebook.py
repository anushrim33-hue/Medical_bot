#!/usr/bin/env python3
"""
Script to clean the Medical_ragbot notebook and convert to accessible formats.
This removes widget metadata that bloats the file and makes it hard to load.
"""

import json
import sys

def clean_notebook(notebook_path):
    """Remove widget metadata from notebook to reduce file size."""
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Remove widgets metadata which is causing the bloat
    if 'metadata' in nb:
        if 'widgets' in nb['metadata']:
            del nb['metadata']['widgets']
            print("✓ Removed widget metadata")
    
    # Clean up cell outputs to remove widget state references
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'code':
            # Keep only essential output info
            clean_outputs = []
            for output in cell.get('outputs', []):
                # Skip widget-related outputs
                if output.get('output_type') != 'display_data':
                    clean_outputs.append(output)
                elif 'application/vnd.jupyter.widget-state+json' not in output.get('data', {}):
                    clean_outputs.append(output)
            cell['outputs'] = clean_outputs
    
    return nb

def save_cleaned_notebook(nb, output_path):
    """Save cleaned notebook."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)
    print(f"✓ Saved cleaned notebook to {output_path}")

def convert_to_html_readme(nb):
    """Create a readable HTML/Markdown version."""
    content = []
    content.append("# Medical RAG Bot Notebook\n")
    
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'markdown':
            content.append(''.join(cell['source']))
            content.append("\n")
        elif cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if source.strip():
                content.append("```python\n")
                content.append(source)
                content.append("\n```\n")
    
    return ''.join(content)

if __name__ == '__main__':
    # Clean the notebook
    print("Cleaning notebook...")
    cleaned_nb = clean_notebook('Medical_ragbot.ipynb')
    
    # Save cleaned version
    save_cleaned_notebook(cleaned_nb, 'Medical_ragbot_cleaned.ipynb')
    
    # Generate markdown version
    print("Generating markdown version...")
    markdown = convert_to_html_readme(cleaned_nb)
    with open('Medical_ragbot_README.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    print("✓ Saved markdown version to Medical_ragbot_README.md")
    
    print("\nDone! You can now:")
    print("1. Open Medical_ragbot_cleaned.ipynb (much smaller file)")
    print("2. View Medical_ragbot_README.md in any browser or text editor")
