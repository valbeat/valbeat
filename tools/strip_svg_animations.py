#!/usr/bin/env python3
"""github-readme-stats のSVGからCSSアニメーションを除去し、最終状態を静的に焼き込む。

SVG を <img> で埋め込んだ際に CSS アニメーションが動かない環境では、
opacity: 0 から fadeIn する要素が不可視のままになるため、
キャッシュ前にアニメーションを取り除いて最終状態を直接記述する。
"""
import re
import sys

RANK_CIRCLE_STATIC = ".rank-circle {{\n      stroke-dashoffset: {offset};"
RANK_TEXT_STATIC = ".rank-text {\n      transform: translate(-5px, 5px);"


def strip_animations(svg: str) -> str:
    m = re.search(
        r"@keyframes rankAnimation.*?to\s*{\s*stroke-dashoffset:\s*([\d.]+);", svg, re.S
    )
    final_offset = m.group(1) if m else None
    svg = re.sub(r"\n\s*animation:\s*[\w-]+ [^;]*;", "", svg)
    svg = svg.replace("opacity: 0;", "opacity: 1;")
    svg = re.sub(r'\s*style="animation-delay: \d+ms"', "", svg)
    if final_offset:
        rank_circle_static = RANK_CIRCLE_STATIC.format(offset=final_offset)
        if rank_circle_static not in svg:
            svg = svg.replace(".rank-circle {", rank_circle_static)
    if RANK_TEXT_STATIC not in svg:
        svg = svg.replace(".rank-text {", RANK_TEXT_STATIC)
    return svg


def main() -> int:
    has_error = False
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            svg = f.read()
        svg = strip_animations(svg)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        remaining = len(re.findall(r"animation:\s*[\w-]+\s+[^;]*;", svg))
        print(f"{path}: stripped (animation declarations remaining: {remaining})")
        if remaining:
            has_error = True
    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
