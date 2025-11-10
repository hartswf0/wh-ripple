#!/usr/bin/env python3
"""
Generate detailed sitemap with metadata extracted from HTML files
"""

import json
import os
import re
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime

class HTMLMetadataExtractor(HTMLParser):
    """Extract metadata from HTML files"""
    
    def __init__(self):
        super().__init__()
        self.title = None
        self.meta_description = None
        self.meta_tags = {}
        self.scripts = []
        self.stylesheets = []
        self.h1_tags = []
        self.in_title = False
        self.in_script = False
        self.script_content = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = attrs_dict.get('name', '').lower()
            content = attrs_dict.get('content', '')
            if name == 'description':
                self.meta_description = content
            elif name:
                self.meta_tags[name] = content
        elif tag == 'script':
            self.in_script = True
            src = attrs_dict.get('src', '')
            if src:
                self.scripts.append(src)
        elif tag == 'link':
            rel = attrs_dict.get('rel', '')
            href = attrs_dict.get('href', '')
            if 'stylesheet' in rel and href:
                self.stylesheets.append(href)
        elif tag == 'h1':
            # Will capture text in handle_data
            pass
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
        elif self.in_script:
            self.script_content += data
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'script':
            self.in_script = False
            self.script_content = ""

def extract_html_metadata(file_path):
    """Extract metadata from an HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        parser = HTMLMetadataExtractor()
        parser.feed(content)
        
        # Additional analysis
        features = []
        
        # Check for common frameworks/libraries
        if 'three.js' in content.lower() or 'three.min.js' in content.lower():
            features.append('Three.js 3D')
        if 'tone.js' in content.lower():
            features.append('Tone.js Audio')
        if 'github api' in content.lower() or 'api.github.com' in content.lower():
            features.append('GitHub API')
        if 'playlist' in content.lower():
            features.append('Playlist System')
        if 'export' in content.lower() and ('json' in content.lower() or 'csv' in content.lower()):
            features.append('Export Functionality')
        if 'bauhaus' in content.lower():
            features.append('Bauhaus Design')
        if 'grid' in content.lower() and 'cell' in content.lower():
            features.append('Grid System')
        if 'canvas' in content.lower():
            features.append('Canvas Rendering')
        if 'observer' in content.lower() and 'system' in content.lower():
            features.append('Observer Pattern')
        
        # Count elements
        function_count = len(re.findall(r'\bfunction\s+\w+', content))
        const_count = len(re.findall(r'\bconst\s+\w+', content))
        let_count = len(re.findall(r'\blet\s+\w+', content))
        
        return {
            'title': parser.title,
            'description': parser.meta_description,
            'meta_tags': parser.meta_tags,
            'external_scripts': parser.scripts,
            'external_stylesheets': parser.stylesheets,
            'features': features,
            'stats': {
                'functions': function_count,
                'constants': const_count,
                'variables': let_count,
                'lines': len(content.splitlines())
            }
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def generate_detailed_sitemap():
    """Generate detailed sitemap with metadata"""
    
    root = Path('/Users/gaia/WH_RIPPLE')
    html_files = sorted(root.glob('*.html'))
    
    sitemap = {
        'project': 'WH_RIPPLE Repository Index',
        'generated': datetime.now().isoformat(),
        'root_path': str(root),
        'repository': 'hartswf0/potters-wheel',
        'pages': []
    }
    
    for html_file in html_files:
        print(f"Processing {html_file.name}...")
        
        metadata = extract_html_metadata(html_file)
        if not metadata:
            continue
        
        page_info = {
            'filename': html_file.name,
            'path': str(html_file.relative_to(root)),
            'url': f"file://{html_file}",
            'size_bytes': html_file.stat().st_size,
            'size_kb': round(html_file.stat().st_size / 1024, 2),
            'modified': datetime.fromtimestamp(html_file.stat().st_mtime).isoformat(),
            'title': metadata['title'],
            'description': metadata['description'],
            'features': metadata['features'],
            'stats': metadata['stats'],
            'external_scripts': metadata['external_scripts'],
            'external_stylesheets': metadata['external_stylesheets']
        }
        
        sitemap['pages'].append(page_info)
    
    # Add summary statistics
    sitemap['summary'] = {
        'total_pages': len(sitemap['pages']),
        'total_size_kb': sum(p['size_kb'] for p in sitemap['pages']),
        'total_size_mb': round(sum(p['size_kb'] for p in sitemap['pages']) / 1024, 2),
        'avg_page_size_kb': round(sum(p['size_kb'] for p in sitemap['pages']) / len(sitemap['pages']), 2) if sitemap['pages'] else 0,
        'total_functions': sum(p['stats']['functions'] for p in sitemap['pages']),
        'total_lines': sum(p['stats']['lines'] for p in sitemap['pages']),
        'all_features': sorted(list(set(feat for p in sitemap['pages'] for feat in p['features'])))
    }
    
    # Group by category
    sitemap['categories'] = {
        'github_indices': [p for p in sitemap['pages'] if 'github' in p['filename'].lower()],
        'kimi_lego': [p for p in sitemap['pages'] if 'kimi' in p['filename'].lower() or 'lego' in p['filename'].lower()],
        'presentations': [p for p in sitemap['pages'] if 'presentation' in p['filename'].lower() or 'mythos' in p['filename'].lower()],
        'wh_pages': [p for p in sitemap['pages'] if p['filename'].startswith('wh') and p['filename'][2].isdigit()]
    }
    
    # Save sitemap
    output_file = root / 'sitemap-detailed.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sitemap, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Detailed sitemap generated: {output_file}")
    print(f"📊 Total pages: {sitemap['summary']['total_pages']}")
    print(f"💾 Total size: {sitemap['summary']['total_size_mb']} MB")
    print(f"🔧 Total functions: {sitemap['summary']['total_functions']}")
    print(f"📝 Total lines: {sitemap['summary']['total_lines']:,}")
    print(f"\n🎨 Features found:")
    for feat in sitemap['summary']['all_features']:
        print(f"  - {feat}")

if __name__ == '__main__':
    generate_detailed_sitemap()
