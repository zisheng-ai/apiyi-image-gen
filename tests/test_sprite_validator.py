#!/usr/bin/env python3
"""Regression tests for the sprite-sheet delivery gate."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    PIL_AVAILABLE = False
else:
    PIL_AVAILABLE = True


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_sprite_cells.py"


@unittest.skipUnless(PIL_AVAILABLE, "Pillow is required; install requirements.txt")
class SpriteValidatorTests(unittest.TestCase):
    def make_sheet(self, path: Path, *, clipped: bool = False) -> None:
        image = Image.new("RGBA", (80, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        for row in range(3):
            for column in range(4):
                left, top = column * 20, row * 20
                if clipped and row == 0 and column == 0:
                    draw.rectangle((left, top + 8, left + 5, top + 12), fill="white")
                else:
                    draw.rectangle((left + 8, top + 8, left + 12, top + 12), fill="white")
        image.save(path)

    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_accepts_a_clean_sheet_and_writes_nested_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sheet = root / "clean.png"
            report = root / "reports" / "validation.json"
            self.make_sheet(sheet)

            result = self.run_validator(
                str(sheet), "--columns", "4", "--rows", "3", "--json-out", str(report)
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(report.exists())
            self.assertTrue(json.loads(report.read_text())["ok"])

    def test_rejects_foreground_that_enters_a_cell_guard_band(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sheet = Path(directory) / "clipped.png"
            self.make_sheet(sheet, clipped=True)

            result = self.run_validator(str(sheet), "--columns", "4", "--rows", "3")

            self.assertEqual(result.returncode, 1)
            self.assertIn("safety guard band", result.stdout)

    def test_rejects_invalid_grid_arguments_before_processing_an_image(self) -> None:
        result = self.run_validator("missing.png", "--columns", "0", "--rows", "3")

        self.assertEqual(result.returncode, 2)
        self.assertIn("must be positive", result.stderr)

    def test_rejects_an_out_of_range_frame_count(self) -> None:
        result = self.run_validator(
            "missing.png", "--columns", "4", "--rows", "3", "--frame-count", "13"
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("between 1 and columns", result.stderr)


if __name__ == "__main__":
    unittest.main()
