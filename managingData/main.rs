extern crate unicode_normalization;
use unicode_normalization::UnicodeNormalization;
use std::fs;
use regex::Regex;

fn format(mut s : String) -> String {

    /* Except '|', '(' and ')' for nomina sacra,
     * we remove punctuation and others signs. ------------------------*/
    s = s.replace(&['¶', '⋄', '?', '!', '–', ':', 
    ';', ',', '.', '·', '“', '”', '‘', '’', '᾽',
    'ʼ', '*', '[', ']', '…', '⟦', '⟧'], "");

    // We remplace any "invisible nu" by a "true one". ------------------
    s = s.replace("ˉ", "ν");

    // We remove any spaces. --------------------------------------------
    s = s.chars().filter(|c| !c.is_whitespace()).collect();

    // We remove diacritics signs. --------------------------------------
    const LEN: usize = '\u{036f}' as usize - '\u{0300}' as usize;
    let mut arr = ['\0'; LEN];
    for (item, ch) in std::iter::zip(&mut arr, '\u{0300}'..='\u{036f}') {
        *item = ch;
    }
    s = s.nfd().to_string().replace(arr, "");

    // We change any uppercase letter to lowercase. ---------------------
    s = s.to_lowercase();
    
    // We replace every sigmas to the lunar sigma. ----------------------
    s.replace(&['σ', 'ς'], "ϲ")
}


fn main() -> std::io::Result<()> {
    
    let re = Regex::new(r"^([^\s]*\s)(.*)").unwrap();
    
    let contents = fs::read_to_string("lastOnes_chosen_db.txt")
        .expect("Something went wrong reading the file");

    let mut new_line = String::from("");
    let lines : String = contents.lines()

        // On remplace le texte grec initial par le formaté.
       .map(|l| {
           for i in re.captures_iter(l) {
               new_line = (&i[1]).to_string()
                   + &format((&i[2]).to_string()) + "\n";
           }
           new_line.clone()
       }).collect();

    fs::write("last_db.txt", lines)?;
    Ok(())
}
