# Ambient Audio System

## 🎵 Overview

Subtle static/white noise that cuts in and out randomly, creating an ambient radio-like atmosphere.

---

## 🎚️ How It Works

### **Audio Generation**
- Uses Web Audio API
- Generates white noise (random values -1 to 1)
- Creates 2-second buffer that loops
- Very quiet volume (0.02 - 0.05)

### **Cut In/Out Pattern**
- **Interval**: 8-20 seconds between cuts
- **Duration**: 2-5 seconds when active
- **Fade In**: 0.5 seconds
- **Hold**: Random duration
- **Fade Out**: Smooth ramp to silence

---

## 🔊 Technical Details

### **Volume Levels**
- Minimum: 0.02 (barely audible)
- Maximum: 0.05 (subtle presence)
- Always quiet, never intrusive

### **Timing**
```javascript
Next cut: 8000ms + random(0-12000ms)
Duration: 2000ms + random(0-3000ms)
Fade in: 500ms
Fade out: gradual over duration
```

---

## 🎮 User Experience

### **Activation**
- Starts on **first click or touch**
- Browser requires user interaction for audio
- Only starts once
- Continues in background

### **Effect**
- Like a distant radio
- Occasional interference
- Subtle atmospheric layer
- Not distracting

---

## 🛠️ Controls

### **Automatic**
- No manual controls needed
- Self-managing intervals
- Random timing feels natural

### **Future Options**
Could add:
- Volume slider
- On/off toggle
- Different static patterns
- Tuning "drift" effect

---

## 📊 Performance

- Low CPU usage
- Single audio buffer
- Efficient Web Audio API
- No audio files to load

---

## 🎨 Design Intent

**"Background presence without distraction"**

- Mimics old radio static
- Creates atmosphere
- Doesn't demand attention
- Adds depth to experience
- Makes interface feel "alive"

---

**Status**: ✅ Active on first interaction
**Volume**: Very quiet (2-5%)
**Pattern**: Random 8-20 second intervals
