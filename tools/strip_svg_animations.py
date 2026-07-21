#!/usr/bin/env python3
"""github-readme-stats のSVGからCSSアニメーションを除去し、最終状態を静的に焼き込む。

SVG を <img> で埋め込んだ際に CSS アニメーションが動かない環境では、
opacity: 0 から fadeIn する要素が不可視のままになるため、
キャッシュ前にアニメーションを取り除いて最終状態を直接記述する。
"""
import re
import sys


def strip_animations(svg: str) -> str:
    m = re.search(
        r"@keyframes rankAnimation.*?to\s*{\s*stroke-dashoffset:\s*([\d.]+);", svg, re.S
    )
    final_offset = m.group(1) if m else None
    svg = re.sub(r"\n\s*animation: [a-zA-Z]+ [^;]*;", "", svg)
    svg = svg.replace("opacity: 0;", "opacity: 1;")
    svg = re.sub(r'\s*style="animation-delay: \d+ms"', "", svg)
    if final_offset:
        svg = svg.replace(
            ".rank-circle {", f".rank-circle {{\n      stroke-dashoffset: {final_offset};"
        )
    svg = svg.replace(".rank-text {", ".rank-text {\n      transform: translate(-5px, 5px);")
    return svg


def main() -> int:
    for path in sys.argv[1:]:
        with open(path) as f:
            svg = f.read()
        svg = strip_animations(svg)
        with open(path, "w") as f:
            f.write(svg)
        remaining = len(re.findall(r"animation: [a-zA-Z]", svg))
        print(f"{path}: stripped (animation declarations remaining: {remaining})")
        if remaining:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
