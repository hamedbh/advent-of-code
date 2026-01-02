use anyhow::Result;
use std::collections::{HashMap, HashSet};

fn proper_divisors(n: i64) -> Vec<i64> {
    if n <= 1 {
        return Vec::new();
    }

    let mut divisors = HashSet::new();
    // 1 is always a divisor
    divisors.insert(1);

    let upper_bound = (n as f64).sqrt() as i64;
    for i in 2..=upper_bound {
        if n % i == 0 {
            divisors.insert(i);
            divisors.insert(n / i);
        }
    }

    let mut result: Vec<i64> = divisors.into_iter().collect();
    result.sort();
    result
}

pub fn parse_input(lines: &[String]) -> Vec<(i64, i64)> {
    assert!(lines.len() == 1);
    lines[0]
        .split(",")
        .map(|s| {
            let (first, second) = s.split_once("-").unwrap();
            (
                first.parse::<i64>().unwrap(),
                second.parse::<i64>().unwrap(),
            )
        })
        .collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let mut invalid_sum: i64 = 0;
    for bounds in input {
        for id in bounds.0..=bounds.1 {
            let idstring = id.to_string();
            let num_digits = idstring.len();
            if num_digits % 2 != 0 {
                continue;
            }
            if &idstring[0..num_digits / 2] == &idstring[num_digits / 2..] {
                invalid_sum += id
            }
        }
    }

    Ok(invalid_sum as i64)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let max_length = input
        .iter()
        .flat_map(|&(a, b)| [a, b])
        .max()
        .unwrap()
        .to_string()
        .len();
    let all_proper_divisors: HashMap<i64, Vec<i64>> = (2..=max_length as i64)
        .map(|n| (n, proper_divisors(n)))
        .collect();
    let mut invalid_sum: i64 = 0;
    for bounds in input {
        for id in bounds.0..=bounds.1 {
            let idstring = id.to_string();
            let num_digits: i64 = idstring.len() as i64;
            if num_digits < 2 {
                continue;
            }
            for &d in &all_proper_divisors[&num_digits] {
                if &idstring == &idstring[0..d as usize].repeat((num_digits / d) as usize) {
                    invalid_sum += id;
                    break;
                }
            }
        }
    }

    Ok(invalid_sum as i64)
}
