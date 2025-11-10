# Re-Categorizing "Other" Projects

## 🎯 Problem

Currently there are **92 projects** in the "Other" theme - this is too many uncategorized repos. They need to be sorted into more specific, meaningful themes.

## 📋 Solution

The Python script `analyze-themes.py` automatically categorizes repos based on:
- Repository names
- Descriptions
- Topics/tags
- Keywords

To improve categorization of the 92 "Other" repos:

### **1. Update Theme Keywords**

Edit `analyze-themes.py` and expand the keyword lists to catch more repos:

```python
# Example: Add more patterns
theme_keywords = {
    'media-theory': ['mcluhan', 'media', 'ecology', 'communication', 'theory'],
    'ai-ml': ['ai', 'ml', 'neural', 'machine-learning', 'deep-learning', 'gpt', 'llm', 'model'],
    'web-dev': ['web', 'html', 'css', 'javascript', 'react', 'vue', 'frontend'],
    # ... add more keywords for each theme
}
```

### **2. Add New Themes**

Create additional theme categories for common patterns in "Other":

```python
# New themes to consider:
- 'blockchain': Crypto, blockchain, web3 projects
- 'gaming': Game development, Unity, game engines
- 'mobile': Mobile apps, iOS, Android development
- 'iot': Internet of Things, hardware, sensors
- 'security': Security tools, cryptography, privacy
- 'testing': Testing frameworks, QA tools
- 'documentation': Docs, wikis, knowledge bases
```

### **3. Manual Review**

For the most common "Other" repos:
1. Look at their names/descriptions
2. Identify common patterns
3. Create new themes or update existing keyword lists
4. Re-run the script

### **4. Re-Run Analysis**

```bash
python3 analyze-themes.py
```

This will regenerate `github-thematic-index.json` with better categorization.

---

## 💡 Suggested New Themes

Based on typical repos that end up in "Other":

| Theme | Description | Example Keywords |
|-------|-------------|------------------|
| **Digital Tools** | Productivity tools, CLI utils | `tool`, `utility`, `cli`, `command` |
| **Research** | Research projects, experiments | `research`, `experiment`, `study`, `analysis` |
| **Templates** | Boilerplates, starters | `template`, `boilerplate`, `starter`, `scaffold` |
| **Personal** | Personal sites, portfolios, blogs | `portfolio`, `blog`, `personal`, `website` |
| **Learning** | Learning projects, tutorials | `learning`, `tutorial`, `course`, `practice` |
| **Automation** | Scripts, automation tools | `automation`, `script`, `workflow`, `ci-cd` |
| **Content** | Content management, CMS | `cms`, `content`, `blog-engine`, `static-site` |

---

## 🔧 Implementation Steps

### **Step 1: Analyze "Other" Category**

Look at the 92 repos manually:
```bash
# Extract "Other" repos from JSON
python3 -c "
import json
data = json.load(open('github-thematic-index.json'))
other = [r for ring in data['theme_rings'] if ring['theme_id'] == 'other' for r in ring['repos']]
for repo in other:
    print(f'{repo['name']}: {repo.get('description', 'N/A')}')
"
```

### **Step 2: Identify Patterns**

Group similar repos:
- Count common words in names/descriptions
- Look for language patterns
- Check topics/tags
- Find related tech stacks

### **Step 3: Update Script**

Edit `analyze-themes.py`:

```python
# Add new themes
theme_keywords = {
    # Existing themes...
    
    # New themes
    'digital-tools': ['tool', 'utility', 'cli', 'command-line', 'helper'],
    'research': ['research', 'experiment', 'study', 'analysis', 'exploration'],
    'templates': ['template', 'boilerplate', 'starter', 'scaffold', 'skeleton'],
    'automation': ['automation', 'script', 'workflow', 'ci', 'cd', 'pipeline'],
    'content': ['cms', 'content', 'blog', 'static-site', 'generator'],
}

# Update theme colors
theme_colors = {
    # ... existing colors
    'digital-tools': '#00BCD4',  # Cyan
    'research': '#9C27B0',       # Purple
    'templates': '#795548',      # Brown
    'automation': '#607D8B',     # Blue Gray
    'content': '#FF5722',        # Deep Orange
}
```

### **Step 4: Re-Run & Verify**

```bash
# Generate new index
python3 analyze-themes.py

# Check results
# "Other" should now have < 30 repos (ideally < 20)
```

---

## 📊 Goal

**Target**: Reduce "Other" from **92 repos** to **< 20 repos**

**Method**:
- Add 5-7 new specific themes
- Expand keywords for existing themes
- Improve pattern matching

**Result**:
- Better organization
- More meaningful themes
- Easier navigation
- Less "miscellaneous" clutter

---

## 🎨 After Re-Categorization

The viewer will automatically:
- Show new themes in legend
- Display proper colors
- Update minimap
- Organize ripple view by new themes
- Populate filter dropdown with new categories

**No viewer code changes needed** - just re-run the Python script!

---

## 📝 Notes

- Keep "Other" for truly misc projects
- Aim for 10-30 repos per theme (ideal range)
- Avoid creating themes with < 5 repos
- Descriptive theme names help users understand
- Update theme descriptions in viewer after adding new themes
