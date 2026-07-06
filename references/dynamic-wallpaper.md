# Mac Dynamic Wallpaper — Generation & Packaging

Mac dynamic wallpapers are `.heic` files containing multiple frames + Apple-proprietary XMP metadata (`apple_desktop:h24`). macOS switches frames based on time of day.

**Tool stack (no Homebrew needed):**
- `pillow-heif` 1.1.1 (already installed) — handles HEIC read/write + XMP
- `plistlib` + `base64` — standard library, generates the h24 metadata

---

## Setup Check

```bash
python3 -c "import pillow_heif; print('OK', pillow_heif.__version__)" || \
  pip3 install pillow-heif -q
```

---

## Frame Strategy — 8 Frames, 24 Hours

Generate 8 frames in parallel. Each frame = same subject, different lighting/time.

| Frame | Time  | t value | Light condition |
|-------|-------|---------|-----------------|
| 0     | 00:00 | 0.0     | Deep night, moonlit, stars |
| 1     | 03:00 | 0.125   | Pre-dawn blue-black |
| 2     | 06:00 | 0.25    | Sunrise, warm gold horizon |
| 3     | 09:00 | 0.375   | Bright morning, soft shadows |
| 4     | 12:00 | 0.5     | Midday, harsh overhead light |
| 5     | 15:00 | 0.625   | Warm afternoon, long shadows |
| 6     | 18:00 | 0.75    | Golden hour, sunset |
| 7     | 21:00 | 0.875   | Blue hour, twilight |

**Metadata:** `l=4` (light mode → noon), `d=0` (dark mode → midnight)

---

## Prompt Template

Append the lighting suffix to the user's theme prompt for each frame:

```
THEME="<user's wallpaper subject, e.g. 'misty mountain forest, photorealistic, 4K'>"

declare -A SUFFIXES=(
  [0]="deep night, moonlit sky, stars, no sunlight"
  [1]="pre-dawn, dark blue sky, very faint horizon glow"
  [2]="sunrise, golden orange light on the horizon, long shadows"
  [3]="bright morning, clear sky, soft warm sunlight"
  [4]="midday, overhead sunlight, high contrast, vivid colors"
  [5]="late afternoon, warm directional light, long golden shadows"
  [6]="sunset, golden hour, orange and purple sky"
  [7]="twilight, blue hour, dusk, fading light"
)
```

---

## Generation — Parallel, 8 Frames

Size: GPT at `3840x2160` (16:9 4K) → Doubao fallback at `2560x1600` → Nano at `1280x720`.

```bash
OUT_DIR="$HOME/.zisheng-ai/dynamic-wallpaper"
mkdir -p "$OUT_DIR"
PIDS=()

for i in 0 1 2 3 4 5 6 7; do
  (
    PROMPT="${THEME}, ${SUFFIXES[$i]}, no text, no watermark"
    OUTPUT_PATH="/tmp/dw_frame_${i}.png"

    if   gen_image_apiyi "$MODEL_GPT"    "3840x2160" "$OUTPUT_PATH"; then MODEL_USED="$MODEL_GPT"
    elif gen_image_apiyi "$MODEL_GPT"    "3840x2160" "$OUTPUT_PATH"; then MODEL_USED="$MODEL_GPT"
    elif gen_image_apiyi "$MODEL_DOUBAO" "2560x1600" "$OUTPUT_PATH"; then MODEL_USED="$MODEL_DOUBAO"
    elif gen_image_apiyi "$MODEL_NANO"   "1280x720"  "$OUTPUT_PATH"; then MODEL_USED="$MODEL_NANO"
    else echo "⚠ frame $i — all models failed"; exit 0; fi

    # Nano: upscale to 2560x1600
    if [ "$MODEL_USED" = "$MODEL_NANO" ]; then
      sips -z 1600 2560 "$OUTPUT_PATH" >/dev/null
    fi

    echo "✓ frame $i  ($MODEL_USED)"
  ) > "/tmp/dw_log_${i}.log" 2>&1 &
  PIDS+=($!)
done

wait "${PIDS[@]}"
cat /tmp/dw_log_*.log
rm -f /tmp/dw_log_*.log
```

