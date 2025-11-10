#!/usr/bin/env python3
"""
Generate comprehensive JSON index from GitHub user hartswf0
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

def fetch_all_github_repos(username):
    """Fetch all repositories for a GitHub user"""
    all_repos = []
    page = 1
    
    print(f"🔍 Fetching repositories for {username}...")
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&type=owner&sort=updated"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/vnd.github+json')
            req.add_header('User-Agent', 'Python-GitHub-Index-Generator')
            
            with urllib.request.urlopen(req) as response:
                repos = json.loads(response.read().decode('utf-8'))
                
                if not repos:
                    break
                    
                all_repos.extend(repos)
                print(f"   Fetched page {page}: {len(repos)} repos")
                
                # Check if there are more pages
                link_header = response.headers.get('Link', '')
                if not link_header or 'rel="next"' not in link_header:
                    break
                    
                page += 1
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"❌ User {username} not found")
            else:
                print(f"❌ GitHub API error: {e.code}")
            return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    print(f"✅ Total repositories found: {len(all_repos)}")
    return all_repos

def categorize_repos(repos):
    """Categorize repos by various criteria for ring visualization"""
    
    # Category 1: By language (most common)
    by_language = {}
    for repo in repos:
        lang = repo.get('language') or 'Other'
        if lang not in by_language:
            by_language[lang] = []
        by_language[lang].append(repo)
    
    # Category 2: By activity (last updated)
    now = datetime.now()
    by_activity = {
        'very_recent': [],  # < 30 days
        'recent': [],       # 30-90 days
        'moderate': [],     # 90-180 days
        'older': [],        # 180-365 days
        'archived': []      # > 365 days
    }
    
    for repo in repos:
        if repo.get('archived'):
            by_activity['archived'].append(repo)
            continue
            
        updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        days_ago = (now - updated).days
        
        if days_ago < 30:
            by_activity['very_recent'].append(repo)
        elif days_ago < 90:
            by_activity['recent'].append(repo)
        elif days_ago < 180:
            by_activity['moderate'].append(repo)
        elif days_ago < 365:
            by_activity['older'].append(repo)
        else:
            by_activity['archived'].append(repo)
    
    # Category 3: By size
    by_size = {
        'tiny': [],      # < 100 KB
        'small': [],     # 100KB - 1MB
        'medium': [],    # 1MB - 10MB
        'large': [],     # 10MB - 50MB
        'huge': []       # > 50MB
    }
    
    for repo in repos:
        size_kb = repo.get('size', 0)
        if size_kb < 100:
            by_size['tiny'].append(repo)
        elif size_kb < 1024:
            by_size['small'].append(repo)
        elif size_kb < 10240:
            by_size['medium'].append(repo)
        elif size_kb < 51200:
            by_size['large'].append(repo)
        else:
            by_size['huge'].append(repo)
    
    # Category 4: By stars
    by_stars = {
        'no_stars': [],
        'few_stars': [],    # 1-5
        'some_stars': [],   # 6-20
        'many_stars': [],   # 21-100
        'popular': []       # > 100
    }
    
    for repo in repos:
        stars = repo.get('stargazers_count', 0)
        if stars == 0:
            by_stars['no_stars'].append(repo)
        elif stars <= 5:
            by_stars['few_stars'].append(repo)
        elif stars <= 20:
            by_stars['some_stars'].append(repo)
        elif stars <= 100:
            by_stars['many_stars'].append(repo)
        else:
            by_stars['popular'].append(repo)
    
    return {
        'by_language': by_language,
        'by_activity': by_activity,
        'by_size': by_size,
        'by_stars': by_stars
    }

def generate_ring_structure(repos, categories):
    """Generate concentric ring structure for visualization"""
    
    # Each repo gets assigned to rings based on different criteria
    rings = []
    
    # Ring assignment: activity-based (innermost = most recent)
    ring_order = ['very_recent', 'recent', 'moderate', 'older', 'archived']
    
    for idx, activity_level in enumerate(ring_order):
        repos_in_ring = categories['by_activity'][activity_level]
        
        if not repos_in_ring:
            continue
        
        ring = {
            'ring_id': idx,
            'ring_name': activity_level.replace('_', ' ').title(),
            'radius_start': idx * 50 + 100,
            'radius_end': (idx + 1) * 50 + 100,
            'color': ['#ff6b35', '#f7931e', '#fdc500', '#c1d82f', '#8ac926'][idx],
            'repo_count': len(repos_in_ring),
            'repos': [
                {
                    'name': r['name'],
                    'full_name': r['full_name'],
                    'description': r['description'],
                    'language': r.get('language'),
                    'stars': r['stargazers_count'],
                    'forks': r['forks_count'],
                    'size_kb': r['size'],
                    'updated_at': r['updated_at'],
                    'created_at': r['created_at'],
                    'html_url': r['html_url'],
                    'homepage': r.get('homepage'),
                    'has_pages': r.get('has_pages', False),
                    'is_fork': r.get('fork', False),
                    'archived': r.get('archived', False),
                    'topics': r.get('topics', [])
                }
                for r in repos_in_ring
            ]
        }
        rings.append(ring)
    
    return rings

def generate_comprehensive_index(username):
    """Generate complete GitHub index"""
    
    repos = fetch_all_github_repos(username)
    
    if not repos:
        return None
    
    categories = categorize_repos(repos)
    rings = generate_ring_structure(repos, categories)
    
    # Generate comprehensive index
    index = {
        'meta': {
            'generated': datetime.now().isoformat(),
            'github_user': username,
            'total_repos': len(repos),
            'api_version': 'v3',
            'visualization': 'concentric_rings'
        },
        'summary': {
            'total_repos': len(repos),
            'total_stars': sum(r.get('stargazers_count', 0) for r in repos),
            'total_forks': sum(r.get('forks_count', 0) for r in repos),
            'total_size_mb': round(sum(r.get('size', 0) for r in repos) / 1024, 2),
            'languages': {
                lang: len(repos_list) 
                for lang, repos_list in categories['by_language'].items()
            },
            'has_pages_count': sum(1 for r in repos if r.get('has_pages')),
            'archived_count': sum(1 for r in repos if r.get('archived')),
            'fork_count': sum(1 for r in repos if r.get('fork'))
        },
        'rings': rings,
        'categories': {
            'by_language': {
                lang: len(repos_list)
                for lang, repos_list in categories['by_language'].items()
            },
            'by_activity': {
                level: len(repos_list)
                for level, repos_list in categories['by_activity'].items()
            },
            'by_size': {
                size: len(repos_list)
                for size, repos_list in categories['by_size'].items()
            },
            'by_stars': {
                level: len(repos_list)
                for level, repos_list in categories['by_stars'].items()
            }
        },
        'all_repos': [
            {
                'name': r['name'],
                'full_name': r['full_name'],
                'description': r['description'],
                'language': r.get('language'),
                'stars': r['stargazers_count'],
                'forks': r['forks_count'],
                'size_kb': r['size'],
                'updated_at': r['updated_at'],
                'created_at': r['created_at'],
                'html_url': r['html_url'],
                'homepage': r.get('homepage'),
                'has_pages': r.get('has_pages', False),
                'topics': r.get('topics', [])
            }
            for r in repos
        ]
    }
    
    return index

if __name__ == '__main__':
    username = 'hartswf0'
    
    index = generate_comprehensive_index(username)
    
    if index:
        output_file = Path(__file__).parent / 'github-ripple-index.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Index generated: {output_file}")
        print(f"\n📊 Summary:")
        print(f"   Total repos: {index['summary']['total_repos']}")
        print(f"   Total stars: {index['summary']['total_stars']}")
        print(f"   Total size: {index['summary']['total_size_mb']} MB")
        print(f"   Rings created: {len(index['rings'])}")
        print(f"\n🌳 Tree Rings:")
        for ring in index['rings']:
            print(f"   Ring {ring['ring_id']}: {ring['ring_name']} - {ring['repo_count']} repos")
        print(f"\n🎨 Languages:")
        for lang, count in sorted(index['summary']['languages'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {lang}: {count}")
    else:
        print("❌ Failed to generate index")
