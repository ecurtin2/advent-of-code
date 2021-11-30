use structopt::StructOpt;
mod d1;


#[derive(StructOpt)]
struct Cli {
    day: i8,
    part: i8,
}

fn main() {
    let args = Cli::from_args();
    println!("Running day {} part {}", args.day, args.part);
    match (args.day, args.part) {
        (1, 1) => d1::part1(),
        _ => println!("No implementation found for inputs.")
    }

}