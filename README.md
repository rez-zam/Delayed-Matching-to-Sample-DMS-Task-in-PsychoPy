# Delayed Matching to Sample (DMS) Task in PsychoPy

A **PsychoPy** implementation of the Delayed Matching to Sample (DMS) cognitive task.  
In each trial, a sample image is displayed for **5 seconds**, followed by a **20-second delay**.  
Then, two images are shown side-by-side: one matches the sample, the other is a foil.  
The participant must choose the matching image.

---

## Features
- 📂 **Folder-based image loading** — load all valid image files from a specified folder.
- 🔢 **Numeric order pairing** — pairs images by numeric filename order (e.g., `1.jpg` with `2.jpg`).
- 🕒 **Customizable timing** — easily change sample display time, delay, and feedback durations.
- 📝 **CSV logging** — trial-by-trial logging with image paths, choices, correctness, and reaction time.
- 🎯 **2AFC choice interface** — participant selects with mouse click, with green/red feedback.

---

## How It Works
1. **Fixation** (optional) before the sample.
2. **Sample** is displayed for 5 seconds.
3. **Delay interval** of 20 seconds.
4. **Choice screen** with target and foil images.
5. **Feedback** on correctness.
6. **CSV logging** of trial data.

---

## File Structure
- `main.py` — main PsychoPy script.
- `Images/` — folder containing numbered image files.
- `results_YYYYMMDD_HHMMSS.csv` — generated results file.

---

## Requirements
- [PsychoPy](https://www.psychopy.org/)  
- Python 3.8+  
- A folder of images (PNG/JPG/BMP/etc.)

---

## Experiment Configuration (in code)
```python
# ==================================
# Experiment Configuration
# ==================================
# - Defines file sources, pairing rules, timing, layout, and data logging.
# - This setup is for a Delayed Matching to Sample (DMS) task.
