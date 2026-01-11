//! Advent of Code 2025, Day 9
//!
//! This puzzle was a real PITA. Ended up having to look for help online,
//! which led me to an amazing breakdown of the problem on Reddit:
//!
//! https://www.reddit.com/r/adventofcode/comments/1pichj2/comment/nt5guy3/
//!
//! Someone had then ported that person's TypeScript code into Python:
//!
//! https://github.com/euporphium/pyaoc/blob/main/aoc/2025/solutions/day09_part2.py
//!
//! (That's what I used for my Python implementation, which I then brought
//! into Rust.)
//!
//! Overall this one was _hard_. When I first saw the puzzle I had thought
//! that maybe I needed to create the polygon for the boundaries, but that
//! seemed so impossible I just forgot about it.
//!
//! The lesson here was really about understanding the size of the problem,
//! and that cool trick for 2d compression. Once it became possible to just
//! lookup elements from a relatively small grid (i.e. a `Vec<char>`)
//! then the problem can complete v fast.
use anyhow::Result;
use itertools::Itertools;
use rayon::prelude::*;
use std::collections::HashMap;

#[derive(Copy, Clone)]
pub struct Point {
    x: i64,
    y: i64,
}

impl Point {
    pub fn new(x: i64, y: i64) -> Self {
        Point { x, y }
    }

    pub fn area(&self, other: &Point) -> i64 {
        let width = (self.x - other.x).abs() + 1;
        let height = (self.y - other.y).abs() + 1;
        height * width
    }

    pub fn unpack(&self) -> (i64, i64) {
        (self.x, self.y)
    }
}
pub fn parse_input(lines: &[String]) -> Vec<Point> {
    lines
        .iter()
        .filter_map(|line| {
            let (left, right) = line.split_once(',')?;
            Some(Point::new(
                left.trim().parse::<i64>().ok()?,
                right.trim().parse::<i64>().ok()?,
            ))
        })
        .collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let pairs: Vec<(&Point, &Point)> =
        input.iter().cartesian_product(&input).collect();
    let out = pairs
        .par_iter()
        .map(|&(p1, p2)| p1.area(&p2))
        .max()
        .unwrap_or(0);
    Ok(out)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let sorted_x: Vec<i64> =
        input.iter().map(|p| p.x).unique().sorted().collect();
    let sorted_y: Vec<i64> =
        input.iter().map(|p| p.y).unique().sorted().collect();
    // Start by compressing the 2d space
    let map_x: HashMap<i64, i64> = sorted_x
        .iter()
        .enumerate()
        .map(|(i, &coord)| (coord, i as i64))
        .collect();
    let map_y: HashMap<i64, i64> = sorted_y
        .iter()
        .enumerate()
        .map(|(i, &coord)| (coord, i as i64))
        .collect();
    let compressed_red: Vec<(i64, i64)> = input
        .iter()
        .filter_map(|&point| {
            Some((*map_x.get(&point.x)?, *map_y.get(&point.y)?))
        })
        .collect();

    // Create the grid
    let width = sorted_x.len();
    let height = sorted_y.len();
    let mut grid: Vec<char> = (0..(width * height)).map(|_| '.').collect();

    // Mark the red tiles. Note I'm using a 1D grid now, just
    // to avoid nesting
    for &(x, y) in &compressed_red {
        grid[y as usize * width + x as usize] = '#';
    }

    // Now we 'rasterise' the edges of the polygon, i.e. connect them
    for i in 0..compressed_red.len() {
        let (x1, y1) = compressed_red[i];
        let (x2, y2) = compressed_red[(i + 1) % compressed_red.len()];

        // If the line is vertical fill along that y-axis, otherwise
        // fill along x-axis
        if x1 == x2 {
            for y in y1.min(y2)..=y1.max(y2) {
                grid[y as usize * width + x1 as usize] = '#';
            }
        } else if y1 == y2 {
            for x in x1.min(x2)..=x1.max(x2) {
                grid[y1 as usize * width + x as usize] = '#';
            }
        }
    }

    // Now we find some point on the inside of the polygon with
    // raycasting
    let mut inside_point: Option<(usize, usize)> = None;
    for y in 0..height {
        for x in 0..width {
            if grid[y * width + x] != '.' {
                continue;
            }

            // Count transitions from this point to the left
            let mut transitions = 0;
            let mut prev = '.';
            for i in (0..x).rev() {
                let cur = grid[y * width + i];
                // This tests whether we have hit a polygon edge
                if cur != prev {
                    transitions += 1;
                }
                prev = cur;
            }

            // Odd number of transitions means we started inside
            if transitions % 2 == 1 {
                inside_point = Some((x, y));
                break;
            }
        }
        if inside_point.is_some() {
            break;
        }
    }

    if let Some(point) = inside_point {
        let mut stack = vec![point];
        while let Some((x, y)) = stack.pop() {
            if x < width && y < height && grid[y * width + x] == '.' {
                grid[y * width + x] = 'X';
                if x + 1 < width {
                    stack.push((x + 1, y));
                }
                if x > 0 {
                    stack.push((x - 1, y));
                }
                if y + 1 < height {
                    stack.push((x, y + 1));
                }
                if y > 0 {
                    stack.push((x, y - 1));
                }
            }
        }
    }

    // Find the largest rectangle that is entirely inside the polygon
    let mut max_area: i64 = 0;

    for (i, first) in input[..input.len() - 1].iter().enumerate() {
        let (x1, y1) = first.unpack();
        let (cx1, cy1) = (map_x[&x1], map_y[&y1]);
        for second in input[(i + 1)..input.len()].iter() {
            let (x2, y2) = second.unpack();
            let (cx2, cy2) = (map_x[&x2], map_y[&y2]);

            // Calculate the actual area, ignore it if it's smaller
            // than current best
            let area = first.area(second);
            if area <= max_area {
                continue;
            }

            // Check if the edges of the rectangle are entirely
            // inside the polygon
            let min_cx = cx1.min(cx2) as usize;
            let max_cx = cx1.max(cx2) as usize;
            let min_cy = cy1.min(cy2) as usize;
            let max_cy = cy1.max(cy2) as usize;

            let mut enclosed = true;

            // First check top and bottom edges
            for cx in min_cx..=max_cx {
                if grid[min_cy * width + cx] == '.'
                    || grid[max_cy * width + cx] == '.'
                {
                    enclosed = false;
                    break;
                }
            }

            // Then left and right
            if enclosed {
                for cy in min_cy..=max_cy {
                    if grid[cy * width + min_cx] == '.'
                        || grid[cy * width + max_cx] == '.'
                    {
                        enclosed = false;
                        break;
                    }
                }
            }

            if enclosed {
                max_area = area;
            }
        }
    }

    Ok(max_area)
}
