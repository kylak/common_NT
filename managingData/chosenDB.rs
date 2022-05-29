use std::fs;
use regex::Regex;

// Retire l'apparat critique NA28, la BHP2, et les versions de Bunning sauf la Pierpont et la KJV.

fn main() -> std::io::Result<()> {
    
    let contents = fs::read_to_string("database_el.txt")
        .expect("Something went wrong reading the file");
    
    let re = Regex::new(r"^.*-E.? .*$").unwrap();
    
    let lines : String = 

        // We treat the database_el.txt file line by line.
        contents.lines()
        
        // We keep the R.P text.
        .map(|l| l.replace("ROBINSON-ET-PIERPONT-E", "ROBINSON-ET-PIERPONT")
        
        // We keep the KJTR.
        .replace("KING-JAMES-E", "KING-JAMES"))
        
        // We remove BHP2, AP-CRITIQUE and A.B versions.
        .filter(|l| !l.contains("BHP2") && !l.contains("AP-CRITIQUE") && !re.is_match(l))
        
        // We create lines in the future created file.
        .map(|s| s.to_string() + "\n").collect();

    fs::write("chosen_db.txt", lines)?;
    Ok(())
}
