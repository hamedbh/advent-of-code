use anyhow::Result;

pub fn parse_input(lines: &[String]) -> Vec<Vec<u32>> {
    lines
        .iter()
        .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect())
        .collect()
}

fn locate_max(batteries: &[u32]) -> (usize, u32) {
    let mut max_idx = 0;
    let mut max_val = batteries[0];
    for (i, &val) in batteries.iter().enumerate() {
        if val > max_val {
            max_idx = i;
            max_val = val;
        }
    }
    (max_idx, max_val)
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let mut total: i64 = 0;
    for bank in input {
        let left = locate_max(&bank[..bank.len() - 1]);
        let right = locate_max(&bank[left.0 + 1..]);
        total += ((10 * left.1) + right.1) as i64;
    }
    Ok(total)
}
pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let slices: Vec<usize> = (0..=11).rev().collect();
    let mut total: i64 = 0;
    for bank in input {
        let mut left_slice = 0;
        for slice in &slices {
            let (idx, val) = locate_max(&bank[left_slice..bank.len() - slice]);
            left_slice += idx + 1;
            total += val as i64 * (10_i64.pow(*slice as u32));
        }
    }
    Ok(total)
}
