use std::io::{BufRead, BufReader};
use std::fs::File;
use std::path::Path;

fn main() {
    // get user input
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();
    let sample_num: u8 = input.trim().parse().unwrap();

    // read file
    let path_str = format!("../../beispieldaten/stapel{}", sample_num);
    let path = Path::new(&path_str);
    let mut lines = BufReader::new(File::open(path).expect("Error opening file")).lines();
    let nkm:Vec<u32> = lines.next().unwrap().unwrap().split_whitespace().map(|x| x.parse::<u32>().unwrap()).collect();
    let (n, k, m) = (nkm[0], nkm[1], nkm[2]);
    println!("{} {} {}", &n, &k, &m);
    
}
