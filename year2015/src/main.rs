use std::fs;
use structopt::StructOpt;
mod d1;
mod d2;

#[derive(StructOpt)]
struct Cli {
    day: i8,
    part: i8,
}

fn load(p: String) -> String {
    return fs::read_to_string(p).expect("Something went wrong reading the file");
}

fn main() {
    let args = Cli::from_args();
    println!("Running day {} part {}", args.day, args.part);
    let result: String = match (args.day, args.part) {
        (1, 1) => d1::part1(load(format!("src/data/d{}p{}.txt", 1, 1))),
        (1, 2) => d1::part2(load(format!("src/data/d{}p{}.txt", 1, 1))),
        (2, 1) => d2::part1(load(format!("src/data/d{}p{}.txt", 2, 1))),
        (2, 2) => d2::part2(load(format!("src/data/d{}p{}.txt", 2, 1))),
        _ => "No implementation found for inputs.".to_string(),
    };
    println!("{}", result)
}
