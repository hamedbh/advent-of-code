use anyhow::Result;
use rayon::prelude::*;
use std::collections::{HashMap, HashSet};

fn digit_length(n: i64) -> i64 {
    (n as f64).log10().floor() as i64 + 1
}

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
    let invalid_sum: i64 = input
        .par_iter()
        .map(|&bounds| {
            let mut local_sum = 0;
            let mut num_digits = digit_length(bounds.0);
            let mut next_boundary = 10_i64.pow(num_digits as u32);
            let mut divisor = 10_i64.pow((num_digits / 2) as u32);

            for id in bounds.0..=bounds.1 {
                if id >= next_boundary {
                    num_digits += 1;
                    next_boundary *= 10;
                    divisor = 10_i64.pow((num_digits / 2) as u32);
                }
                if num_digits % 2 != 0 {
                    continue;
                }
                let left: i64 = id / divisor;
                let right: i64 = id % divisor;
                if left == right {
                    local_sum += id
                }
            }
            local_sum
        })
        .sum();

    Ok(invalid_sum as i64)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let max_length =
        digit_length(input.iter().flat_map(|&(a, b)| [a, b]).max().unwrap());
    let powers_of_ten: Vec<i64> =
        (0..=max_length).map(|i| 10_i64.pow(i as u32)).collect();
    let all_proper_divisors: HashMap<i64, Vec<i64>> = (2..=max_length as i64)
        .map(|n| (n, proper_divisors(n)))
        .collect();
    let divisors_with_multipliers: HashMap<i64, Vec<(i64, i64)>> =
        all_proper_divisors
            .iter()
            .map(|(&num_digits, divisors)| {
                let pairs = divisors
                    .iter()
                    .map(|&d| {
                        let multiplier = (powers_of_ten[num_digits as usize]
                            - 1)
                            / (powers_of_ten[d as usize] - 1);
                        (d, multiplier)
                    })
                    .collect();
                (num_digits, pairs)
            })
            .collect();
    let invalid_sum: i64 = input
        .par_iter()
        .map(|&bounds| {
            let mut num_digits = digit_length(bounds.0);
            let mut next_boundary = 10_i64.pow(num_digits as u32);
            let mut local_sum = 0;
            for id in bounds.0..=bounds.1 {
                if id >= next_boundary {
                    num_digits += 1;
                    next_boundary *= 10;
                }
                if num_digits < 2 {
                    continue;
                }
                for &(d, multiplier) in &divisors_with_multipliers[&num_digits]
                {
                    let pattern = id / powers_of_ten[(num_digits - d) as usize];
                    let repeated = pattern * multiplier;
                    if id == repeated {
                        local_sum += id;
                        break;
                    }
                }
            }
            local_sum
        })
        .sum();

    Ok(invalid_sum)
}