Verify all 8 frames exist before packaging:

```bash
MISSING=()
for i in 0 1 2 3 4 5 6 7; do
  [ -f "/tmp/dw_frame_${i}.png" ] || MISSING+=($i)
done
if [ ${#MISSING[@]} -gt 0 ]; then
  echo "⚠ Missing frames: ${MISSING[*]} — cannot package"
  exit 1
fi
```

---

## Packaging — PNG Frames → HEIC with h24 Metadata

Run this Python script after all frames are ready:

```python
#!/usr/bin/env python3
import sys, plistlib, base64, os
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

frame_paths = [f"/tmp/dw_frame_{i}.png" for i in range(8)]
output = os.path.expanduser("~/.zisheng-ai/dynamic-wallpaper/wallpaper.heic")
os.makedirs(os.path.dirname(output), exist_ok=True)

n = len(frame_paths)
si = [{"i": i, "t": round(i / n, 8)} for i in range(n)]
plist_data = plistlib.dumps({"ap": {"l": 4, "d": 0}, "si": si}, fmt=plistlib.FMT_BINARY)
h24 = base64.b64encode(plist_data).decode()

xmp = (
    '<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>'
    '<x:xmpmeta xmlns:x="adobe:ns:meta/">'
    '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
    '<rdf:Description rdf:about="" xmlns:apple_desktop="http://ns.apple.com/namespace/1.0/">'
    f'<apple_desktop:h24>{h24}</apple_desktop:h24>'
    '</rdf:Description></rdf:RDF></x:xmpmeta>'
    '<?xpacket end="w"?>'
)

images = [Image.open(p).convert("RGB") for p in frame_paths]
images[0].save(output, format="HEIF", save_all=True, append_images=images[1:], xmp=xmp.encode())

size_kb = os.path.getsize(output) // 1024
print(f"✓ {output}  ({n} frames, {size_kb} KB)")
```

Run it:

```bash
python3 -c "$(cat <<'PYEOF'
# paste the script above here, or save it to /tmp/pack_heic.py and run:
PYEOF
)"
# OR
python3 /tmp/pack_heic.py
```

Clean up temp PNGs after packaging:

```bash
rm -f /tmp/dw_frame_*.png
```

---

## Set as Dynamic Wallpaper

```bash
HEIC="$HOME/.zisheng-ai/dynamic-wallpaper/wallpaper.heic"
open "$HEIC"
```

After opening, ask: **「要设置为桌面壁纸吗？」** Wait for confirmation, then:

```bash
osascript -e "tell application \"Finder\" to set desktop picture to POSIX file \"$HOME/.zisheng-ai/dynamic-wallpaper/wallpaper.heic\""
```

---

## Full Pipeline Summary

```
1. Load generation.md → model alias resolution
2. Build THEME + SUFFIXES[0..7]
3. gen_image_apiyi × 8 in parallel → /tmp/dw_frame_{0..7}.png
4. Verify all 8 frames exist
5. Run Python packaging script → ~/.zisheng-ai/dynamic-wallpaper/wallpaper.heic
6. open + ask to set as wallpaper
```

**Cost estimate:** 8 × GPT Image 2 at 3840×2160 ≈ 8 API calls. If budget is a concern, use Doubao as primary (set `export APIYI_MODEL=doubao`) for 2560×1600 frames.

---

## Output Convention (Dynamic Wallpaper)

- **Format:** `.heic` (HEIF multi-image, lossless PNG quality per frame)
- **No WebP conversion** — HEIC is the deliverable
- **No intermediate PNG cleanup** until packaging is confirmed successful
- **Location:** `~/.zisheng-ai/dynamic-wallpaper/wallpaper.heic`
