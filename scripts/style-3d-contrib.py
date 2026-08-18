import os
import re

def style_3d_contrib():
    svg_path = os.path.join("profile-3d-contrib", "profile-customize.svg")
    if not os.path.exists(svg_path):
        print(f"File not found: {svg_path}")
        return

    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean style block
    clean_style = """<style>
* { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
.fill-fg { fill: #CBD5E1; }
.stroke-fg { stroke: #00E5FF; }
.fill-bg { fill: #050816; }
.stroke-bg { stroke: #1E293B; }
.fill-weak { fill: #64748B; }
.stroke-weak { stroke: #1E293B; }
.fill-strong { fill: #00E5FF; font-weight: bold; }
.radar {
  stroke-width: 3px;
  stroke: #00E5FF;
  fill: #7C3AED;
  fill-opacity: 0.45;
}
</style>"""

    if "<style>" in content and "</style>" in content:
        content = re.sub(r"<style>.*?</style>", clean_style, content, flags=re.DOTALL)
    elif "<style" in content:
        content = re.sub(r"<style[^>]*>.*?</style>", clean_style, content, flags=re.DOTALL)

    # 2. Add direct fill and stroke to all isometric block faces
    def replacer(match):
        prefix = match.group(1)  # <g transform="translate(X Y)">
        r1 = match.group(2)
        r2 = match.group(3)
        r3 = match.group(4)

        h_match = re.search(r'height="([0-9\.]+)"', r2)
        if h_match:
            h = float(h_match.group(1))
            if h <= 2.6:
                # 0 contributions -> navy base grid
                top_color = "#13233c"
                left_color = "#0e1a2d"
                right_color = "#0a1320"
                border = "#1a3154"
            elif h <= 15:
                # Level 1 -> Deep Teal
                top_color = "#00796B"
                left_color = "#00695C"
                right_color = "#004D40"
                border = "#004D40"
            elif h <= 35:
                # Level 2 -> Electric Cyan
                top_color = "#00B4D8"
                left_color = "#0096C7"
                right_color = "#0077B6"
                border = "#0077B6"
            elif h <= 55:
                # Level 3 -> Neon Cyan
                top_color = "#00E5FF"
                left_color = "#00B4D8"
                right_color = "#0096C7"
                border = "#0096C7"
            else:
                # Level 4 -> Plasma Violet
                top_color = "#A855F7"
                left_color = "#9333EA"
                right_color = "#7E22CE"
                border = "#7E22CE"

            # Strip existing fill or stroke
            r1_clean = re.sub(r'\s+(fill|stroke|stroke-width)="[^"]*"', '', r1)
            r2_clean = re.sub(r'\s+(fill|stroke|stroke-width)="[^"]*"', '', r2)
            r3_clean = re.sub(r'\s+(fill|stroke|stroke-width)="[^"]*"', '', r3)

            r1_mod = r1_clean.replace('<rect', f'<rect fill="{top_color}" stroke="{border}" stroke-width="0.3"', 1)
            r2_mod = r2_clean.replace('<rect', f'<rect fill="{left_color}" stroke="{border}" stroke-width="0.3"', 1)
            r3_mod = r3_clean.replace('<rect', f'<rect fill="{right_color}" stroke="{border}" stroke-width="0.3"', 1)

            return f'{prefix}{r1_mod}{r2_mod}{r3_mod}</g>'

        return match.group(0)

    pattern = r'(<g transform="translate\([0-9\.\s]+\)">)(<rect[^>]*></rect>)(<rect[^>]*height="[0-9\.]+"[^>]*></rect>)(<rect[^>]*></rect>)</g>'
    content = re.sub(pattern, replacer, content)

    # 3. Ensure radar chart polygon has direct presentation attributes
    if '<polygon class="radar"' in content and 'fill=' not in content.split('<polygon class="radar"')[1].split('>')[0]:
        content = content.replace('<polygon class="radar"', '<polygon class="radar" fill="#7C3AED" fill-opacity="0.45" stroke="#00E5FF" stroke-width="3"')

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully styled profile-customize.svg!")

if __name__ == "__main__":
    style_3d_contrib()
