# Delayed Matching to Sample (DMS) Task in PsychoPy

This is a simple **PsychoPy** script for running a Delayed Matching to Sample task.  
Here’s how it works: you see a sample image for **5 seconds**, wait **20 seconds**, and then pick the matching image from two choices.  

---

## What’s Included
- **Loads images from a folder** (supports PNG, JPG, BMP, and more).
- **Pairs images by number order** in filenames (e.g., `1.jpg` with `2.jpg`).
- **Adjustable timings** for sample, delay, and feedback.
- **Logs results to CSV** with accuracy and reaction times.
- **Click-based interface** with green/red feedback.

---

## How a Trial Goes
1. (Optional) Fixation dot appears.
2. **Sample image** is shown for 5s.
3. **Wait** for 20s.
4. **Two images** appear — one is the original, one is a foil.
5. **Click** the one you think is correct.
6. See **feedback** and move on to the next trial.

---

## Requirements
- [PsychoPy](https://www.psychopy.org/)
- Python 3.8+
- A folder of numbered images

---

Enjoy experimenting, and feel free to tweak it for your needs!
