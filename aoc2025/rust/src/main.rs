use anyhow::Result;
use clap::Parser;
use std::time::Instant;

mod day01;
mod input;
mod paths;

#[derive(Parser)]
#[command(name = "aoc2025")]
#[command(about = "Advent of Code 2025 - Rust")]
struct Cli {
    /// Day to run (1-25)
    #[arg(short, long)]
    day: u8,

    /// Use example data
    #[arg(short, long)]
    test: bool,

    /// Which part to solve (1, 2, or both)
    #[arg(short, long, default_value = "both")]
    part: String,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    let lines = input::load_lines(cli.day, cli.test)?;

    match cli.day {
        1 => run_day(
            &lines,
            cli.day,
            &cli.part,
            cli.test,
            day01::solve_part1,
            day01::solve_part2,
        )?,
        _ => println!("Day {} not implemented yet", cli.day),
    }

    Ok(())
}

fn run_day<F1, F2>(
    lines: &[String],
    day: u8,
    part: &str,
    test: bool,
    solve1: F1,
    solve2: F2,
) -> Result<()>
where
    F1: Fn(&[String]) -> Result<i64>,
    F2: Fn(&[String]) -> Result<i64>,
{
    if part == "1" || part == "both" {
        let start = Instant::now();
        let answer = solve1(lines)?;
        let elapsed = start.elapsed();
        println!("Part 1: {} ({:.3}s)", answer, elapsed.as_secs_f64());
        input::save_answer(day, 1, answer, test)?;
        if !test {
            input::save_timing(day, 1, elapsed)?;
        }
    }

    if part == "2" || part == "both" {
        let start = Instant::now();
        let answer = solve2(lines)?;
        let elapsed = start.elapsed();
        println!("Part 2: {} ({:.3}s)", answer, elapsed.as_secs_f64());
        input::save_answer(day, 2, answer, test)?;
        if !test {
            input::save_timing(day, 2, elapsed)?;
        }
    }

    Ok(())
}
