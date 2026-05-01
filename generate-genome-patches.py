#!/usr/bin/env python3
"""
REPO GENOME SCANNER v2
ONE REPO = ONE TIMELINE PATCH. PROGRAM THEORY CAPSULES ACTIVE.

Generates genome patches for all repos created in the past year.
Each patch encodes:
  1. Timeline Genome — when it appears in the year
  2. Artifact Genome — what the repo visibly is
  3. Program Theory Genome — what theory-of-the-program it performs
  4. Creator Trail Genome — what trail of making it preserves or implies
"""

import json
import re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# === CONFIGURATION ===
USERNAME = 'hartswf0'
YEAR_START = datetime(2025, 5, 1)
YEAR_END = datetime(2026, 5, 1)

# === THEME PRIORITY (from analyze-themes.py) ===
THEME_PRIORITY = {
    'media_theory': 'Media Theory & McLuhan',
    'ai_systems': 'AI Systems & Agents',
    'interactive_media': 'Interactive Experiences',
    'platos_cave': "Plato's Cave & Philosophy",
    'narrative_tools': 'Narrative & Storytelling',
    'temporal_systems': 'Time & Memory',
    'sound_audio': 'Sound & Audio',
    'three_d_viz': '3D Visualization & WebGL',
    'educational': 'Educational Tools',
    'archives': 'Archives & Collections',
    'other': 'Other Projects'
}

# === QUARTERLY PHASES ===
def get_phase(created_dt):
    if created_dt < datetime(2025, 8, 1):
        return {"quarter": "Q2-2025", "phase": "SEEDING", "phase_desc": "Planting biological metaphors, early probes"}
    elif created_dt < datetime(2025, 11, 1):
        return {"quarter": "Q3-2025", "phase": "ERUPTION", "phase_desc": "Massive outpouring across all themes"}
    elif created_dt < datetime(2026, 2, 1):
        return {"quarter": "Q4-2025", "phase": "CONSOLIDATION", "phase_desc": "Building infrastructure, shield project crystallizes"}
    else:
        return {"quarter": "Q1-2026", "phase": "OPERATIONALIZATION", "phase_desc": "Description becomes construction"}

# === MATURITY CLASSIFIER ===
def classify_maturity(repo, lifespan_days, size_mb, commits=None):
    """Classify maturity stage: seed | sketch | prototype | instrument | infrastructure"""
    c = commits or 1
    if size_mb < 0.05 and lifespan_days < 2:
        return "seed"
    elif lifespan_days < 3 and size_mb < 5:
        return "sketch"
    elif lifespan_days < 15 or (c < 10 and size_mb < 20):
        return "prototype"
    elif lifespan_days >= 30 or c >= 20 or size_mb >= 50:
        return "instrument"
    else:
        return "prototype"

# === CONSTELLATION CLASSIFIER ===
CONSTELLATIONS = {
    'media': {
        'name': 'Media Constellation',
        'terms': ['media', 'mcluhan', 'tetrad', 'medium', 'ecology', 'surfer', 'shaper'],
    },
    'machine': {
        'name': 'Machine Constellation',
        'terms': ['machine', 'automata', 'engine', 'grid', 'compute', 'algorithm', 'agent'],
    },
    'cave': {
        'name': 'Cave Constellation',
        'terms': ['cave', 'plato', 'shadow', 'republic', 'reality', 'photon'],
    },
    'prompt': {
        'name': 'Prompt/Operative Constellation',
        'terms': ['prompt', 'operative', 'ekphrasis', 'describe', 'shield', 'operator'],
    },
    'myth': {
        'name': 'Myth/Narrative Constellation',
        'terms': ['myth', 'narrative', 'story', 'hephaestus', 'legos', 'metisim'],
    },
    'temporal': {
        'name': 'Temporal Constellation',
        'terms': ['time', 'memory', 'archive', 'temporal', 'bridge', 'ancient', 'history'],
    },
    'genetic': {
        'name': 'Genetic Constellation',
        'terms': ['gene', 'codon', 'intron', 'genome', 'dna', 'genetic', 'evolution'],
    },
    'ethics': {
        'name': 'Ethics Constellation',
        'terms': ['ethics', 'disclosure', 'privacy', 'kayfabe', 'surveillance', 'consent'],
    },
    'sound': {
        'name': 'Sound Constellation',
        'terms': ['sound', 'audio', 'music', 'tts', 'groove', 'listen', 'waveform', 'sonic'],
    },
    'ritual': {
        'name': 'Ritual Constellation',
        'terms': ['ritual', 'ceremony', 'nothing', 'sense', 'soul', 'spirit'],
    },
}

