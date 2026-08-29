# Phone — assets status

---

## ✅ Done

| Asset | File | Status |
|---|---|---|
| Phone frame | `images/ui/phone.png` (+ `phone2.png` variant) | ✅ |
| All 8 app icons | `images/ui/icons/app_*.png` | ✅ |

---

## ❌ Still needed

### Phone wallpaper
Background rendered inside the phone screen, behind the app icons.

**File:** `images/ui/phone_wallpaper.png`
**Size:** 460×690 px (matches the phone display area in `phone.rpy`)

```
Night city panorama seen from above or through a window, heavily blurred bokeh,
deep navy/black tones, very low brightness (~30-40% exposure) so app icons
stay legible on top, slight vignette at the bottom, painterly or photographic style
```

**Wiring** (one line in `phone.rpy`, inside the `fixed` that holds phone content):
```renpy
# replace the implicit dark background with:
add "images/ui/phone_wallpaper.png" xpos 0 ypos 0
```
