# 🍊 WH_RIPPLE — Repository Explorer & Portfolio

> **245 repos. 3 users. Sorting algorithmic slop into reusable blocks.**

A forensic slopwright's toolkit for exploring GitHub repositories through interactive, thematic visualizations. Built by Watson Hartsoe.

**Design System: Circles over rectangles. Orange over complexity. Less is more.**

---

## 🎯 **Quick Start**

1. **Clone or download** this repository
2. **Open `index.html`** in your browser
3. **Navigate with circular buttons** — All 14 HTML files connected
4. **Click 🍊** to explore the main grid viewer

**Live:** [View the Grid →](orange-grid-viewer.html)

---

## 📂 **Project Structure**

```
WH_RIPPLE/
├── index.html                   # Landing page (14 files connected)
├── orange-grid-viewer.html      # Main explorer (★ PRIMARY TOOL)
├── about-watson.html            # Research context
├── orange-grid-universal.css    # Universal design system
├── github-thematic-index.json   # 245 repos data
├── sitemap-index.json           # Site structure
└── analyze-themes.py            # Data generator

Viewers (6):
├── orange-ripple-viewer.html
├── thematic-rings-viewer.html
├── ripple-rings-viewer.html
├── ripple-viewer-clean.html
├── kimi-k2-lego-FIXED.html
└── mythos_presentation.html

GitHub Indexes (3):
├── git_hub_repo_index_bauhaus_table_hartswf_0 (2).html  # Latest
├── git_hub_repo_index_bauhaus_table_hartswf_0 (1).html
└── git_hub_repo_index_bauhaus_table_hartswf_0.html

Pages (2):
├── wh0.html
└── wh1.html

Documentation (7):
├── README.md                    # This file
├── ORANGE-GRID-SYSTEM.md        # Design system guide
├── NAVIGATION.md                # Site navigation
├── MOBILE-HEADER.md             # Mobile design
├── FINAL-IMPROVEMENTS.md        # Feature summary
├── MINIMAL-IMPROVEMENTS.md      # Design philosophy
└── RECATEGORIZE-OTHER.md        # Theme guide
```

**Total: 15 HTML files, all accessible from index.html**

### **🚀 NEW: Live Demos** (`live-demos.html`)
**Real-world deployments on GitHub Pages**

- ✅ **60+ live projects** from hartswf0 GitHub Pages
- ✅ **Orange grid aesthetic** matching the main site
- ✅ **Categorized cards** with project names and URLs
- ✅ **Direct links** to tetrad-gamepad, soul-mansion, LEGOS, and more
- ✅ **Multiple variants** shown when available
- ✅ **Repo links** distinguished from live demos

---

## 🔧 **Main Tools**

### **1. Orange Grid Viewer** (`orange-grid-viewer.html`)
**The primary interface for exploring all 245 repositories.**

#### **Features:**
- ✅ **Grid View** — Cards with hover previews and number badges
- ✅ **Ripple View** — Animated canvas visualization with theme clusters
- ✅ **Timeline View** — Chronological exploration by year/month
- ✅ **Minimap** — GitHub contribution-style navigation with viewport indicator
- ✅ **Mobile-friendly** — Hamburger menu with touch-optimized controls
- ✅ **Filters** — By theme, language, sort order
- ✅ **Search** — Real-time filtering by name/description
- ✅ **Expanded View** — Click any repo to see details + iframe preview

#### **Views:**

**Grid View:**
- 8 columns on desktop, responsive on mobile
- Minimal number badges (black → orange on hover → white when selected)
- Staggered pop-in animation on load
- Hover to preview, click to expand

**Ripple View:**
- Canvas-based animation with floating repo balls
- Organized by theme in spatial clusters
- Better spacing (40px gaps, 32% distance)
- Interactive clicking and dragging

**Timeline View:**
- Grouped by year and month
- See project evolution over time
- Same filtering and search capabilities

**Minimap:**
- Full-width touchpad below header
- All 245 repos as color-coded dots
- Click to jump to repo with smooth scroll
- Viewport indicator box shows visible section
- 8px dots with active state highlighting

---

### **2. About Watson** (`about-watson.html`)
**Minimal, integrated "about me" page explaining the research practice.**

#### **Structure:**
- **Hero** — Name, title, core stats (245 repos, 3 users)
- **Four Families** — Work organized by rhetorical genome:
  - Media as Operator
  - Centauric Cognition
  - Narrative as OS
  - Encoded Power
- **Mythic → Mechanics** — Claims deflated from conference-speak to real-talk
- **Links** — Browse grid, GitHub, YouTube

#### **Design:**
- Orange grid aesthetic (minimal, clean)
- Clickable project bubbles with user counts
- One-line claims, no fluff
- Less is more philosophy

---

### **3. Index & Sitemap** (`index.html`)
**Landing page with sitemap navigator and quick actions.**

#### **Features:**
- Stats bar (files, size, categories)
- Quick links to Orange Grid and About page
- Categorized file browser
- Tree view toggle
- Export JSON functionality

---

