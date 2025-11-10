# Orange Grid Viewer - Complete Feature List

## 🎯 Overview
Advanced repository visualization system with grid and ripple views, featuring extensive filtering, sorting, zoom, hover previews, and connection mapping.

---

## 🌟 Main Features

### **1. Dual View Modes**

#### Grid View (Default)
- Organized grid of orange circles
- Each orange = one repository
- Responsive grid layout
- Color-coded by theme

#### Ripple View
- Organic floating oranges
- Theme-based clustering
- Click creates ripple effects
- Drag to pan around

---

## 🔍 Filtering & Sorting

### **Filter by Theme**
- Dropdown shows all 11 themes
- Filter to specific theme family
- Shows repo count per theme
- Example: "Media Theory & McLuhan (27)"

### **Filter by Language**
- Dropdown populated with all languages
- Filter HTML, JavaScript, Python, etc.
- Shows only repos in that language

### **Sort Options**
1. **By Theme** - Groups by thematic category
2. **By Stars** - Most starred first
3. **By Size** - Largest repos first
4. **Recently Updated** - Most recent activity
5. **By Name** - Alphabetical order

---

## 🔎 Zoom Controls

### **4 Zoom Levels**
- **Small** (−) - 120px oranges, 12px gaps
- **Medium** (default) - 200px oranges, 20px gaps
- **Large** (+) - 280px oranges, 28px gaps
- **Extra Large** (++) - 360px oranges, 35px gaps

### **Usage**
- Click `+` button to zoom in
- Click `−` button to zoom out
- Grid dynamically resizes
- Smooth transitions

---

## 👁️ Hover Preview

### **In Grid View**
When you hover over an orange:

1. **Repo with GitHub Pages**:
   - Circular iframe preview appears
   - Shows live page inside the circle
   - Scales to fit
   - Smooth fade-in animation

2. **Repo without Pages**:
   - Shows repo name
   - Shows metadata

### **Always Shows**
- Repository name
- Language badge
- Numbered badge (top-right)

---

## 🔢 Number Badges

- Every orange has a number
- Shows position in current filtered view
- Top-right corner
- Black badge with orange number
- Updates when filters change

---

## 🕸️ Cross-Connections

### **Connection Visualization**
Click "Connections" button to:

- Draw lines between related repos
- Connects repos with **same language**
- Dashed lines in theme color
- Semi-transparent overlay
- SVG-based rendering

### **What You See**
- All JavaScript repos connected
- All HTML repos connected
- All Python repos connected
- Helps identify language families
- Visual pattern recognition

---

## 📦 Expanded View

### **Click Any Orange**
Opens full modal with:

#### Sidebar
- **Stats Cards**:
  - Stars count
  - Forks count  
  - Size in MB
  - Language

- **File Ripples**:
  - Shows related files as bubbles
  - README.md, index.html, etc.
  - Color-coded to theme
  - Clickable (future: view file)

#### Main Panel
- **If Has Pages**:
  - Full iframe preview (600px)
  - Action buttons: Open Page, View Code, Homepage
  
- **If No Pages**:
  - Message + GitHub link
  - Homepage link if available

---

## 🎨 Visual Design

### **Orange Styling**
- Radial gradient (light to dark)
- Glossy shine effect (top-left highlight)
- Inset shadows for depth
- Box shadow with glow
- Perfect circles

### **Color System**
- 11 theme colors
- Each theme has signature color
- Consistent across views
- Orange (#ff6b35) as primary accent

### **Animations**
- Smooth hover scale (1.0 → 1.1)
- Preview fade-in
- Connection line drawing
- Zoom transitions
- Ripple emanations (ripple view)

---

## 📊 Live Stats

### **Header Display**
- @hartswf0 username
- Total repo count (updates with filters)
- Updates in real-time

---

## 🎮 Controls Summary

### **Header Bar**
```
[Grid] [Ripples] | [Theme ▼] [Language ▼] [Sort ▼] | [−] [+] | [Connections]
```

### **Keyboard/Mouse**
- Click orange → Expand
- Hover orange → Preview (if pages)
- Drag canvas → Pan (ripple view)
- Click connection → Toggle lines

---

## 🔄 View Comparison

| Feature | Grid View | Ripple View |
|---------|-----------|-------------|
| Layout | Organized grid | Organic clusters |
| Hover | Iframe preview | Name label |
| Click | Expand modal | Ripple + expand |
| Drag | N/A | Pan around |
| Connections | SVG lines | N/A |
| Zoom | 4 levels | N/A |
| Numbers | Yes | No |

---

## 💡 Use Cases

### **Explore by Theme**
1. Select theme from dropdown
2. See all repos in that theme
3. View connections between them
4. Click to explore

### **Find by Language**
1. Filter to JavaScript
2. Click "Connections"
3. See all JS repos linked
4. Identify patterns

### **Browse Recent Work**
1. Sort by "Recently Updated"
2. See latest projects first
3. Zoom in for details
4. Hover to preview pages

### **Size Analysis**
1. Sort by "Size"
2. See largest projects
3. Connections show language families
4. Identify heavy repos

---

## 🎯 Technical Details

### **Performance**
- Lazy-loaded iframes (on hover)
- SVG for connection lines
- Filtered rendering
- Smooth 60fps animations

### **Responsive**
- Works on mobile
- Touch-friendly
- Adapts to screen size
- Side panel on mobile

### **Data Source**
- `github-thematic-index.json`
- 245 repositories
- 11 thematic clusters
- Real-time filtering

---

## 🚀 Quick Start

1. **Open** `orange-grid-viewer.html`
2. **Filter** by theme or language
3. **Sort** by stars, size, or date
4. **Zoom** in/out to adjust view
5. **Hover** to preview pages
6. **Click** to explore details
7. **Toggle connections** to see relationships

---

## 🎨 Design Philosophy

**"Each repository is an orange in a bowl"**

- Natural, organic layout
- Tactile, clickable elements
- Hover reveals depth
- Connections show relationships
- Numbers provide order
- Zoom controls perspective
- Filters focus attention

---

**Status**: ✅ Fully Functional
**File**: orange-grid-viewer.html
**Last Updated**: 2025-11-10
