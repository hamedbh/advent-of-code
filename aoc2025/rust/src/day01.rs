use anyhow::Result;

fn count_zero_clicks(start_position: i32, turn_size: i32) -> u64 {
    let start_position = start_position.rem_euclid(100);
    let distance = turn_size.abs();
    let mut full_cycles = (distance / 100) as u64;

    if turn_size >= 0 {
        let end = (start_position + distance).rem_euclid(100);
        if end < start_position {
            full_cycles += 1;
        }
    } else {
        let end = (start_position - distance).rem_euclid(100);
        if end > start_position {
            full_cycles += 1;
        }
    }

    full_cycles
}

pub fn parse_input(lines: &[String]) -> Vec<i32> {
    // TODO: Parse lines like "R49", "L13" into numbers
    // You'll need to handle the direction and convert to signed ints
    lines
        .iter()
        .map(|s| {
            let direction = if s.chars().next().unwrap() == 'R' {
                1
            } else {
                -1
            };
            let number_part = &s[1..];
            number_part.parse::<i32>().unwrap() * direction
        })
        .collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);

    let mut position = 50;
    let mut count = 0;

    for &value in &input {
        position = (position + value) % 100;
        if position == 0 {
            count += 1;
        }
    }

    Ok(count)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);

    let mut position = 50;
    let mut total = 0;

    for &turn in &input {
        let clicks = count_zero_clicks(position, turn);
        total += clicks;
        position += turn;
    }

    Ok(total as i64)
}
