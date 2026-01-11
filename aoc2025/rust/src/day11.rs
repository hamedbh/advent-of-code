use anyhow::Result;
use std::collections::{HashMap, HashSet};

pub struct PathCounter {
    graph: HashMap<String, HashSet<String>>,
    cache: HashMap<(String, String), i64>,
}

impl PathCounter {
    pub fn new(graph: HashMap<String, HashSet<String>>) -> Self {
        PathCounter {
            graph,
            cache: HashMap::new(),
        }
    }

    fn count_paths(&mut self, current: &str, target: &str) -> i64 {
        // 1. Check the cache
        if let Some(&cached) =
            self.cache.get(&(current.to_string(), target.to_string()))
        {
            return cached;
        }
        // 2. Compute the result
        let result = if current == target {
            1
        } else {
            let neighbours: Vec<String> = self
                .graph
                .get(current)
                .map(|set| set.iter().cloned().collect())
                .unwrap_or_default();
            neighbours
                .iter()
                .map(|next_node| self.count_paths(&next_node, target))
                .sum::<i64>()
        };
        // 3. Update the cache
        self.cache
            .insert((current.to_string(), target.to_string()), result);
        // 4. Return result
        result
    }
}
pub fn parse_input(lines: &[String]) -> HashMap<String, HashSet<String>> {
    lines
        .iter()
        .filter_map(|line| {
            let (left, right) = line.split_once(": ")?;
            let values: HashSet<String> =
                right.split_whitespace().map(|s| s.to_string()).collect();
            Some((left.to_string(), values))
        })
        .collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    let mut path_counter = PathCounter::new(parse_input(lines));
    let out = path_counter.count_paths("you", "out");
    Ok(out)
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    let mut path_counter = PathCounter::new(parse_input(lines));
    let dac_fft = path_counter.count_paths("dac", "fft");
    let out = if dac_fft > 0 {
        path_counter.count_paths("svr", "dac")
            * dac_fft
            * path_counter.count_paths("fft", "out")
    } else {
        path_counter.count_paths("svr", "fft")
            * path_counter.count_paths("fft", "dac")
            * path_counter.count_paths("dac", "out")
    };
    Ok(out)
}
