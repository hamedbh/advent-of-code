import csv
import json
from datetime import datetime
from typing import Any

from aoc2025 import locations


def load_data(day: int, use_example: bool = False) -> str:
    """Load input data for a given day.

    Args:
        day: Day number (1-25)
        use_example: If True, load example data instead of real input

    Returns:
        Raw input data as string
    """
    if use_example:
        file_path = locations.EXAMPLES_DIR / f"day{day:02d}.txt"
    else:
        file_path = locations.INPUTS_DIR / f"day{day:02d}.txt"

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    return file_path.read_text().strip()


def load_lines(day: int, use_example: bool = False) -> list[str]:
    """Load input data as a list of lines."""
    return load_data(day, use_example).splitlines()


def save_answer(
    day: int, part: int, answer: Any, use_example: bool = False
) -> None:
    """Save an answer to the appropriate output file.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        answer: The answer to save
        use_example: If True, save to example_outputs, else outputs
    """
    # Validate before saving
    validate_answer(day, part, answer, use_example=use_example)

    if use_example:
        output_dir = locations.EXAMPLE_OUTPUTS_DIR
    else:
        output_dir = locations.PYTHON_OUTPUTS_DIR

    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"day{day:02d}_part{part}.txt"
    output_file.write_text(str(answer))


def save_timing(
    day: int, part: int, time_seconds: float, language: str = "python"
) -> None:
    """Save timing data to CSV file.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        time_seconds: Execution time in seconds
        language: Programming language used (default: "python")
    """
    locations.TIMINGS_DIR.mkdir(exist_ok=True)
    csv_file = locations.TIMINGS_FILE
    file_exists = csv_file.exists()

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)

        # Write header if file is new
        if not file_exists:
            writer.writerow(
                ["day", "language", "part", "time_seconds", "timestamp"]
            )

        # Write timing data
        writer.writerow(
            [
                f"{day:02d}",
                language,
                part,
                f"{time_seconds:.6f}",
                datetime.now().isoformat(),
            ]
        )


def load_expected_answers() -> dict[int, dict[int, int]]:
    """Load expected answers from JSON.

    Returns:
        Dictionary mapping day -> {part1: answer, part2: answer}
    """
    answers_file = locations.ANSWERS_FILE
    try:
        with open(answers_file) as f:
            out = json.load(f)
            return {
                int(day): {int(part): answer for part, answer in v.items()}
                for day, v in out.items()
            }
    except FileNotFoundError:
        return {}


def validate_answer(
    day: int, part: int, answer: int, use_example: bool = False
) -> bool:
    """Validate an answer against expected value.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        answer: The computed answer
        use_example: If True, skip validation (examples have different answers)

    Returns:
        True if validation passes

    Raises:
        ValueError: If answer doesn't match expected value
    """
    if use_example:
        return True  # Don't validate the test examples

    expected_answers = load_expected_answers()

    if day not in expected_answers:
        return True  # No expected answer stored yet

    if part not in expected_answers[day]:
        return True  # No expected answer for this part yet

    expected = expected_answers[day][part]

    if answer != expected:
        raise ValueError(
            f"Day {day} Part {part} validation failed! "
            f"Expected {expected}, got {answer}"
        )

    return True
