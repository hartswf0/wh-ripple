# Meaningful Connection System

## 🧠 How Connections Work Now

The connection system now uses **intelligent analysis** to find actual relationships between repositories, not just simple language matching.

---

## 📊 Connection Scoring System

Each potential connection is scored based on **6 factors**:

### **1. Same Theme** (Weight: 3 points)
- Repos in same thematic family (e.g., both Media Theory)
- Strong indicator of related work
- Example: `platos-cave` ↔ `platos-laundry`

### **2. Shared Topics** (Weight: 2 points per topic)
- GitHub topics/tags that both repos have
- Direct metadata match
- Example: Both tagged with `interactive`, `visualization`

### **3. Similar Name Patterns** (Weight: 1 point per shared word)
- Analyzes kebab-case/underscore naming
- Finds shared words in repo names
- Example: `media-shaper` ↔ `media-surfer` (share "media")
- Minimum 4 characters to avoid false matches

### **4. Shared Concepts** (Weight: 1.5 points per concept)
- Analyzes descriptions for keywords
- Detects: `ai`, `media`, `interactive`, `visualization`, `tool`, `framework`, `app`, `3d`, `vr`
- Semantic relationship detection
- Example: Both describe "interactive media tools"

### **5. Same Language** (Weight: 1 point)
- HTML, JavaScript, Python, etc.
- Weakest indicator (just tech stack)
- Combined with other factors

### **6. Similar Size** (Weight: 0.5 points)
- Within 30% of each other in KB
- May indicate similar complexity/scope
- Subtle indicator

---

## 🎯 Connection Threshold

**Minimum Score: 3 points**

Only connections with strength ≥3 are drawn. This ensures:
- No spam lines
- Only meaningful relationships shown
- Focus on actual connections

---

## 🎨 Visual Encoding

### **Line Thickness**
- Stronger connection = thicker line
- Width = strength / 2 (max 3px)

### **Line Opacity**
- Stronger connection = more visible
- Opacity = strength / 10 (max 0.6)

### **Line Style**
- **Solid line** - Very strong (strength > 5)
- **Dashed line** - Moderate (strength 3-5)

### **Line Color**
- Uses theme color of source repo
- Helps identify theme clusters

---

## 💡 Examples of Connections

### **Strong Connection (Score: 8)**
```
platos-cave ↔ platos-laundry
- Same theme: Philosophy ✓ (+3)
- Similar names: "plato" ✓ (+1)
- Shared concepts: "plato", "reality" ✓ (+3)
- Same language: HTML ✓ (+1)
= 8 points → THICK SOLID LINE
```

### **Moderate Connection (Score: 4.5)**
```
media-shaper ↔ media-surfer
- Same theme: Media Theory ✓ (+3)
- Similar names: "media" ✓ (+1)
- Shared concepts: "media" ✓ (+1.5)
= 5.5 points → MEDIUM DASHED LINE
```

### **No Connection (Score: 1)**
```
random-repo-A ↔ random-repo-B
- Different themes ✗
- No shared topics ✗
- Different names ✗
- No shared concepts ✗
- Same language: HTML ✓ (+1)
= 1 point → NOT DRAWN
```

---

## 🔍 How to Read Connections

### **Hover Over Lines**
- Shows both repo names
- Lists connection reasons
- Example: "Same theme, 2 shared topics, Similar names"

### **Dense Clusters**
- Many lines = related work
- Indicates a project family
- Theme-based grouping

### **Long Lines**
- Cross-theme connections
- Unexpected relationships
- Interesting discoveries

### **Thick Lines**
- Very strong relationship
- Core project family
- Worth exploring together

---

## 📈 Connection Limit

**Maximum: 100 connections drawn**

Prevents visual clutter while showing most important relationships.

---

## 🎮 Usage Tips

### **Filter First, Then Connect**
1. Filter to a theme or language
2. Click "Connections"
3. See relationships within that subset
4. Less clutter, more insight

### **Zoom In for Detail**
1. Zoom to large oranges
2. Enable connections
3. See line thickness better
4. Hover to read relationships

### **Compare Themes**
1. No filter (show all)
2. Enable connections
3. See cross-theme bridges
4. Discover unexpected links

---

## 🧪 Technical Details

### **Performance**
- Analyzes all repo pairs
- O(n²) but limited to 100 connections
- Runs in ~100ms for 245 repos
- SVG-based rendering

### **Console Output**
Check console: `📊 Drew N meaningful connections`

---

## 🎯 What Makes This Better

### **Old System**
- ❌ Only matched language
- ❌ Too many meaningless lines
- ❌ No context
- ❌ Visual noise

### **New System**
- ✅ Multi-factor analysis
- ✅ Only meaningful relationships
- ✅ Shows WHY connected
- ✅ Visual strength encoding
- ✅ Hover tooltips explain
- ✅ Threshold filtering

---

## 📱 Mobile-Friendly Header

### **Responsive Layout**
- Desktop: All controls in one row
- Tablet: Wraps to 2 rows
- Mobile: Stacks vertically

### **Mobile Optimizations**
- Smaller buttons/selects
- Hides "@hartswf0" label on tiny screens
- Full-width filters
- Touch-friendly spacing

### **Breakpoints**
- `1024px` - Two rows
- `640px` - Vertical stack, compact sizing

---

**Result**: Connections now show actual project relationships based on content, themes, and purpose—not just technology!
