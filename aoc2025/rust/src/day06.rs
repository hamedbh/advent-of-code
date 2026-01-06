use anyhow::Result;

// The enum allows us to look up addition and multiplication easily,
// which simplifies the rest of it
pub enum Op {
    Add,
    Mul,
}

impl Op {
    fn apply(&self, values: &[i64]) -> i64 {
        match self {
            Op::Add => values.iter().sum(),
            Op::Mul => values.iter().product(),
        }
    }
}

// Type aliases to make code more readable
type CharColumn = Vec<char>;
type ColumnGroup = Vec<CharColumn>;

fn parse_operators(line: &str) -> Vec<Op> {
    // Parsing the operators is easy: split on any whitespace and then
    // lookup from the enum. The result will have an `.apply()` method,
    // which we use later.
    line.split_whitespace()
        .map(|x| match x {
            "+" => Op::Add,
            "*" => Op::Mul,
            _ => panic!("Unexpected operator: {}", x),
        })
        .collect()
}

fn parse_vertical_number(column: &[char]) -> i64 {
    let s: String = column.iter().filter(|&&c| c != ' ').collect();
    s.parse::<i64>().unwrap()
}

fn group_columns(columns: Vec<CharColumn>) -> Vec<ColumnGroup> {
    let mut groups: Vec<ColumnGroup> = Vec::new();
    let mut current_group: ColumnGroup = Vec::new();
    for column in columns {
        if column.iter().all(|&c| c == ' ') {
            if !current_group.is_empty() {
                groups.push(current_group.clone());
                current_group.clear();
            }
        } else {
            current_group.push(column);
        }
    }
    if !current_group.is_empty() {
        groups.push(current_group);
    }
    groups
}

pub fn parse_input_human(lines: &[String]) -> Vec<(Vec<i64>, Op)> {
    let (operator_line, data_lines) = lines.split_last().expect("Empty input");
    let operators = parse_operators(operator_line);
    let rows: Vec<Vec<i64>> = data_lines
        .iter()
        .map(|line| {
            line.split_whitespace()
                .map(|s| s.parse::<i64>().unwrap())
                .collect()
        })
        .collect();
    let num_cols = rows[0].len();
    // Nested iterators: for each col_idx, map over the rows and
    // extract the element at that position
    let operands: Vec<Vec<i64>> = (0..num_cols)
        .map(|col_idx| rows.iter().map(|row| row[col_idx]).collect())
        .collect();
    operands.into_iter().zip(operators).collect()
}

pub fn parse_input_ceph(lines: &[String]) -> Vec<(Vec<i64>, Op)> {
    // Parse cephalopod-style maths: numbers written vertically
    // (top-to-bottom), problems separated by columns of spaces
    let (operator_line, data_lines) = lines.split_last().expect("Empty input");
    let operators = parse_operators(operator_line);
    let char_grid: Vec<Vec<char>> = data_lines
        .iter()
        .map(|line| line.chars().collect())
        .collect();
    let num_cols = char_grid[0].len();
    let columns: Vec<CharColumn> = (0..num_cols)
        .map(|col_idx| char_grid.iter().map(|row| row[col_idx]).collect())
        .collect();
    let groups = group_columns(columns);
    let operands: Vec<Vec<i64>> = groups
        .iter()
        .map(|group| {
            group.iter().map(|col| parse_vertical_number(col)).collect()
        })
        .collect();
    operands.into_iter().zip(operators).collect()
}

pub fn solve_part1(lines: &[String]) -> Result<i64> {
    Ok(parse_input_human(lines)
        .iter()
        .map(|(operands, operator)| operator.apply(&operands))
        .sum())
}

pub fn solve_part2(lines: &[String]) -> Result<i64> {
    Ok(parse_input_ceph(lines)
        .iter()
        .map(|(operands, operator)| operator.apply(&operands))
        .sum())
}
