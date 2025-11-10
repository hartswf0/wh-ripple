# GitHub Repository Index System

## 📊 Overview

Complete system for indexing, analyzing, and visualizing all 245 repositories from @hartswf0's GitHub account.

## 🎯 What's Available

### 1. **Data Generation Scripts**

#### `generate-github-index.py`
- Fetches all repos from GitHub API
- Organizes by activity (time-based rings)
- Generates: `github-ripple-index.json`

#### `analyze-themes.py` ⭐ RECOMMENDED
- Analyzes repos by theme/topic
- Uses keyword extraction and clustering
- Generates: `github-thematic-index.json`
- **11 thematic clusters identified**:
  - AI Systems & Agents (61 repos)
  - Media Theory & McLuhan (27 repos)
  - Time & Memory (16 repos)
  - Interactive Experiences (12 repos)
  - Sound & Audio (9 repos)
  - Plato's Cave & Philosophy (7 repos)
  - Narrative & Storytelling (7 repos)
  - 3D Visualization & WebGL (7 repos)
  - Educational Tools (5 repos)
  - Archives & Collections (2 repos)
  - Other Projects (92 repos)

### 2. **Visualization Viewers**

#### `thematic-rings-viewer.html` ⭐ BEST
- **Fully functional and tested**
- Loads: `github-thematic-index.json`
- Shows repos organized by **theme** (not just time)
- 11 concentric rings, one per theme
- Interactive: hover, click, drag to rotate
- Legend shows all themes
- **This is the one that works!**

#### `ripple-rings-viewer.html` 
- **FIXED! Now working**
- Same as thematic-rings but different styling
- Also loads thematic data
- Time-based alternative view

### 3. **JSON Data Files**

#### `github-ripple-index.json`
- Time-based organization
- 5 rings by recency
- Structure: `data.rings[]`

#### `github-thematic-index.json` ⭐ 
- Theme-based organization
- 11 rings by topic
- Structure: `data.theme_rings[]`
- Includes keyword analysis
- Co-occurrence matrix

#### `sitemap-index.json`
- Simple local file listing
- Basic categorization
- Good for quick reference

### 4. **Local Index Pages**

#### `index.html`
- Landing page for local files
- Links to all HTML files in directory
- Stats dashboard
- Quick navigation

## 🚀 How to Use

### First Time Setup:

```bash
# 1. Generate GitHub data
python3 generate-github-index.py

# 2. Analyze themes
python3 analyze-themes.py

# 3. Open viewer
open thematic-rings-viewer.html
```

### To Refresh Data:

```bash
# Refresh from GitHub API
python3 generate-github-index.py

# Re-analyze themes
python3 analyze-themes.py

# Refresh browser (Cmd+R)
```

## 🎨 What You See

**Thematic Rings Visualization:**
- Center: @hartswf0 (245 repos)
- Ring 1 (innermost): Largest theme
- Ring 2-11: Other themes by size
- Each segment = 1 repository
- Colors distinguish themes

**Interactions:**
- **Hover legend** → Highlight ring
- **Click segment** → See repo details
- **Drag canvas** → Rotate view
- **Animate button** → Auto-rotate
- **Legend button** → Toggle theme list

## 📁 File Structure

```
WH_RIPPLE/
├── generate-github-index.py      # Fetch from GitHub
├── analyze-themes.py              # Thematic clustering
├── github-ripple-index.json       # Time-based data
├── github-thematic-index.json     # Theme-based data ⭐
├── thematic-rings-viewer.html     # Best viewer ⭐
├── ripple-rings-viewer.html       # Alternative viewer
├── sitemap-index.json             # Local files
├── index.html                     # Landing page
└── README-GITHUB-INDEX.md         # This file
```

## ✅ Fixed Issues

1. **Event listener errors** - Canvas now initializes before event binding
2. **Data loading failures** - Correct JSON file references
3. **Theme organization** - Proper thematic clustering instead of just time
4. **Legend display** - Shows theme names and counts correctly

## 🎯 Use Cases

- **Explore by theme** - Find all AI projects, media theory work, etc.
- **Discover connections** - See how repos cluster by topic
- **Portfolio navigation** - Interactive way to browse 245 repos
- **Pattern analysis** - Understand research themes and focus areas
- **Quick access** - Click any repo to jump to GitHub/Pages

## 📊 Statistics

- **Total Repos**: 245
- **Total Stars**: 3
- **Total Size**: 3.0 GB
- **Themes**: 11
- **With Pages**: 191 repos
- **Forks**: 25 repos
- **Languages**: HTML (163), JavaScript (14), CSS (9), Python (3), TypeScript (1)

## 🔄 Future Enhancements

- [ ] Search functionality
- [ ] Filter by language/stars/size
- [ ] Timeline view (chronological)
- [ ] Network graph of connections
- [ ] Export to PDF/image
- [ ] Playlist/collection system
- [ ] Theme evolution over time

---

**Status**: ✅ Fully functional
**Last Updated**: 2025-11-09
**Data Source**: GitHub API (hartswf0)