## 🎨 **Data Structure**

### **`github-thematic-index.json`**
Generated by `analyze-themes.py` from GitHub API data.

```json
{
  "summary": {
    "total_repos": 245,
    "total_stars": 123,
    "total_forks": 45
  },
  "theme_rings": [
    {
      "theme_id": "media-theory",
      "theme_name": "Media Theory & McLuhan",
      "color": "#FF6B35",
      "repo_count": 27,
      "repos": [
        {
          "name": "tetrad-gamepad",
          "description": "McLuhan's tetrad as interactive controller",
          "url": "https://github.com/hartswf0/tetrad-gamepad",
          "language": "JavaScript",
          "stars": 3,
          "created_at": "2024-03-15",
          "updated_at": "2024-11-10"
        }
      ]
    }
  ]
}
```

---

## 🔄 **Regenerating the Index**

To update `github-thematic-index.json` with fresh data:

```bash
python3 analyze-themes.py
```

### **What it does:**
1. Fetches all repos from GitHub API (`@hartswf0`)
2. Categorizes by keywords and patterns
3. Assigns theme colors
4. Outputs sorted JSON with metadata

### **Improving Categorization:**

The "Other Projects" theme currently has **92 repos** (too many). To fix:

1. **Edit `analyze-themes.py`**
2. **Expand keyword lists** for existing themes
3. **Add new themes** (e.g., Digital Tools, Research, Templates)
4. **Re-run the script**

See `RECATEGORIZE-OTHER.md` for detailed guide.

---

## 🎨 **Design Philosophy: Circles Over Rectangles**

### **Universal Orange Grid System**
**See `ORANGE-GRID-SYSTEM.md` for complete guide**

