"""Central location for all project paths."""

from pathlib import Path

# Configuration constants
TIMINGS_FILENAME = "timings.csv"


def find_project_root() -> Path:
    """Find project root by looking for .venv directory.

    Returns:
        Path to project root directory

    Raises:
        RuntimeError: If project root cannot be found
    """
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".venv").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find project root (no .venv found)")


# Project paths
PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
INPUTS_DIR = DATA_DIR / "inputs"
EXAMPLES_DIR = DATA_DIR / "examples"
OUTPUTS_DIR = DATA_DIR / "outputs"
EXAMPLE_OUTPUTS_DIR = DATA_DIR / "example_outputs"
TIMINGS_DIR = DATA_DIR / "timings"
TIMINGS_FILE = TIMINGS_DIR / TIMINGS_FILENAME
