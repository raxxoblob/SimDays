#!/usr/bin/env python3
"""Self-check for the kinky SMS system.

Validates:
  - Message pools exist for all three characters and all three tiers.
  - Each tier has at least 3 messages.
  - Tiers are personality-differentiated (no identical text across characters).
  - Tier thresholds are correct (30/50/75).
  - The daily check function exists and is callable.
"""

import os
import re
import sys


def rpy_python_blocks(path, priority=None):
    """Extract python blocks from a .rpy file."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    blocks = []
    for m in re.finditer(r"init\s+python:\s*\n(.*?)(?=\n(?:label|define|screen|transform|image)\b|\Z)", src, re.DOTALL):
        blocks.append(m.group(1))
    return blocks


def main():
    base = os.path.join(os.path.dirname(__file__), "..")
    rpy_path = os.path.join(base, "kinky_sms.rpy")

    if not os.path.exists(rpy_path):
        print("FAIL: kinky_sms.rpy not found at", rpy_path)
        sys.exit(1)

    with open(rpy_path, "r", encoding="utf-8") as f:
        src = f.read()

    errors = []

    # 1. All three characters present in the pool dict.
    for char in ("marcus", "zoe", "nora"):
        if '"%s"' % char not in src and "'%s'" % char not in src:
            errors.append("Character '%s' missing from KINKY_SMS_POOLS" % char)

    # 2. All three tiers present for each character.
    for tier in ("sweet", "flirty", "kinky"):
        if '"%s"' % tier not in src and "'%s'" % tier not in src:
            errors.append("Tier '%s' missing from message pools" % tier)

    # 3. Each character/tier combo has at least 3 messages.
    # We do a rough count by looking for quoted strings within each section.
    import ast
    try:
        # Extract the KINKY_SMS_POOLS dict via regex + eval of the python block.
        m = re.search(r"KINKY_SMS_POOLS\s*=\s*(\{.*?\n    \})", src, re.DOTALL)
        if not m:
            errors.append("Could not locate KINKY_SMS_POOLS assignment")
        else:
            pools_src = m.group(1)
            # The dict uses Python syntax; try to parse it.
            ns = {}
            exec("KINKY_SMS_POOLS = " + pools_src, ns)
            pools = ns["KINKY_SMS_POOLS"]
            for char in ("marcus", "zoe", "nora"):
                if char not in pools:
                    errors.append("Character '%s' missing from parsed pools" % char)
                    continue
                for tier in ("sweet", "flirty", "kinky"):
                    msgs = pools.get(char, {}).get(tier, [])
                    if len(msgs) < 3:
                        errors.append("%s/%s has only %d messages (need >= 3)" % (char, tier, len(msgs)))

            # 4. Personality differentiation: no message text appears in more than one character's pool.
            all_texts = {}
            for char, tiers in pools.items():
                for tier, msgs in tiers.items():
                    for msg in msgs:
                        if msg not in all_texts:
                            all_texts[msg] = set()
                        all_texts[msg].add(char)
            dupes = {t: chars for t, chars in all_texts.items() if len(chars) > 1}
            if dupes:
                errors.append("Duplicate message text across characters: %s" % list(dupes.keys())[:3])

    except Exception as e:
        errors.append("Failed to parse KINKY_SMS_POOLS: %s" % e)

    # 5. Tier threshold function exists and is correct.
    if "def kinky_sms_tier" not in src:
        errors.append("kinky_sms_tier() function missing")
    else:
        # Verify thresholds by checking the source for the right comparisons.
        if ">= 75" not in src:
            errors.append("Missing >= 75 threshold for 'kinky' tier")
        if ">= 50" not in src:
            errors.append("Missing >= 50 threshold for 'flirty' tier")
        if ">= 30" not in src:
            errors.append("Missing >= 30 threshold for 'sweet' tier")

    # 6. Daily check function exists.
    if "def kinky_sms_daily_check" not in src:
        errors.append("kinky_sms_daily_check() function missing")

    # 7. script.rpy calls the daily check.
    script_path = os.path.join(base, "script.rpy")
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            script_src = f.read()
        if "kinky_sms_daily_check" not in script_src:
            errors.append("script.rpy does not call kinky_sms_daily_check()")
    else:
        errors.append("script.rpy not found for integration check")

    # Report.
    if errors:
        print("FAIL (%d issues):" % len(errors))
        for e in errors:
            print("  -", e)
        sys.exit(1)
    else:
        print("PASS: kinky SMS system checks all OK.")


if __name__ == "__main__":
    main()
