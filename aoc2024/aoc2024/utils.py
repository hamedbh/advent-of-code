from pathlib import Path


def load_data(day: int, use_example: bool = False) -> str:
    """Load input data for a given day.
    
    Args:
        day: Day number (1-25)
        use_example: If True, load example data instead of real input
        
    Returns:
        Raw input data as string
    """
    data_dir = Path(__file__).parent.parent / "data"
    
    if use_example:
        file_path = data_dir / "examples" / f"day{day:02d}.txt"
    else:
        file_path = data_dir / "inputs" / f"day{day:02d}.txt"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    return file_path.read_text().strip()


def load_lines(day: int, use_example: bool = False) -> list[str]:
    """Load input data as a list of lines."""
    return load_data(day, use_example).splitlines()


def save_answer(day: int, part: int, answer: str, use_example: bool = False) -> None:
    """Save an answer to the appropriate output file.
    
    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        answer: The answer to save
        use_example: If True, save to example_outputs, else outputs
    """
    data_dir = Path(__file__).parent.parent / "data"
    
    if use_example:
        output_dir = data_dir / "example_outputs"
    else:
        output_dir = data_dir / "outputs"
    
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"day{day:02d}_part{part}.txt"
    output_file.write_text(str(answer))