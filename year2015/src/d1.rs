use std::env;
use std::fs;

pub fn part1() {
    println!("Part1");

    let contents = fs::read_to_string("src/data/d1p1.txt")
        .expect("Something went wrong reading the file");

    let mut sum = 0;
    for c in contents.chars() {
        sum += match c {
            '(' => 1,
            ')' => -1,
            _ => 0
        }
    }
    println!("{}", sum)
}