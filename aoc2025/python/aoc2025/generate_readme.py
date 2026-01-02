import csv

from aoc2025 import locations


def get_all_timings() -> dict[tuple[int, int, str], float]:
    """Get the most recent timing for each day/part/language combination.

    Returns:
        Dict mapping (day, part, language) to time in seconds
    """
    timings_file = locations.TIMINGS_FILE

    if not timings_file.exists():
        return {}

    timings = {}
    with open(timings_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (int(row["day"]), int(row["part"]), row["language"])
            # Always update with latest (CSV appends, so last is newest)
            timings[key] = float(row["time_seconds"])

    return timings


def get_answers() -> dict[tuple[int, int], str]:
    """Get all answers from output files.

    Returns:
        Dict mapping (day, part) to answer
    """
    outputs_dir = locations.OUTPUTS_DIR

    if not outputs_dir.exists():
        return {}

    answers = {}
    for output_file in sorted(outputs_dir.glob("*/day*_part*.txt")):
        # Parse filename: day01_part1.txt
        parts = output_file.stem.split("_")
        day = int(parts[0].replace("day", ""))
        part = int(parts[1].replace("part", ""))

        answer = output_file.read_text().strip()
        answers[(day, part)] = answer

    return answers


def get_available_languages(timings: dict) -> list[str]:
    """Extract all unique languages from timings data.

    Returns:
        Sorted list of language names
    """
    languages = set()
    for _, _, lang in timings.keys():
        languages.add(lang)
    return sorted(languages)


def generate_readme() -> str:
    """Generate the complete README content."""
    answers = get_answers()
    timings = get_all_timings()
    languages = get_available_languages(timings)

    # Find all completed days
    completed_days = set()
    for day, _ in answers.keys():
        completed_days.add(day)

    # Header
    readme = """# Advent of Code 2025

Solutions for [Advent of Code 2025](https://adventofcode.com/2025).

"""

    # Generate section for each completed day
    for day in sorted(completed_days):
        # Count stars
        has_part1 = (day, 1) in answers
        has_part2 = (day, 2) in answers
        stars = ""
        if has_part1 and has_part2:
            stars = " ⭐⭐"
        elif has_part1:
            stars = " ⭐"

        readme += f"## Day {day:02d}{stars}\n\n"

        # Create table header with columns for each language
        readme += "| Part | Answer |"
        for lang in languages:
            readme += f" {lang.capitalize()} (s) |"
        readme += " Rust speedup |"
        readme += "\n"

        # Table separator
        readme += "|------|--------|"
        for _ in languages:
            readme += "----------|"
        readme += "---------|"
        readme += "\n"

        # Add rows for each part
        for part in [1, 2]:
            if (day, part) in answers:
                answer = answers[(day, part)]
                readme += f"| {part} | {answer} |"

                # Add timing for each language
                for lang in languages:
                    time_key = (day, part, lang)
                    if time_key in timings:
                        readme += f" {timings[time_key]:.6f} |"
                    else:
                        readme += " N/A |"

                # Calculate speedup (Python / Rust)
                python_time = timings.get((day, part, "python"))
                rust_time = timings.get((day, part, "rust"))
                if python_time and rust_time:
                    speedup = python_time / rust_time
                    readme += f" {speedup:.1f}x |"
                else:
                    readme += " |"

                readme += "\n"

        readme += "\n---\n\n"

    return readme


def main():
    """Generate and write README.md."""
    readme_content = generate_readme()
    readme_path = locations.PROJECT_ROOT / "README.md"
    readme_path.write_text(readme_content)
    print(f"Generated {readme_path}")


if __name__ == "__main__":
    main()