def find_constellations(repo):
    text = f"{repo['name']} {repo.get('description') or ''}".lower()
    matches = []
    for cid, cdata in CONSTELLATIONS.items():
        score = sum(1 for t in cdata['terms'] if t in text)
        if score > 0:
            matches.append((cdata['name'], score))
    matches.sort(key=lambda x: -x[1])
    return [m[0] for m in matches]

# === VOCABULARY EXTRACTION ===
def extract_vocabulary(repo):
    text = f"{repo['name']} {repo.get('description') or ''}"
    text_lower = text.lower()
    
    # Entities (nouns/concepts)
    entity_terms = [
        'media', 'machine', 'agent', 'cave', 'grid', 'shield', 'myth',
        'narrative', 'prompt', 'soul', 'ritual', 'archive', 'memory',
        'ecology', 'interface', 'code', 'time', 'space', 'culture',
        'ethics', 'reality', 'world', 'sound', 'text', 'image',
        'film', 'operator', 'engine', 'system', 'tool', 'language',
        'pattern', 'structure', 'bridge', 'island', 'ocean', 'dust',
        'gene', 'dna', 'cell', 'wave', 'field', 'vibe', 'canvas',
        'stone', 'mason', 'fork', 'seed', 'loom', 'thread',
        'attention', 'feed', 'disclosure', 'surveillance'
    ]
    entities = [t for t in entity_terms if t in text_lower]
    
    # Morphisms (verbs/transformations)
    morphism_terms = [
        'transforms', 'shapes', 'encodes', 'decodes', 'maps', 'builds',
        'describes', 'assembles', 'generates', 'navigates', 'explores',
        'tracks', 'forages', 'observes', 'infers', 'suggests',
        'creates', 'destroys', 'remembers', 'forgets', 'evolves',
        'adapts', 'learns', 'discovers', 'reveals', 'hides',
        'organizes', 'connects', 'bridges', 'fuses', 'splits',
        'making', 'thinking', 'operating', 'describing', 'building',
        'scripting', 'programming', 'rendering', 'visualizing'
    ]
    morphisms = [t for t in morphism_terms if t in text_lower]
    
    # Groups (collections/structures)
    group_terms = [
        'system', 'collection', 'archive', 'network', 'ecology',
        'constellation', 'toolkit', 'suite', 'framework', 'engine',
        'infrastructure', 'platform', 'gallery', 'deck', 'stack',
        'field', 'garden', 'mansion', 'town', 'republic', 'empire'
    ]
    groups = [t for t in group_terms if t in text_lower]
    
    return {
        'key_entities': entities[:8],
        'key_morphisms': morphisms[:6],
        'key_groups': groups[:4],
        'coined_terms': [],  # Would need deep inspection
        'conceptual_anchors': (entities[:3] if entities else [repo['name'].split('-')[0]])
    }

