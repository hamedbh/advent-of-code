use anyhow::Result;
use rayon::prelude::*;

pub fn parse_input(lines: &[String]) -> (Vec<i64>, usize, usize) {
    let height = lines.len();
    let width = lines[0].len();
    let grid = lines
        .iter()
        .flat_map(|line| line.chars().map(|c| if c == '@' { 1 } else { 0 }))
        .collect();
    (grid, height, width)
}

fn find_neighbours(i: usize, j: usize, m: usize, n: usize) -> Vec<usize> {
    ((i.saturating_sub(1))..=(i + 1).min(m - 1))
        .flat_map(|row| {
            (j.saturating_sub(1)..=(j + 1).min(n - 1))
                .map(move |col| (row, col))
        })
        .filter(|(row, col)| !(*row == i && *col == j))
        .map(|(row, col)| row * n + col)
        .collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let (grid, height, width) = parse_input(lines);
    let mut all_neighbours: Vec<Vec<usize>> =
        Vec::with_capacity(height * width);
    for i in 0..height {
        for j in 0..width {
            all_neighbours.push(find_neighbours(i, j, height, width));
        }
    }
    let total: i64 = (0..grid.len())
        .into_par_iter()
        .filter(|&idx| grid[idx] == 1)
        .filter(|&idx| {
            let neighbours = &all_neighbours[idx];
            neighbours.iter().map(|&n_idx| grid[n_idx]).sum::<i64>() < 4
        })
        .count() as i64;
    Ok(total)
}
pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let (mut grid, height, width) = parse_input(lines);
    let mut total: i64 = 0;
    let mut all_neighbours: Vec<Vec<usize>> =
        Vec::with_capacity(height * width);
    for i in 0..height {
        for j in 0..width {
            all_neighbours.push(find_neighbours(i, j, height, width));
        }
    }
    let mut removable: Vec<usize> = Vec::with_capacity(grid.len());
    loop {
        removable.clear();
        for idx in 0..grid.len() {
            if grid[idx] != 1 {
                continue;
            }
            let neighbours = &all_neighbours[idx];
            let roll_count: i64 =
                neighbours.iter().map(|&n_idx| grid[n_idx]).sum();
            if roll_count < 4 {
                removable.push(idx);
            }
        }
        if removable.is_empty() {
            break;
        }
        total += removable.len() as i64;
        for &idx in &removable {
            grid[idx] = 0;
        }
    }
    Ok(total)
}
