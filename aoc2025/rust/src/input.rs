use anyhow::{Context, Result};
use std::fs;
use std::time::Duration;

pub fn load_lines(day: u8, use_example: bool) -> Result<Vec<String>> {
    let paths = crate::paths::Paths::new();
    let file_path = if use_example {
        paths.examples_dir.join(format!("day{:02}.txt", day))
    } else {
        paths.inputs_dir.join(format!("day{:02}.txt", day))
    };

    let content = fs::read_to_string(&file_path)
        .with_context(|| format!("Failed to read {:?}", file_path))?;

    Ok(content.lines().map(String::from).collect())
}

pub fn save_answer<T: std::fmt::Display>(
    day: u8,
    part: u8,
    answer: T,
    use_example: bool,
) -> Result<()> {
    let paths = crate::paths::Paths::new();
    let output_dir = if use_example {
        &paths.example_outputs_dir
    } else {
        &paths.rust_outputs_dir
    };

    fs::create_dir_all(output_dir)?;
    let output_file = output_dir.join(format!("day{:02}_part{}.txt", day, part));
    fs::write(output_file, answer.to_string())?;
    Ok(())
}

pub fn save_timing(day: u8, part: u8, duration: Duration) -> Result<()> {
    let paths = crate::paths::Paths::new();
    let timings_dir = paths.timings_file.parent().unwrap();
    fs::create_dir_all(timings_dir)?;
    let file_exists = paths.timings_file.exists();
    let file = fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(&paths.timings_file)?;
    let mut wtr = csv::Writer::from_writer(file);
    // Write header if file is new
    if !file_exists {
        wtr.write_record(&["day", "language", "part", "time_seconds", "timestamp"])?;
    }
    // Write timing data
    wtr.write_record(&[
        format!("{:02}", day),
        "rust".to_string(),
        part.to_string(),
        format!("{:.6}", duration.as_secs_f64()),
        chrono::Utc::now().to_rfc3339(),
    ])?;
    wtr.flush()?;
    Ok(())
}
