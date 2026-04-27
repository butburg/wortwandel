import sys
from pathlib import Path


# Ensure top-level imports like "from handle_sqlite import ..." resolve in tests.
ROOT_DIR = Path(__file__).resolve().parents[1]
PYLIB_DIR = ROOT_DIR / "pylib"
if str(PYLIB_DIR) not in sys.path:
    sys.path.insert(0, str(PYLIB_DIR))