### **Core Principles**
1. **Circle First** — All interactive elements are circular
2. **Radial Gradients** — Depth through light positioning (circle at 30% 30%)
3. **Orange Signal** — Single accent color (#FF6B35)
4. **Minimal Borders** — 1px subtle opacity, no heavy outlines
5. **Smooth Motion** — 0.3s ease transitions
6. **Dark Background** — Pure black (#0a0a0a) base
7. **Less Is More** — Remove unnecessary elements

### **Element Shapes**
```
Cards:   ⭕ Circular (border-radius: 50%, aspect-ratio: 1)
Buttons: ⭕ Circular (60×60px minimum)
Badges:  ⭕ Circular dots (8-12px)
Icons:   ⭕ Contained in circles
Primary: ⭕ Large circles (120×120px)
```

### **No Irregular Elements**
```
❌ Sharp corners
❌ Heavy borders (>1px)
❌ Complex shadows
❌ Multiple border styles
✅ Perfect circles
✅ Radial gradients
✅ Minimal borders
✅ Subtle glows
```

### **Color System**
```css
--bg: #0a0a0a                    /* Black background */
--text: #e0e0e0                  /* Light gray text */
--accent: #FF6B35                /* Orange primary */
--border: rgba(255, 107, 53, 0.2)  /* Subtle orange */
--hover: rgba(255, 107, 53, 0.1)   /* Hover state */
```

### **Universal CSS**
Apply to any HTML file:
```html
<link rel="stylesheet" href="orange-grid-universal.css">
```

All 14 HTML files now share the same circular, minimal aesthetic.

---

## 📊 **Stats & Scale**

| Metric | Value |
|--------|-------|
| **Total Repos** | 245 |
| **HTML Files** | 15 (all connected) |
| **Live Demos** | 60+ (GitHub Pages) |
| **Themes** | 16 |
| **Languages** | ~20 |
| **Users** | 3 (tetrad-gamepad, latent-sculptor, soul-mansion) |
| **Design System** | Orange grid, minimal |
| **Status** | Early |

---

## 🚀 **Key Features**

### **Interactive Navigation**
- ✅ Click minimap dots to jump to repos
- ✅ Scroll with viewport indicator tracking
- ✅ Search by name/description
- ✅ Filter by theme + language
- ✅ Sort chronologically or by theme

### **Mobile Experience**
- ✅ Hamburger menu (clean, no border, 16px height)
- ✅ Theme browser with descriptions
- ✅ Touch-friendly controls (48px+ tap targets)
- ✅ Responsive grid (1-8 columns)
- ✅ Ripple view fits screen

### **Visual Feedback**
- ✅ Pulse animation when navigating
- ✅ Hover previews on grid cards
- ✅ Active state on minimap dots
- ✅ Smooth scroll with offset
- ✅ Staggered pop-in on load

### **Expanded View**
- ✅ Auto-opens when clicking minimap
- ✅ Shows full details + iframe preview
- ✅ Close button to return
- ✅ Prevents hidden scroll issue

---

## 📖 **Documentation**

- **`MOBILE-HEADER.md`** — Mobile header design guide
- **`FINAL-IMPROVEMENTS.md`** — Summary of all improvements
- **`MINIMAL-IMPROVEMENTS.md`** — Minimal design philosophy
- **`RECATEGORIZE-OTHER.md`** — Guide to fixing "Other" category

---

## 🛠️ **Tech Stack**

- **HTML5** — Semantic markup
- **CSS3** — Grid, flexbox, animations, responsive design
- **Vanilla JavaScript** — No dependencies
- **Canvas API** — Ripple view rendering
- **JSON** — Data storage

### **No Build Step**
- Open `index.html` in browser
- All files are static
- No npm, webpack, or compilation needed

---

## 🎯 **Use Cases**

### **Portfolio Browsing**
- Explore Watson's 245 repos by theme
- Filter to find specific types of projects
- Preview repos with iframe embedding
- See chronological evolution

### **Research Context**
- Understand the four families of work
- See how projects connect to theory
- Navigate from mythic claims to mechanics
- Find specific tools (3 with users)

### **Data Export**
- Export JSON for analysis
- View sitemap structure
- Copy file paths
- See file sizes and metadata

---

## 🎨 **Color Palette**

```css
--accent: #FF6B35    /* Orange - primary brand */
--bg: #0a0a0a        /* Black - background */
--text: #e0e0e0      /* Light gray - text */
--muted: #666        /* Mid gray - secondary */
```

### **Theme Colors:**
Each of the 16 themes has its own color assigned by the Python script, creating a visual spectrum in the minimap and ripple view.

---

## 📱 **Responsive Breakpoints**

- **Mobile:** < 768px (1-2 columns)
- **Tablet:** 768-1199px (3-4 columns)
- **Desktop:** 1200-1599px (6 columns)
- **Large:** 1600px+ (8 columns)

---

## 🔗 **External Links**

- **GitHub:** [@hartswf0](https://github.com/hartswf0)
- **YouTube:** [@watsonhartsoe](https://youtube.com/@watsonhartsoe)
- **Medium:** [@Wfh.iii](https://medium.com/@Wfh.iii)

---

## 🧪 **Development**

### **Local Setup**
```bash
# Clone repo
git clone https://github.com/hartswf0/potters-wheel.git
cd potters-wheel

# Open in browser
open index.html
# or
python3 -m http.server 8000
```

### **Updating Data**
```bash
# Regenerate index from GitHub
python3 analyze-themes.py

# Refresh browser to see changes
```

### **File Editing**
All HTML files are standalone. Edit directly in your IDE:
- `orange-grid-viewer.html` — Main viewer
- `about-watson.html` — About page
- `index.html` — Landing page

---

## 🎓 **Core Thesis**

**Building systems that treat media as ecology, stories as executable rituals, and audiences as co-authors—composing worlds like software, verifying them like science, and sharing them like folk art.**

### **The Practice**
One person sorting algorithmic slop into reusable blocks, logging failures, and building tools so others can sort faster. Every AI output becomes either a reusable component with traceable lineage or documented waste.

### **Four Families**

1. **Media as Operator** — Turn media effects into design parameters you can fork and steer
2. **Centauric Cognition** — The centaur is a cognitive subject whose native reasoning is interfacial
3. **Narrative as OS** — Mythology is live firmware; to critique it you must refactor its narrative kernels
4. **Encoded Power** — Every interface is a political settlement; critique requires adversarial reimplementation

---

## 📊 **Key Projects**

| Project | Users | Description |
|---------|-------|-------------|
| **tetrad-gamepad** | 3 | McLuhan's tetrad as interactive controller |
| **latent-sculptor** | 1 | Prompting as spatial sculpting |
| **soul-mansion** | 1 workshop | Images compiled as LEGOS programs |
| **LEGOS** | — | Atomic narrative building blocks |
| **mythos-canon** | — | Living knowledge graph for worlds |
| **spuddy-west** | — | Western picture exploring algorithmic culture |

---

## 🏗️ **Future Work**

### **Planned Features**
- [ ] Graph view showing repo connections
- [ ] Collaboration network visualization
- [ ] Advanced filtering (date ranges, file types)
- [ ] Bookmarking/favorites system
- [ ] Share URLs with filters applied

### **Data Improvements**
- [ ] Reduce "Other" category from 92 to <20 repos
- [ ] Add project descriptions to more repos
- [ ] Include README previews
- [ ] Show commit activity graphs

### **UX Enhancements**
- [ ] Keyboard shortcuts
- [ ] Dark/light mode toggle
- [ ] Accessibility improvements
- [ ] Print-friendly CSS

---

## 📝 **License**

See individual repositories for licensing. This viewer is MIT licensed.

---

## 🙏 **Acknowledgments**

- **Blue Deli / Blue Belt Films** — Collaborators on A Western Picture
- **Georgia Tech PACE ICE** — Research support
- **Gen48 teams** — Film experiments
- **All contributors** to the 245 repositories

---

## 📬 **Contact**

**Watson Hartsoe**
- GitHub: [@hartswf0](https://github.com/hartswf0)
- YouTube: [@watsonhartsoe](https://youtube.com/@watsonhartsoe)
- Medium: [@Wfh.iii](https://medium.com/@Wfh.iii)

---

**Built with care. Deployed with honesty. 245 demos, 3 users, status: early.**

🍊
