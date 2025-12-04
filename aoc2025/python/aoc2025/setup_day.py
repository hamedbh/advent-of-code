import os

import click
import httpx

from aoc2025 import locations


def get_session_cookie() -> str:
    """Get session cookie from environment (loaded by uv from .env)."""
    session = os.getenv("AOC_SESSION")
    if not session:
        raise ValueError(
            "AOC_SESSION not found in environment. "
            "Please add your session cookie to the .env file at the "
            "project root."
        )
    return session


def download_input(year: int, day: int, session: str) -> str:
    """Download input data from Advent of Code."""
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session}

    try:
        response = httpx.get(url, cookies=cookies, timeout=10.0)
        response.raise_for_status()
        return response.text.strip()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError(
                f"Day {day} input not available yet. "
                "Check if the puzzle has been released."
            ) from e
        elif e.response.status_code == 400:
            raise ValueError(
                "Invalid session cookie. Please check your AOC_SESSION in .env"
            ) from e
        else:
            raise ValueError(f"HTTP error: {e.response.status_code}") from e
    except httpx.TimeoutException as e:
        raise ValueError("Request timed out. Please try again.") from e
    except Exception as e:
        raise ValueError(f"Failed to download input: {e}") from e


def create_python_template(day: int) -> str:
    """Create Python solution template."""
    return f'''import time

import click

from aoc2025.utils import load_lines, save_answer, save_timing


def parse_input(lines: list[str]):
    """Parse the input lines."""
    # TODO: Implement input parsing
    return lines


def solve_part1(lines: list[str]) -> int:
    """Solve part 1."""
    # input_data = parse_input(lines)
    # TODO: Implement part 1 solution
    return 0


def solve_part2(lines: list[str]) -> int:
    """Solve part 2."""
    # input_data = parse_input(lines)
    # TODO: Implement part 2 solution
    return 0


@click.command()
@click.option("--test", is_flag=True, help="Run on example data")
@click.option(
    "--part",
    type=click.Choice(["1", "2", "both"]),
    default="both",
    help="Which part to solve",
)
def main(test: bool, part: str) -> None:
    """Solve Advent of Code 2025 Day {day:02d}."""
    day = {day}
    lines = load_lines(day, use_example=test)

    if part in ("1", "both"):
        start = time.perf_counter()
        answer1 = solve_part1(lines)
        elapsed1 = time.perf_counter() - start
        print(f"Part 1: {{answer1}} ({{elapsed1:.3f}}s)")
        save_answer(day, 1, answer1, use_example=test)
        if not test:
            save_timing(day, 1, elapsed1)

    if part in ("2", "both"):
        start = time.perf_counter()
        answer2 = solve_part2(lines)
        elapsed2 = time.perf_counter() - start
        print(f"Part 2: {{answer2}} ({{elapsed2:.3f}}s)")
        save_answer(day, 2, answer2, use_example=test)
        if not test:
            save_timing(day, 2, elapsed2)


if __name__ == "__main__":
    main()
'''


@click.command()
@click.option("--day", type=int, required=True, help="Day number (1-25)")
@click.option("--year", type=int, default=2025, help="Year (default: 2025)")
def main(day: int, year: int) -> None:
    """Set up files for a new Advent of Code day."""
    if not 1 <= day <= 25:
        click.echo("Error: Day must be between 1 and 25")
        raise click.Abort()

    # Define paths
    input_file = locations.INPUTS_DIR / f"day{day:02d}.txt"
    example_file = locations.EXAMPLES_DIR / f"day{day:02d}.txt"
    python_file = (
        locations.PROJECT_ROOT / "python" / "aoc2025" / f"day{day:02d}.py"
    )

    created_files = []

    # Download input data
    if input_file.exists():
        click.echo(f"✓ Input file already exists: {input_file}")
    else:
        try:
            session = get_session_cookie()
            click.echo(f"Downloading input for day {day}...")
            input_data = download_input(year, day, session)
            input_file.write_text(input_data + "\n")
            click.echo(f"✓ Created input file: {input_file}")
            created_files.append(str(input_file))
        except Exception as e:
            click.echo(f"✗ Failed to download input: {e}", err=True)

    # Create blank example file
    if example_file.exists():
        click.echo(f"✓ Example file already exists: {example_file}")
    else:
        example_file.write_text("")
        click.echo(f"✓ Created blank example file: {example_file}")
        created_files.append(str(example_file))

    # Create Python template
    if python_file.exists():
        click.echo(f"✓ Python file already exists: {python_file}")
    else:
        template = create_python_template(day)
        python_file.write_text(template)
        click.echo(f"✓ Created Python file: {python_file}")
        created_files.append(str(python_file))

    if created_files:
        click.echo(f"\nCreated {len(created_files)} new file(s)")
    else:
        click.echo("\nAll files already exist")


if __name__ == "__main__":
    main()
