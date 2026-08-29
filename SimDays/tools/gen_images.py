"""
gen_images.py — batch image-gen browser automation
===================================================

Reads a prompts file, pastes each prompt into successive browser tabs,
waits for generation, repeats.

PROMPTS FILE FORMAT
-------------------
## SCENE: scene_name        <- scene header (optional, for organisation)
prompt text line 1
prompt text continues
--                          <- separator between individual prompts
next prompt text
--
...

## SCENE: another_scene
...

USAGE
-----
python gen_images.py prompts.txt [options]

Options:
  --tabs N          Number of browser tabs to use (default: 5)
  --start-tab N     First tab number in Chrome (Ctrl+N), default: 2
  --wait N          Seconds to wait after filling all tabs (default: 180)
  --delay N         Seconds between keystrokes within a tab (default: 0.6)
  --pause N         Seconds before script starts (time to focus browser, default: 4)
  --submit enter|none   How to submit (default: enter)
  --focus click     Click input field before pasting (default, recommended)
  --focus tab       Press Tab key to find input field instead of clicking
  --focus none      Don't try to focus (input already active)
  --click-x N       Horizontal position of input click, % of screen width (default: 50)
  --click-y N       Vertical position of input click, % of screen height (default: 88)
  --dry-run         Print prompts without doing anything

FINDING THE RIGHT --click-x / --click-y
-----------------------------------------
Run with --dry-run first, then open your generator in the browser,
move your mouse to the centre of the input field, and check the coordinates
with the helper:
    python gen_images.py --find-click

INSTALL
-------
pip install pyautogui pyperclip
"""

import sys
import time
import argparse
import platform
import pyautogui
import pyperclip

pyautogui.FAILSAFE = True   # move mouse to top-left corner to abort

# Mac uses Command; Windows/Linux use Ctrl
MOD = "command" if platform.system() == "Darwin" else "ctrl"


# ── Prompt parser ────────────────────────────────────────────────────────────

def parse_prompts(path):
    """Return list of (scene_name, prompt_text) tuples."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    results = []

    blocks = raw.split("\n## SCENE:")
    for i, block in enumerate(blocks):
        if i == 0 and not block.lstrip().startswith("## SCENE:"):
            scene_name = "default"
            body = block
        else:
            lines = block.strip().split("\n", 1)
            scene_name = lines[0].strip()
            body = lines[1] if len(lines) > 1 else ""

        for p in body.split("\n--\n"):
            p = p.strip()
            if p:
                results.append((scene_name, p))

    return results


# ── Screen helpers ───────────────────────────────────────────────────────────

def screen_point(pct_x, pct_y):
    """Convert percentage (0–100) to absolute screen pixels."""
    w, h = pyautogui.size()
    return int(w * pct_x / 100), int(h * pct_y / 100)


def focus_input(mode, click_x_pct, click_y_pct, delay):
    if mode == "none":
        return
    if mode == "tab":
        time.sleep(delay)
        pyautogui.press("tab")
        time.sleep(delay)
    else:  # click (default)
        x, y = screen_point(click_x_pct, click_y_pct)
        time.sleep(delay)
        pyautogui.click(x, y)
        time.sleep(delay)


# ── Core automation ──────────────────────────────────────────────────────────

def switch_tab(tab_number):
    pyautogui.hotkey(MOD, str(tab_number))


def send_prompt(text, focus_mode, click_x, click_y, delay, submit):
    focus_input(focus_mode, click_x, click_y, delay)

    # Select all existing text and replace (in case field wasn't empty)
    pyautogui.hotkey(MOD, "a")
    time.sleep(0.2)

    pyperclip.copy(text)
    pyautogui.hotkey(MOD, "v")
    time.sleep(delay)

    if submit == "enter":
        pyautogui.press("enter")


def run(prompts, args):
    tabs      = args.tabs
    start_tab = args.start_tab
    wait_secs = args.wait
    delay     = args.delay
    submit    = args.submit
    focus     = args.focus
    cx        = args.click_x
    cy        = args.click_y

    total = len(prompts)
    print(f"\n{total} prompts | {tabs} tabs | {wait_secs}s wait | "
          f"focus={focus}" + (f" at ({cx}%, {cy}%)" if focus == "click" else ""))
    print(f"Starting in {args.pause}s — switch to your browser now…\n")
    time.sleep(args.pause)

    batch_num = 0
    i = 0
    while i < total:
        batch = prompts[i : i + tabs]
        batch_num += 1
        print(f"── Batch {batch_num}  [{i+1}–{i+len(batch)} / {total}] ──")

        for offset, (scene, prompt) in enumerate(batch):
            tab_n = start_tab + offset
            short = prompt[:70].replace("\n", " ")
            print(f"  Tab {tab_n}  {scene}  |  {short}…")
            switch_tab(tab_n)
            send_prompt(prompt, focus, cx, cy, delay, submit)

        i += tabs

        if i < total:
            print(f"\n  Waiting {wait_secs}s for generation…")
            elapsed = 0
            step = 30
            while elapsed < wait_secs:
                chunk = min(step, wait_secs - elapsed)
                time.sleep(chunk)
                elapsed += chunk
                remaining = wait_secs - elapsed
                if remaining > 0:
                    print(f"    {remaining}s left…")
            print("  Done. Next batch.\n")

    print("\n✓ All prompts sent.")


# ── CLI ──────────────────────────────────────────────────────────────────────

def find_click_helper():
    """Print current mouse position every second so user can find coordinates."""
    w, h = pyautogui.size()
    print(f"Screen: {w}×{h}px")
    print("Move mouse to your input field. Ctrl+C to stop.\n")
    try:
        while True:
            x, y = pyautogui.position()
            pct_x = round(x / w * 100, 1)
            pct_y = round(y / h * 100, 1)
            print(f"  x={x} y={y}  →  --click-x {pct_x} --click-y {pct_y}", end="\r")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nUse those values in --click-x / --click-y")


def main():
    if "--find-click" in sys.argv:
        find_click_helper()
        return

    ap = argparse.ArgumentParser(description="Batch image-gen browser automation")
    ap.add_argument("file",          help="Prompts file path")
    ap.add_argument("--tabs",        type=int,   default=5)
    ap.add_argument("--start-tab",   type=int,   default=2)
    ap.add_argument("--wait",        type=int,   default=180)
    ap.add_argument("--delay",       type=float, default=0.6)
    ap.add_argument("--pause",       type=int,   default=4)
    ap.add_argument("--submit",      default="enter", choices=["enter", "none"])
    ap.add_argument("--focus",       default="click", choices=["click", "tab", "none"])
    ap.add_argument("--click-x",     type=float, default=50,
                    help="Input field horizontal position, %% of screen width (default 50)")
    ap.add_argument("--click-y",     type=float, default=88,
                    help="Input field vertical position, %% of screen height (default 88)")
    ap.add_argument("--dry-run",     action="store_true")
    args = ap.parse_args()

    prompts = parse_prompts(args.file)
    if not prompts:
        print("No prompts found. Check file format.")
        sys.exit(1)

    by_scene = {}
    for scene, _ in prompts:
        by_scene[scene] = by_scene.get(scene, 0) + 1
    print(f"Loaded {len(prompts)} prompts:")
    for scene, count in by_scene.items():
        print(f"  {scene}: {count}")

    if args.dry_run:
        print("\n── DRY RUN ──")
        for i, (scene, p) in enumerate(prompts, 1):
            print(f"\n[{i}] {scene}\n{p}")
        return

    run(prompts, args)


if __name__ == "__main__":
    main()
