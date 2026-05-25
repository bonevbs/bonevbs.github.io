#!/usr/bin/env python3
"""Backward-compatible alias for generate_publication_previews.py."""
import subprocess
import sys
from pathlib import Path

script = Path(__file__).resolve().parent / "generate_publication_previews.py"
raise SystemExit(subprocess.call([sys.executable, str(script), *sys.argv[1:]]))