# === PROGRAM THEORY EXTRACTION ===
def extract_program_theory(repo, theme, constellations):
    desc = repo.get('description') or ''
    name = repo['name']
    lang = repo.get('language') or 'HTML'
    has_pages = repo.get('has_pages', False)
    
    # Initial interpretation
    if desc:
        problem = desc[:120]
    else:
        problem = f"Repository '{name}' — purpose inferred from name only"
    
    # Infer what the repo is a tool for
    tool_for = "unknown"
    desc_lower = (desc or '').lower()
    name_lower = name.lower()
    
    if any(t in desc_lower for t in ['interactive', 'interface', 'canvas', 'game', 'explore']):
        tool_for = "interactive exploration"
    elif any(t in desc_lower for t in ['visualization', 'visualiz', 'map', 'chart', 'graph']):
        tool_for = "visualization and mapping"
    elif any(t in desc_lower for t in ['simulation', 'model', 'agent', 'abm']):
        tool_for = "simulation and modeling"
    elif any(t in desc_lower for t in ['archive', 'collection', 'index', 'catalog']):
        tool_for = "archiving and retrieval"
    elif any(t in desc_lower for t in ['audio', 'sound', 'music', 'dj', 'mix']):
        tool_for = "sound design and audio exploration"
    elif any(t in desc_lower for t in ['theory', 'framework', 'concept', 'research']):
        tool_for = "theoretical framework demonstration"
    elif any(t in desc_lower for t in ['tool', 'editor', 'builder', 'maker']):
        tool_for = "creative tool / builder"
    elif any(t in desc_lower for t in ['presentation', 'essay', 'article', 'argument']):
        tool_for = "argumentative presentation"
    elif has_pages:
        tool_for = "web-based interactive artifact"
    
    # Evidence confidence
    if desc and len(desc) > 30:
        confidence = "strongly_inferred"
    elif desc:
        confidence = "weakly_inferred"
    else:
        confidence = "name_only"
    
    # Basic entities/operations from description
    theory_entities = []
    theory_operations = []
    if desc:
        # Extract noun-like patterns
        words = re.findall(r'[A-Z][a-z]+|[a-z]{4,}', desc)
        theory_entities = list(set(words[:6]))
        # Common verbs
        for verb in ['creates', 'builds', 'maps', 'transforms', 'explores', 'generates',
                      'decodes', 'encodes', 'navigates', 'tracks', 'reveals', 'connects',
                      'simulates', 'assembles', 'scripts', 'programs']:
            if verb in desc_lower:
                theory_operations.append(f"[{verb}]")
    
    return {
        'initial_interpretation': {
            'program_theory_problem': problem,
            'real_world_activity': tool_for,
            'repo_as_tool_for': tool_for,
        },
        'theory_skeleton': {
            'entities': [f"<{e}>" for e in theory_entities[:5]] or [f"<{name}>"],
            'operations': theory_operations[:4] or ["[renders]", "[displays]"],
        },
        'evidence': {
            'scan_level': 'metadata_only',
            'confidence': confidence,
            'evidence_sources': ['repo metadata', 'description text', 'language tag', 'pages status'],
        }
    }

# === CREATOR TRAIL ===
def extract_creator_trail(repo, lifespan_days, size_mb, commits=None):
    c = commits or 0
    
    # Trail maturity
    if c > 20 or lifespan_days > 30:
        trail_maturity = 1  # TRAIL_AS_FEATURE
        trail_maturity_label = "TRAIL_AS_FEATURE"
    elif c > 5 or lifespan_days > 7:
        trail_maturity = 0  # TRAIL_AS_INVISIBLE_EXHAUST
        trail_maturity_label = "TRAIL_AS_INVISIBLE_EXHAUST"
    else:
        trail_maturity = 0
        trail_maturity_label = "TRAIL_AS_INVISIBLE_EXHAUST"
    
    # Process metadata
    process = {
        'created_at': repo['created_at'],
        'updated_at': repo['updated_at'],
        'lifespan_days': lifespan_days,
        'size_mb': round(size_mb, 2),
        'commits': c if c > 0 else "unknown",
        'language': repo.get('language') or 'unspecified',
        'has_pages': repo.get('has_pages', False),
        'deployment_status': 'deployed' if repo.get('has_pages') else 'source_only',
    }
    
    # Infer making pattern
    if lifespan_days == 0 and size_mb > 10:
        making_pattern = "single_session_dump"
        making_notes = "Large repo created and not updated — likely a single-session build or import"
    elif lifespan_days == 0:
        making_pattern = "flash_sketch"
        making_notes = "Created and deployed in one session"
    elif lifespan_days < 7:
        making_pattern = "sprint"
        making_notes = f"Active for {lifespan_days} days — short focused sprint"
    elif lifespan_days < 30:
        making_pattern = "project"
        making_notes = f"Active over {lifespan_days} days — multi-session project"
    else:
        making_pattern = "sustained_practice"
        making_notes = f"Active over {lifespan_days} days — sustained, evolving practice"
    
    return {
        'trail_maturity': trail_maturity,
        'trail_maturity_label': trail_maturity_label,
        'process_metadata': process,
        'making_pattern': making_pattern,
        'making_notes': making_notes,
        'trail_ethics': {
            'supports_observing': True,
            'supports_inferring': repo.get('has_pages', False),
            'supports_creator_control': True,
            'risks_caging': False,
            'risks_surveilling': False,
        }
    }

