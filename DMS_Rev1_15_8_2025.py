from psychopy import visual, core, event
import random, os, csv, glob, re
from datetime import datetime

# ==============================
# Experiment configuration
# ==============================

USE_FOLDER = True
IMAGES_DIR = r".\Images"      # Folder containing your images
VALID_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif")

# Pairing policy:
# - We want deterministic pairing by the numeric order in filenames: 1 with 2, 3 with 4, ...
RANDOM_PAIRING   = False       # No random pairing; use ordered (numeric) pairing
WITH_REPLACEMENT = False       # Not used when RANDOM_PAIRING=False

# Trial order:
SHUFFLE_TRIALS = False         # Keep trials in the same order as the pairs were formed

# Timing (seconds)
T_FIX    = 0.5                 # Fixation before the sample (set to 0.0 if you don't want it)
T_SAMPLE = 5.0                 # Show the sample image for 5 seconds
T_DELAY  = 20.0                # After 20 seconds, show the two-choice screen
T_FB     = 0.6                 # Feedback duration

# Stimulus layout
IMG_SIZE = (200, 200)          # Image size in pixels (width, height)
OFFSET_X = 300                 # Horizontal offset for left/right images

# Data logging
SAVE_CSV = True
CSV_PATH = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


# ==============================
# Folder utilities
# ==============================

def list_images(folder, valid_exts=VALID_EXTS):
    """Return a list of image file paths in `folder` whose extensions match `valid_exts`."""
    files = [f for f in glob.glob(os.path.join(folder, "*")) if f.lower().endswith(valid_exts)]
    return files

def numeric_key(path):
    """
    Sorting key that extracts the first number found in the filename.
    If no number exists, push it to the end (by using +∞) and break ties by name.
    Example: '2.jpg' < '10.jpg' (true numeric ordering, not lexicographic).
    """
    base = os.path.basename(path)
    m = re.search(r'\d+', base)
    return (int(m.group()) if m else float('inf'), base.lower())

def make_pairs_random_no_replacement(files):
    """Shuffle and split into non-overlapping pairs. Drop the last file if odd."""
    random.shuffle(files)
    if len(files) < 2:
        return []
    if len(files) % 2 == 1:
        files = files[:-1]
    return [(files[i], files[i+1]) for i in range(0, len(files), 2)]

def make_pairs_random_with_replacement(files, n_trials):
    """
    Build `n_trials` random pairs where images can repeat across trials.
    Each pair contains two *distinct* images sampled from the pool.
    """
    if len(files) < 2:
        return []
    pairs = []
    for _ in range(n_trials):
        a, b = random.sample(files, 2)
        pairs.append((a, b))
    return pairs

