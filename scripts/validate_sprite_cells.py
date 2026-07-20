#!/usr/bin/env python3
"""Reject sprite sheets with cell-edge clipping or substantial detached fragments."""

from __future__ import annotations

import argparse
import json
import math
from collections import deque
from pathlib import Path

from PIL import Image


def parse_hex_color(value: str) -> tuple[int, int, int]:
    normalized = value.strip().lstrip("#")
    if len(normalized) != 6:
        raise argparse.ArgumentTypeError("chroma key must be #RRGGBB")
    return tuple(int(normalized[index:index + 2], 16) for index in (0, 2, 4))


def components(mask: list[bool], width: int, height: int) -> list[int]:
    seen = bytearray(width * height)
    sizes: list[int] = []
    for start, used in enumerate(mask):
        if not used or seen[start]:
            continue
        seen[start] = 1
        queue = deque([start])
        size = 0
        while queue:
            index = queue.popleft()
            size += 1
            x, y = index % width, index // width
            for ny in range(max(0, y - 1), min(height, y + 2)):
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    neighbor = ny * width + nx
                    if mask[neighbor] and not seen[neighbor]:
                        seen[neighbor] = 1
                        queue.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sheet")
    parser.add_argument("--columns", type=int, required=True)
    parser.add_argument("--rows", type=int, required=True)
    parser.add_argument("--frame-count", type=int)
    parser.add_argument("--guard-ratio", type=float, default=0.08)
    parser.add_argument("--alpha-threshold", type=int, default=15)
    parser.add_argument("--chroma-key", type=parse_hex_color)
    parser.add_argument("--chroma-threshold", type=float, default=96.0)
    parser.add_argument("--detached-ratio", type=float, default=0.02)
    parser.add_argument("--min-detached-pixels", type=int, default=24)
    parser.add_argument("--json-out")
    args = parser.parse_args()

    sheet = Image.open(args.sheet).convert("RGBA")
    nominal_cell_width = sheet.width / args.columns
    nominal_cell_height = sheet.height / args.rows
    frame_count = args.frame_count or args.columns * args.rows
    errors: list[str] = []
    cells: list[dict[str, object]] = []

    for index in range(frame_count):
        column, row = index % args.columns, index // args.columns
        left = round(column * sheet.width / args.columns)
        top = round(row * sheet.height / args.rows)
        right = round((column + 1) * sheet.width / args.columns)
        bottom = round((row + 1) * sheet.height / args.rows)
        cell = sheet.crop((left, top, right, bottom))
        cell_width, cell_height = cell.size
        guard_x = max(1, round(cell_width * args.guard_ratio))
        guard_y = max(1, round(cell_height * args.guard_ratio))
        pixels = list(cell.getdata())
        mask = [
            alpha > args.alpha_threshold
            and (
                args.chroma_key is None
                or math.dist((red, green, blue), args.chroma_key) > args.chroma_threshold
            )
            for red, green, blue, alpha in pixels
        ]
        used = sum(mask)
        guard_pixels = sum(
            mask[y * cell_width + x]
            for y in range(cell_height)
            for x in range(cell_width)
            if x < guard_x or x >= cell_width - guard_x or y < guard_y or y >= cell_height - guard_y
        )
        component_sizes = components(mask, cell_width, cell_height)
        detached_limit = max(args.min_detached_pixels, round(used * args.detached_ratio))
        substantial = [size for size in component_sizes if size >= detached_limit]
        cell_errors: list[str] = []
        if not used:
            cell_errors.append("empty cell")
        if guard_pixels:
            cell_errors.append(f"{guard_pixels} foreground pixels enter the safety guard band")
        if len(substantial) > 1:
            cell_errors.append(f"{len(substantial)} substantial disconnected components: {substantial}")
        errors.extend(f"cell {index + 1}: {message}" for message in cell_errors)
        cells.append({
            "index": index + 1,
            "row": row,
            "column": column,
            "source_box": [left, top, right, bottom],
            "cell_size": [cell_width, cell_height],
            "guard_pixels_xy": [guard_x, guard_y],
            "foreground_pixels": used,
            "guard_pixels": guard_pixels,
            "component_sizes": component_sizes,
            "substantial_components": substantial,
            "errors": cell_errors,
        })

    report = {
        "ok": not errors,
        "sheet": str(Path(args.sheet).resolve()),
        "size": [sheet.width, sheet.height],
        "grid": [args.columns, args.rows],
        "nominal_cell_size": [nominal_cell_width, nominal_cell_height],
        "chroma_key": None if args.chroma_key is None else list(args.chroma_key),
        "cells": cells,
        "errors": errors,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
