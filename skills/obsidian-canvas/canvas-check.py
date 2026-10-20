"""Check an Obsidian .canvas against the obsidian-canvas skill (SKILL.md next to this file). Usage: py canvas-check.py <file.canvas>"""
import json
import math
import sys

CHAR_PX = 8.4          # average glyph width at 16px body text
CODE_CHAR_PX = 9.4     # monospace inline code
HEADING_CHAR_PX = 13.5
PAD_X = 48             # left + right content padding
PAD_Y = 28             # top + bottom content padding
LINE_PX = 26
HEADING_PX = 48
CLEARANCE = 12         # free space a line keeps around every block


def text_width_px(line):
    if line.startswith("## "):
        return len(line[3:]) * HEADING_CHAR_PX
    code_chars = sum(len(part) for i, part in enumerate(line.split("`")) if i % 2 == 1)
    plain_chars = len(line.replace("`", "")) - code_chars
    return plain_chars * CHAR_PX + code_chars * CODE_CHAR_PX + line.count("`") // 2 * 6


def needed_height(text, width):
    if not text.strip():
        return 0
    height = PAD_Y
    for line in text.split("\n"):
        wrapped = max(1, math.ceil(text_width_px(line) / (width - PAD_X)))
        height += (HEADING_PX if line.startswith("## ") else LINE_PX) * wrapped
    return height


def side_point(node, side):
    x, y, w, h = node["x"], node["y"], node["width"], node["height"]
    return {"top": (x + w / 2, y), "bottom": (x + w / 2, y + h),
            "left": (x, y + h / 2), "right": (x + w, y + h / 2)}[side]


def segment_hits_rect(p1, p2, node, margin):
    left, top = node["x"] - margin, node["y"] - margin
    right, bottom = node["x"] + node["width"] + margin, node["y"] + node["height"] + margin
    (x1, y1), (x2, y2) = p1, p2
    if abs(x1 - x2) < 0.5:
        return left < x1 < right and max(min(y1, y2), top) < min(max(y1, y2), bottom)
    if abs(y1 - y2) < 0.5:
        return top < y1 < bottom and max(min(x1, x2), left) < min(max(x1, x2), right)
    return True  # diagonal segments are reported separately


def facing(from_side, to_side, p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    pairs = {("right", "left"): x2 > x1 and abs(y1 - y2) < 0.5,
             ("left", "right"): x2 < x1 and abs(y1 - y2) < 0.5,
             ("bottom", "top"): y2 > y1 and abs(x1 - x2) < 0.5,
             ("top", "bottom"): y2 < y1 and abs(x1 - x2) < 0.5}
    return pairs.get((from_side, to_side), False)


def check(path):
    canvas = json.load(open(path, encoding="utf-8"))
    nodes = {n["id"]: n for n in canvas["nodes"]}
    blocks = [n for n in canvas["nodes"] if n["type"] != "group"]
    problems = []
    for node in blocks:
        need = needed_height(node.get("text", ""), node["width"])
        if need > node["height"]:
            problems.append(f"scroll: {node['id']} needs ~{need:.0f}px, has {node['height']}")
    for i, a in enumerate(blocks):
        for b in blocks[i + 1:]:
            if (a["x"] < b["x"] + b["width"] and b["x"] < a["x"] + a["width"]
                    and a["y"] < b["y"] + b["height"] and b["y"] < a["y"] + a["height"]):
                problems.append(f"overlap: {a['id']} / {b['id']}")
    for edge in canvas["edges"]:
        if edge.get("label"):
            problems.append(f"label on line: {edge['id']} '{edge['label']}'")
        a, b = nodes[edge["fromNode"]], nodes[edge["toNode"]]
        p1, p2 = side_point(a, edge["fromSide"]), side_point(b, edge["toSide"])
        if not facing(edge["fromSide"], edge["toSide"], p1, p2):
            problems.append(f"not straight: {edge['id']} ({edge['fromSide']} -> {edge['toSide']})")
            continue
        for node in blocks:
            if node["id"] in (a["id"], b["id"]):
                continue
            if segment_hits_rect(p1, p2, node, CLEARANCE):
                problems.append(f"line over block: {edge['id']} crosses {node['id']}")
    edge_count = len(canvas["edges"])
    print(f"{path}: {len(blocks)} blocks, {edge_count} lines, {len(problems)} problems")
    for problem in problems:
        print("  " + problem)
    return not problems


if __name__ == "__main__":
    sys.exit(0 if check(sys.argv[1]) else 1)