# === LINEAGE DETECTION ===
def detect_lineage(repo, all_repos):
    name = repo['name'].lower()
    desc = (repo.get('description') or '').lower()
    name_parts = set(re.findall(r'[a-z]{3,}', name))
    
    siblings = []
    parents = []
    descendants = []
    
    for other in all_repos:
        if other['name'] == repo['name']:
            continue
        
        other_name = other['name'].lower()
        other_parts = set(re.findall(r'[a-z]{3,}', other_name))
        other_desc = (other.get('description') or '').lower()
        
        # Shared name components (excluding trivial)
        shared = name_parts & other_parts - {'the', 'and', 'for', 'with', 'html'}
        
        if shared and len(shared) > 0:
            other_created = datetime.strptime(other['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            repo_created = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            
            if other_created < repo_created:
                parents.append(other['name'])
            elif other_created > repo_created:
                descendants.append(other['name'])
            else:
                siblings.append(other['name'])
    
    return {
        'parent_repos': parents[:5],
        'sibling_repos': siblings[:5],
        'descendant_repos': descendants[:5],
    }

# === MAIN PIPELINE ===
def generate_all_patches():
    print("REPO GENOME SCANNER v2 ONLINE. ONE REPO = ONE TIMELINE PATCH. PROGRAM THEORY CAPSULES ACTIVE.")
    print()
    
    # Load data
    with open('github-ripple-index.json') as f:
        ripple_data = json.load(f)
    with open('github-thematic-index.json') as f:
        thematic_data = json.load(f)
    
    all_repos = ripple_data['all_repos']
    
    # Build theme lookup
    theme_lookup = {}
    theme_color_lookup = {}
    for ring in thematic_data['theme_rings']:
        for r in ring['repos']:
            theme_lookup[r['name']] = ring['theme_name']
            theme_color_lookup[r['name']] = ring['color']
    
    # Filter to past year
    year_repos = []
    for r in all_repos:
        created = datetime.strptime(r['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if YEAR_START <= created < YEAR_END:
            year_repos.append(r)
    
    # Sort by creation date
    year_repos.sort(key=lambda r: r['created_at'])
    
    print(f"Processing {len(year_repos)} repos from past year...")
    print()
    
    # Commit counts for top repos (pre-fetched)
    commit_counts = {
        'moto': 46, 'sense-ritual': 32, 'k2.html': 49,
        'tractor-dce-gyo': 61, 'opek': 1, 'ripples': 28,
        'human-as-media': 3, 'tractor-field-notes': 20,
        'dust-empire': 3, 'core-age': 60, 'alien-child': 1,
        'hyperclay-editor': 43, 'abc-flix': 23, 'meets': 8,
        'potters-wheel': 9,
    }
    
    patches = []
    
    for idx, repo in enumerate(year_repos):
        created = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        lifespan = (updated - created).days
        size_mb = repo['size_kb'] / 1024
        commits = commit_counts.get(repo['name'], 0)
        
        phase_info = get_phase(created)
        theme = theme_lookup.get(repo['name'], 'Other Projects')
        theme_color = theme_color_lookup.get(repo['name'], '#ff6b35')
        constellations = find_constellations(repo)
        maturity = classify_maturity(repo, lifespan, size_mb, commits)
        vocab = extract_vocabulary(repo)
        theory = extract_program_theory(repo, theme, constellations)
        trail = extract_creator_trail(repo, lifespan, size_mb, commits)
        lineage = detect_lineage(repo, year_repos)
        
        patch = {
            'patch_id': f"P-{idx+1:03d}",
            'repo_name': repo['name'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
            'month': created.strftime('%Y-%m'),
            'quarter': phase_info['quarter'],
            'phase': phase_info['phase'],
            'phase_desc': phase_info['phase_desc'],
            
            'timeline_genome': {
                'timeline_title': repo['name'],
                'one_line_summary': (repo.get('description') or f"Repository: {repo['name']}")[:120],
                'yearly_arc': phase_info['phase'],
                'local_cluster': f"{created.strftime('%b %Y')} cluster",
                'constellation': constellations[0] if constellations else 'Uncharted',
                'all_constellations': constellations,
                'maturity_stage': maturity,
                'theme': theme,
                'theme_color': theme_color,
            },
            
            'artifact_genome': {
                'artifact_type': 'web_application' if repo.get('has_pages') else 'source_repository',
                'primary_language': repo.get('language') or 'unspecified',
                'deployment_shape': 'github_pages' if repo.get('has_pages') else 'source_only',
                'has_pages': repo.get('has_pages', False),
                'pages_url': f"https://hartswf0.github.io/{repo['name']}/" if repo.get('has_pages') else None,
                'github_url': repo.get('html_url', ''),
                'size_mb': round(size_mb, 2),
                'stars': repo.get('stars', 0),
                'forks': repo.get('forks', 0),
            },
            
            'vocabulary_genome': vocab,
            
            'program_theory_capsule': theory,
            
            'creator_trail_genome': trail,
            
            'lineage_genome': lineage,
            
            'timeline_ui_card': {
                'card_title': repo['name'],
                'card_subtitle': (repo.get('description') or '')[:80],
                'badges': [
                    maturity,
                    phase_info['phase'].lower(),
                    theme.split(' ')[0].lower(),
                ] + (['pages'] if repo.get('has_pages') else []),
                'hover_summary': f"{repo['name']} — {maturity} — {theme} — {created.strftime('%b %d, %Y')}",
                'filters': [
                    theme,
                    phase_info['phase'],
                    maturity,
                    phase_info['quarter'],
                ] + constellations[:2],
            },
        }
        
        patches.append(patch)
    
    # Aggregate stats
    constellation_counts = defaultdict(int)
    phase_counts = defaultdict(int)
    maturity_counts = defaultdict(int)
    theme_counts = defaultdict(int)
    
    for p in patches:
        for c in p['timeline_genome']['all_constellations']:
            constellation_counts[c] += 1
        phase_counts[p['phase']] += 1
        maturity_counts[p['timeline_genome']['maturity_stage']] += 1
        theme_counts[p['timeline_genome']['theme']] += 1
    
    output = {
        'meta': {
            'generated': datetime.now().isoformat(),
            'scanner_version': '2.0',
            'mode': 'year-in-review-repo-forensics',
            'patch_unit': 'one_repo',
            'total_patches': len(patches),
            'year_range': f"{YEAR_START.strftime('%Y-%m-%d')} to {YEAR_END.strftime('%Y-%m-%d')}",
        },
        'summary': {
            'total_repos': len(patches),
            'constellation_counts': dict(constellation_counts),
            'phase_counts': dict(phase_counts),
            'maturity_counts': dict(maturity_counts),
            'theme_counts': dict(theme_counts),
        },
        'patches': patches,
    }
    
    return output

if __name__ == '__main__':
    output = generate_all_patches()
    
    out_file = Path(__file__).parent / 'genome-patches.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nGenerated {output['meta']['total_patches']} genome patches → {out_file}")
    print(f"\nPhase distribution:")
    for phase, count in sorted(output['summary']['phase_counts'].items()):
        print(f"  {phase}: {count}")
    print(f"\nMaturity distribution:")
    for mat, count in sorted(output['summary']['maturity_counts'].items()):
        print(f"  {mat}: {count}")
    print(f"\nConstellation distribution:")
    for const, count in sorted(output['summary']['constellation_counts'].items(), key=lambda x: -x[1]):
        print(f"  {const}: {count}")
