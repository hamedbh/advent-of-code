use anyhow::Result;
use once_cell::sync::Lazy;
use regex::Regex;

static RE: Lazy<Regex> = Lazy::new(|| Regex::new(r"\d+").unwrap());

pub fn parse_input(lines: &[String]) -> (&[String], &[String]) {
    let mut boundary: usize = 0;
    for (i, line) in lines.iter().enumerate() {
        if line.contains('x') {
            boundary = i;
            break;
        }
    }
    (&lines[0..boundary], &lines[boundary..lines.len()])
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let (_, regions) = parse_input(lines);
    let out: i64 = regions
        .iter()
        .map(|region| {
            let nums: Vec<i64> = RE
                .find_iter(region)
                .filter_map(|m| m.as_str().parse().ok())
                .collect();
            let mut res = 0;
            if let [i, j, counts @ ..] = nums.as_slice() {
                if (i / 3) * (j / 3) >= counts.iter().sum::<i64>() {
                    res += 1;
                }
            };
            res
        })
        .sum();
    Ok(out)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let _input = parse_input(lines);
    Ok(0)
}
