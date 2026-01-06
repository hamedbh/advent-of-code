use anyhow::Result;

pub fn parse_input(lines: &[String]) -> (Vec<(i64, i64)>, Vec<i64>) {
    let mut fresh_ranges: Vec<(i64, i64)> = Vec::with_capacity(lines.len());
    let mut available: Vec<i64> = Vec::with_capacity(lines.len());
    for item in lines {
        if let Some((lower, upper)) = item.split_once("-") {
            fresh_ranges.push((
                lower.parse::<i64>().unwrap(),
                upper.parse::<i64>().unwrap(),
            ));
        } else if !item.is_empty() {
            available.push(item.parse::<i64>().unwrap());
        }
    }
    fresh_ranges.sort();
    let mut merged_ranges: Vec<(i64, i64)> =
        Vec::with_capacity(fresh_ranges.len());
    let mut current_range = fresh_ranges[0];
    for &(lower, upper) in &fresh_ranges[1..] {
        if current_range.1 >= lower - 1 {
            current_range = (current_range.0, current_range.1.max(upper));
        } else {
            merged_ranges.push(current_range);
            current_range = (lower, upper);
        }
    }
    merged_ranges.push(current_range);
    (merged_ranges, available)
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let (merged_ranges, available) = parse_input(lines);

    let mut total: i64 = 0;
    // Use binary search across the ranges
    for item in available {
        let mut low: usize = 0;
        let mut high: usize = merged_ranges.len() - 1;
        while low <= high {
            let mid: usize = (low + high) / 2;
            let &(lower, upper) = &merged_ranges[mid];
            if item < lower {
                if mid == 0 {
                    break;
                }
                high = mid - 1;
            } else if item > upper {
                low = mid + 1;
            } else {
                total += 1;
                break;
            }
        }
    }
    Ok(total)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let (merged_ranges, _available) = parse_input(lines);
    Ok(merged_ranges
        .iter()
        .map(|(lower, upper)| upper - lower + 1)
        .sum())
}
