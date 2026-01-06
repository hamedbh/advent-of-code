use anyhow::Result;
use std::collections::{HashMap, HashSet};

type Row = Vec<char>;

pub fn parse_input(lines: &[String]) -> Vec<Row> {
    lines.iter().map(|line| line.chars().collect()).collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let mut beams: HashSet<usize> = input[0]
        .iter()
        .enumerate()
        .filter(|&(_, &c)| c == 'S')
        .map(|(i, _)| i)
        .collect();
    let max_index = input[0].len() - 1;
    let mut split_count: i64 = 0;
    for i in 1..input.len() {
        let mut new_beams: HashSet<usize> = HashSet::new();
        for &beam_col in &beams {
            let char_below = input[i][beam_col];
            if char_below == '^' {
                split_count += 1;
                new_beams.extend([(beam_col - 1), (beam_col + 1)]);
            }
            if char_below == '.' {
                new_beams.insert(beam_col);
            }
        }
        beams = new_beams
            .iter()
            .filter(|&&beam| beam <= max_index)
            .map(|&beam| beam)
            .collect();
    }
    Ok(split_count)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let mut beams: HashMap<usize, i64> = input[0]
        .iter()
        .enumerate()
        .filter(|&(_, &c)| c == 'S')
        .map(|(i, _)| (i, 1))
        .collect();
    let max_index = input[0].len() - 1;
    for i in 1..input.len() {
        let mut new_beams: HashMap<usize, i64> = HashMap::new();
        for (&beam_col, _) in &beams {
            let char_below = input[i][beam_col];
            if char_below == '^' {
                if beam_col > 0 {
                    *new_beams.entry(beam_col - 1).or_insert(0) +=
                        beams[&beam_col];
                }
                if beam_col + 1 <= max_index {
                    *new_beams.entry(beam_col + 1).or_insert(0) +=
                        beams[&beam_col];
                }
            }
            if char_below == '.' {
                *new_beams.entry(beam_col).or_insert(0) += beams[&beam_col];
            }
        }
        beams = new_beams;
    }
    Ok(beams.values().sum())
}
