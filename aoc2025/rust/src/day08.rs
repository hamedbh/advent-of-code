use std::collections::HashMap;

use anyhow::Result;

pub struct Point {
    x: i64,
    y: i64,
    z: i64,
}

impl Point {
    pub fn new(x: i64, y: i64, z: i64) -> Self {
        Point { x, y, z }
    }

    pub fn distance(&self, other: &Point) -> f64 {
        let dx = (self.x - other.x) as f64;
        let dy = (self.y - other.y) as f64;
        let dz = (self.z - other.z) as f64;
        (dx * dx + dy * dy + dz * dz).sqrt()
    }
}

pub struct UnionFind {
    parents: Vec<usize>,
}

impl UnionFind {
    pub fn new(size: usize) -> Self {
        UnionFind {
            parents: (0..size).collect(),
        }
    }

    pub fn find_root(&mut self, x: usize) -> usize {
        // First pass finds the root
        let mut current: usize = x;
        loop {
            if self.parents[current] == current {
                break;
            } else {
                current = self.parents[current];
            }
        }
        let root = current;

        // second pass compresses the path
        let mut current = x;
        while current != root {
            // steps are:
            //   1. save the next before overwriting
            //   2. point current directly at the root
            //   3. Update current to next
            let next = self.parents[current];
            self.parents[current] = root;
            current = next;
        }
        root
    }

    pub fn union(&mut self, x: usize, y: usize) -> i64 {
        let root_x = self.find_root(x);
        let root_y = self.find_root(y);
        if root_x != root_y {
            self.parents[root_x] = root_y;
            -1
        } else {
            0
        }
    }
}

fn compute_pairwise_distances(points: &[Point]) -> Vec<(f64, usize, usize)> {
    let mut pairwise_distances: Vec<(f64, usize, usize)> =
        Vec::with_capacity(points.len() * (points.len() - 1) / 2);
    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            let distance = points[i].distance(&points[j]);
            pairwise_distances.push((distance, i, j));
        }
    }
    pairwise_distances
}

pub fn parse_input(lines: &[String]) -> Vec<Point> {
    lines
        .iter()
        .map(|line| {
            let numbers: Vec<i64> =
                line.split(",").map(|n| n.parse::<i64>().unwrap()).collect();
            Point::new(numbers[0], numbers[1], numbers[2])
        })
        .collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let mut pairwise_distances = compute_pairwise_distances(&input);
    pairwise_distances.sort_by(|a, b| a.0.total_cmp(&b.0));
    let n_connections: usize = if input.len() == 1000 { 1000 } else { 10 };
    let distances = &pairwise_distances[..n_connections];
    let mut union_find = UnionFind::new(input.len());
    for &(_, i, j) in distances {
        union_find.union(i, j);
    }
    let roots: Vec<usize> =
        (0..input.len()).map(|x| union_find.find_root(x)).collect();
    let mut circuit_sizes: HashMap<usize, i64> = HashMap::new();
    for root in roots {
        *circuit_sizes.entry(root).or_insert(0) += 1;
    }
    let mut counts: Vec<i64> = circuit_sizes.values().copied().collect();
    counts.sort_by(|a, b| b.cmp(a));
    Ok(counts[..3].iter().product())
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let input = parse_input(lines);
    let mut pairwise_distances = compute_pairwise_distances(&input);
    pairwise_distances.sort_by(|a, b| a.0.total_cmp(&b.0));
    let mut union_find = UnionFind::new(input.len());
    let mut n_circuits = input.len() as i64;
    for (_, i, j) in pairwise_distances {
        n_circuits += union_find.union(i, j);
        if n_circuits == 1 {
            return Ok(input[i].x * input[j].x);
        }
    }
    // Need to leave this in, otherwise the return value of the
    // function could be ()
    Ok(0)
}
