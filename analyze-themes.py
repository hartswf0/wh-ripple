#!/usr/bin/env python3
"""
Analyze GitHub repos and cluster them into thematic patterns
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    if not text:
        return []
    
    # Convert to lowercase
    text = text.lower()
    
    # Common meaningful words in this corpus
    keywords = []
    
    # Media theory terms
    media_terms = ['media', 'mcluhan', 'tetrad', 'cage', 'narrative', 'cinema', 'film', 'video', 'audio', 'sound']
    # AI/ML terms
    ai_terms = ['ai', 'llm', 'gpt', 'agent', 'chatbot', 'machine learning', 'neural', 'model']
    # Philosophy terms
    phil_terms = ['plato', 'myth', 'ethics', 'philosophy', 'theory', 'reality', 'truth']
    # Technical terms
    tech_terms = ['three.js', '3d', 'vr', 'webgl', 'canvas', 'interactive', 'visualization']
    # Temporal terms
    time_terms = ['time', 'temporal', 'archive', 'memory', 'history']
    # Design terms
    design_terms = ['interface', 'ui', 'design', 'bauhaus', 'interactive']
    
    all_terms = media_terms + ai_terms + phil_terms + tech_terms + time_terms + design_terms
    
    for term in all_terms:
        if term in text:
            keywords.append(term)
    
    return list(set(keywords))

def analyze_themes(repos):
    """Cluster repos into thematic groups"""
    
    themes = {
        'media_theory': {
            'name': 'Media Theory & McLuhan',
            'keywords': ['media', 'mcluhan', 'tetrad', 'cage', 'sapir', 'myth', 'reality media'],
            'repos': []
        },
        'ai_systems': {
            'name': 'AI Systems & Agents',
            'keywords': ['ai', 'llm', 'gpt', 'agent', 'chatbot', 'neural', 'machine', 'model'],
            'repos': []
        },
        'platos_cave': {
            'name': "Plato's Cave & Philosophy",
            'keywords': ['plato', 'cave', 'reality', 'shadow', 'philosophy'],
            'repos': []
        },
        'narrative_tools': {
            'name': 'Narrative & Storytelling',
            'keywords': ['narrative', 'story', 'legos', 'myth', 'cinema', 'film'],
            'repos': []
        },
        'three_d_viz': {
            'name': '3D Visualization & WebGL',
            'keywords': ['three.js', '3d', 'webgl', 'vr', 'a-frame', 'visualization'],
            'repos': []
        },
        'temporal_systems': {
            'name': 'Time & Memory',
            'keywords': ['time', 'temporal', 'archive', 'memory', 'history', 'timeline'],
            'repos': []
        },
        'interactive_media': {
            'name': 'Interactive Experiences',
            'keywords': ['interactive', 'game', 'interface', 'ui', 'canvas'],
            'repos': []
        },
        'archives': {
            'name': 'Archives & Collections',
            'keywords': ['archive', 'collection', 'arkadu', 'xanadu', 'library', 'codex'],
            'repos': []
        },
        'sound_audio': {
            'name': 'Sound & Audio',
            'keywords': ['sound', 'audio', 'music', 'listening', 'waveform', 'tts'],
            'repos': []
        },
        'educational': {
            'name': 'Educational Tools',
            'keywords': ['teaching', 'learning', 'education', 'course', 'classroom', 'student'],
            'repos': []
        }
    }
    
    # Classify each repo
    for repo in repos:
        text = f"{repo['name']} {repo['description'] or ''} {' '.join(repo.get('topics', []))}"
        text = text.lower()
        
        matched_themes = []
        
        for theme_id, theme in themes.items():
            score = 0
            for keyword in theme['keywords']:
                if keyword in text:
                    score += 1
            
            if score > 0:
                matched_themes.append((theme_id, score))
        
        # Assign to best matching theme(s)
        if matched_themes:
            matched_themes.sort(key=lambda x: x[1], reverse=True)
            primary_theme = matched_themes[0][0]
            themes[primary_theme]['repos'].append(repo)
        else:
            # Uncategorized
            if 'other' not in themes:
                themes['other'] = {
                    'name': 'Other Projects',
                    'keywords': [],
                    'repos': []
                }
            themes['other']['repos'].append(repo)
    
    # Remove empty themes
    themes = {k: v for k, v in themes.items() if v['repos']}
    
    return themes

def create_enhanced_index(input_file):
    """Create enhanced thematic index"""
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    repos = data['all_repos']
    themes = analyze_themes(repos)
    
    # Create enhanced structure
    enhanced = {
        'meta': data['meta'],
        'summary': data['summary'],
        'themes': {}
    }
    
    # Convert themes to ring structure
    theme_rings = []
    for idx, (theme_id, theme_data) in enumerate(sorted(themes.items(), key=lambda x: len(x[1]['repos']), reverse=True)):
        ring = {
            'ring_id': idx,
            'theme_name': theme_data['name'],
            'theme_id': theme_id,
            'keywords': theme_data['keywords'],
            'repo_count': len(theme_data['repos']),
            'radius_start': idx * 60 + 120,
            'radius_end': (idx + 1) * 60 + 120,
            'color': [
                '#ff6b35', '#f7931e', '#fdc500', '#c1d82f', '#8ac926',
                '#52b788', '#36a9e1', '#5390d9', '#9b59b6', '#e74c3c'
            ][idx % 10],
            'repos': theme_data['repos']
        }
        theme_rings.append(ring)
    
    enhanced['theme_rings'] = theme_rings
    
    # Add co-occurrence matrix
    cooccurrence = defaultdict(lambda: defaultdict(int))
    for repo in repos:
        text = f"{repo['name']} {repo['description'] or ''}"
        keywords = extract_keywords(text)
        for i, k1 in enumerate(keywords):
            for k2 in keywords[i+1:]:
                cooccurrence[k1][k2] += 1
                cooccurrence[k2][k1] += 1
    
    enhanced['keyword_network'] = {
        k: dict(v) for k, v in cooccurrence.items()
    }
    
    # Theme summary
    enhanced['theme_summary'] = {
        'total_themes': len(theme_rings),
        'largest_theme': max(theme_rings, key=lambda x: x['repo_count'])['theme_name'],
        'theme_distribution': {
            r['theme_name']: r['repo_count'] 
            for r in theme_rings
        }
    }
    
    return enhanced

if __name__ == '__main__':
    input_file = Path(__file__).parent / 'github-ripple-index.json'
    output_file = Path(__file__).parent / 'github-thematic-index.json'
    
    print("📊 Analyzing themes...")
    enhanced = create_enhanced_index(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Thematic analysis complete: {output_file}")
    print(f"\n🎨 Themes identified: {enhanced['theme_summary']['total_themes']}")
    print(f"📈 Largest theme: {enhanced['theme_summary']['largest_theme']}")
    print(f"\n📊 Theme Distribution:")
    for theme, count in sorted(enhanced['theme_summary']['theme_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {theme}: {count} repos")