def build_trials():
    """
    Create the list of image pairs for the experiment.

    If RANDOM_PAIRING=False:
        - Sort files by the first number in their names (numeric order).
        - Pair as (1,2), (3,4), (5,6), ...
        - If there is an odd file out, drop the last one.

    Otherwise:
        - Use the legacy random-pairing options (with or without replacement).
    """
    files = list_images(IMAGES_DIR)
    if len(files) < 2:
        raise RuntimeError("Found fewer than two images in the folder.")

    if RANDOM_PAIRING and not WITH_REPLACEMENT:
        pairs = make_pairs_random_no_replacement(files)
    elif RANDOM_PAIRING and WITH_REPLACEMENT:
        n_trials = max(1, len(files) // 2)
        pairs = make_pairs_random_with_replacement(files, n_trials)
    else:
        # Deterministic numeric ordering
        files = sorted(files, key=numeric_key)
        if len(files) % 2 == 1:
            files = files[:-1]
        pairs = [(files[i], files[i+1]) for i in range(0, len(files), 2)]

    if SHUFFLE_TRIALS:
        random.shuffle(pairs)
    return pairs


# ==============================
# PsychoPy setup
# ==============================

win = visual.Window(fullscr=False, color=[0.5, 0.5, 0.5], units="pix")
fix = visual.Circle(win, radius=5, fillColor="black", lineColor="black")
mouse = event.Mouse(visible=True, win=win)

def safe_quit_check():
    """Allow quitting anytime via Esc/ESC or Q/q."""
    keys = event.getKeys()
    if "escape" in keys or "esc" in keys or "q" in keys:
        win.close()
        core.quit()

def fixation(t):
    """Show a central fixation dot for `t` seconds."""
    fix.draw()
    win.flip()
    core.wait(t)
    safe_quit_check()

def show_img(path, t):
    """Show a single image for `t` seconds."""
    img = visual.ImageStim(win, image=path, size=IMG_SIZE)
    img.draw()
    win.flip()
    core.wait(t)
    safe_quit_check()

def choices(sample_path, foil_path):
    """
    Show two images, left and right, and collect a mouse response.
    One image is the target (the correct answer), randomly assigned to left or right.

    Returns:
        dict with keys:
          - choice_side: "left" or "right"
          - correct_side: "left" or "right"
          - rt: reaction time in seconds
          - left_path: file path shown on the left
          - right_path: file path shown on the right
    """
    # Randomly decide which side is correct
    correct_side = random.choice(["left", "right"])
    if correct_side == "left":
        left_img_path, right_img_path = sample_path, foil_path
    else:
        left_img_path, right_img_path = foil_path, sample_path

    stim_left  = visual.ImageStim(win, image=left_img_path,  size=IMG_SIZE, pos=(-OFFSET_X, 0))
    stim_right = visual.ImageStim(win, image=right_img_path, size=IMG_SIZE, pos=( OFFSET_X, 0))

    # Reset input and start the RT clock from the first frame
    mouse.clickReset()
    event.clearEvents()
    clock = core.Clock()
    clock.reset()

    while True:
        safe_quit_check()
        stim_left.draw()
        stim_right.draw()
        win.flip()

        # Wait for a left-button click; ignore clicks outside both images
        buttons, _ = mouse.getPressed(getTime=True)
        if buttons[0]:
            pos = mouse.getPos()
            # Debounce: wait for release to avoid multiple detections
            while mouse.getPressed()[0]:
                core.wait(0.01)
                safe_quit_check()

            if stim_left.contains(pos):
                choice_side = "left"
            elif stim_right.contains(pos):
                choice_side = "right"
            else:
                # Click outside both images—keep waiting
                continue

            rt = clock.getTime()
            return {
                "choice_side": choice_side,
                "correct_side": correct_side,
                "rt": rt,
                "left_path": left_img_path,
                "right_path": right_img_path
            }

def feedback(correct):
    """Full-screen color feedback: green for correct, red for incorrect."""
    color = "green" if correct else "red"
    fb_rect = visual.Rect(win, width=9999, height=9999,
                          fillColor=color, lineColor=color)
    fb_rect.draw()
    win.flip()
    core.wait(T_FB)
    safe_quit_check()


# ==============================
# CSV helpers
# ==============================

def csv_header(path):
    """Create a fresh CSV file with the standard header row."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "trial_index",
            "pair_a", "pair_b",
            "sample", "foil",
            "left_image", "right_image",
            "correct_side", "choice_side",
            "correct", "rt_sec"
        ])

def csv_append(path, row):
    """Append a single trial row to the CSV."""
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)


# ==============================
# Run the experiment
# ==============================

if SAVE_CSV:
    csv_header(CSV_PATH)

TRIAL_PAIRS = build_trials()

for idx, (a_path, b_path) in enumerate(TRIAL_PAIRS, start=1):
    # 1) Optional fixation before the sample
    fixation(T_FIX)

    # 2) Decide which file is the sample vs. the foil.
    #    (If you want the first of the pair to ALWAYS be the sample, replace the next line with:
    #       sample_path, foil_path = a_path, b_path)
    sample_path, foil_path = random.choice([(a_path, b_path), (b_path, a_path)])

    # 3) Show the sample for 5 seconds
    show_img(sample_path, T_SAMPLE)

    # 4) Retention interval of 20 seconds (currently shows fixation; use a blank screen if you prefer)
    fixation(T_DELAY)

    # 5) Two-alternative forced-choice with mouse response
    res = choices(sample_path, foil_path)
    correct = (res["choice_side"] == res["correct_side"])

    # 6) Color feedback
    feedback(correct)

    # 7) Log the trial
    if SAVE_CSV:
        csv_append(CSV_PATH, [
            idx,
            a_path, b_path,
            sample_path, foil_path,
            res["left_path"], res["right_path"],
            res["correct_side"], res["choice_side"],
            int(correct), f"{res['rt']:.4f}"
        ])

# Clean up
win.close()
core.quit()
print("Done.")
