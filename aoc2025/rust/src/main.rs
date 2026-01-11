use anyhow::Result;
use clap::Parser;
use std::time::Instant;

mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod day07;
mod day08;
mod day09;
mod day10;
mod input;
mod paths;

type SolveFn = fn(&[String]) -> Result<i64>;

struct Entry {
    day: u8,
    part1: SolveFn,
    part2: SolveFn,
}

static DAYS: &[Entry] = &[
    Entry {
        day: 1,
        part1: day01::solve_part1,
        part2: day01::solve_part2,
    },
    Entry {
        day: 2,
        part1: day02::solve_part1,
        part2: day02::solve_part2,
    },
    Entry {
        day: 3,
        part1: day03::solve_part1,
        part2: day03::solve_part2,
    },
    Entry {
        day: 4,
        part1: day04::solve_part1,
        part2: day04::solve_part2,
    },
    Entry {
        day: 5,
        part1: day05::solve_part1,
        part2: day05::solve_part2,
    },
    Entry {
        day: 6,
        part1: day06::solve_part1,
        part2: day06::solve_part2,
    },
    Entry {
        day: 7,
        part1: day07::solve_part1,
        part2: day07::solve_part2,
    },
    Entry {
        day: 8,
        part1: day08::solve_part1,
        part2: day08::solve_part2,
    },
    Entry {
        day: 9,
        part1: day09::solve_part1,
        part2: day09::solve_part2,
    },
    Entry {
        day: 10,
        part1: day10::solve_part1,
        part2: day10::solve_part2,
    },
];

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

    if let Some(entry) = DAYS.iter().find(|e| e.day == cli.day) {
        run_day(
            &lines,
            cli.day,
            &cli.part,
            cli.test,
            entry.part1,
            entry.part2,
        )?;
    } else {
        println!("Day {} not implemented yet", cli.day);
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
