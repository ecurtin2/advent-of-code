pub fn part1(input: String) -> String {
    let result: i32 = input
        .chars()
        .map(|c| match c {
            '(' => 1,
            ')' => -1,
            _ => 0,
        })
        .sum();
    format!("{}", result)
}

pub fn part2(input: String) -> String {
    let nums = input.chars().map(|c| match c {
        '(' => 1,
        ')' => -1,
        _ => 0,
    });

    let mut total = 0;
    let mut result: i32 = -1;
    for (i, val) in nums.enumerate() {
        total += val;
        if total == -1 {
            result = i as i32;
            break;
        }
    }
    format!("{}", result + 1)
}

#[cfg(test)]
mod tests {
    use crate::d1::part2;
    #[test]
    fn it_works() {
        assert_eq!(part2(")".to_string()), "1");
        assert_eq!(part2("()())".to_string()), "5");
    }
}
