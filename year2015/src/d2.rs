fn calc_paper_needed(s: &str) -> i32 {
    let mut side_sizes: Vec<i32> = s.split("x").map(|x| x.parse::<i32>().unwrap()).collect();
    side_sizes.sort();
    side_sizes[0] * side_sizes[1] + 2 * (side_sizes[0] * side_sizes[1]
        + side_sizes[1] * side_sizes[2]
        + side_sizes[0] * side_sizes[2])
}


fn calc_ribbon_needed(s: &str) -> i32 {
    let mut side_sizes: Vec<i32> = s.split("x").map(|x| x.parse::<i32>().unwrap()).collect();
    side_sizes.sort();
    2 * (side_sizes[0] + side_sizes[1]) + side_sizes[0] * side_sizes[1] * side_sizes[2]
}

pub fn part1(input: String) -> String {
    let result: i32 = input.split("\n").map(calc_paper_needed).sum();
    format!("{}", result)
}

pub fn part2(input: String) -> String {
    let result: i32 = input.split("\n").map(calc_ribbon_needed).sum();
    format!("{}", result)
}

#[cfg(test)]
mod tests {
    use crate::d2::part1;
    use crate::d2::part2;
    #[test]
    fn it_works() {
        assert_eq!(part1("2x3x4".to_string()), "58");
        assert_eq!(part1("1x1x10".to_string()), "43");
        assert_eq!(part2("2x3x4".to_string()), "34");
        assert_eq!(part2("1x1x10".to_string()), "14");
    }
}
