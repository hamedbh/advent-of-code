use anyhow::Result;
use good_lp::{
    Expression, Solution, SolverModel, Variable, default_solver, variable,
    variables,
};
use itertools::Itertools;
use once_cell::sync::Lazy;
use rayon::prelude::*;
use regex::Regex;
use std::collections::HashSet;

static RE: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^\[([#.]+)\] ([()\d, ]+) \{([\d,]+)\}$").unwrap()
});

pub struct Puzzle {
    lights: HashSet<u32>,
    buttons: Vec<HashSet<u32>>,
    joltages: Vec<u32>,
}

impl Puzzle {
    pub fn new(line: &str) -> Option<Self> {
        let caps = RE.captures(line)?;
        let lights: HashSet<u32> = caps
            .get(1)?
            .as_str()
            .chars()
            .enumerate()
            .filter(|(_i, c)| *c == '#')
            .map(|(i, _)| i as u32)
            .collect();
        let buttons: Vec<HashSet<u32>> = caps
            .get(2)?
            .as_str()
            .split_whitespace()
            .map(|button_str| {
                button_str
                    .trim_matches(|c| c == '(' || c == ')')
                    .split(',')
                    .filter_map(|n| n.trim().parse::<u32>().ok())
                    .collect()
            })
            .collect();
        let joltages: Vec<u32> = caps
            .get(3)?
            .as_str()
            .split(',')
            .filter_map(|n| n.trim().parse::<u32>().ok())
            .collect();

        Some(Puzzle {
            lights,
            buttons,
            joltages,
        })
    }
}

pub fn parse_input(lines: &[String]) -> Vec<Puzzle> {
    lines.iter().filter_map(|line| Puzzle::new(line)).collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let out = input
        .par_iter()
        .map(|puzzle| {
            let mut out: i64 = 0;
            let buttons = &puzzle.buttons;

            // Convert lights HashSet to a bitmask
            let lights_bits: u64 =
                puzzle.lights.iter().fold(0, |acc, &l| acc | (1 << l));
            'outer: for r in 1..=buttons.len() {
                for combo in buttons.iter().combinations(r) {
                    // XOR all button lights in one step with bits
                    let mut switched: u64 = 0;
                    for button in combo {
                        for &light in button {
                            switched ^= 1 << light;
                        }
                    }

                    // Compare bitmasks
                    if switched == lights_bits {
                        out = r as i64;
                        break 'outer;
                    }
                }
            }
            out
        })
        .sum();
    Ok(out)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let out: i64 = input
        .par_iter()
        .filter_map(|puzzle| {
            let mut vars = variables!();
            let button_vars: Vec<Variable> = (0..puzzle.buttons.len())
                .map(|_| vars.add(variable().min(0).integer()))
                .collect();
            let objective: Expression = button_vars.iter().sum();
            let mut problem = vars.minimise(objective).using(default_solver);

            // Add constraints for each joltage
            for (light_idx, &joltage) in puzzle.joltages.iter().enumerate() {
                let mut constraint_expr = Expression::from(0);
                for (button_idx, button) in puzzle.buttons.iter().enumerate() {
                    if button.contains(&(light_idx as u32)) {
                        constraint_expr += button_vars[button_idx];
                    }
                }
                problem = problem.with(constraint_expr.eq(joltage as f64));
            }

            // Solve
            let solution = problem.solve().ok()?;

            // Sum all of the button pressed
            Some(
                button_vars
                    .iter()
                    .map(|&v| solution.value(v) as i64)
                    .sum::<i64>(),
            )
        })
        .sum();
    Ok(out)
}
