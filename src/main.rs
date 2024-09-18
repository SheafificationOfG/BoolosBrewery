mod game;
mod language;
mod util;

use std::io::{self, Write};

#[cfg(not(feature = "test-strategy"))]
use colored::Colorize;

#[cfg(feature = "test-strategy")]
use rand::{seq::SliceRandom, thread_rng};

fn read_line(prompt: String) -> io::Result<String> {
    if !prompt.is_empty() {
        print!("{} ", prompt);
    }
    io::stdout().flush()?;

    let mut line = String::new();
    io::stdin().read_line(&mut line)?;

    Ok(String::from(line.trim_end()))
}

#[cfg(feature = "test-strategy")]
fn main() {
    let question_limit: usize = read_line(String::new())
        .unwrap_or_else(|err| panic!("{err}"))
        .trim()
        .parse()
        .unwrap_or_else(|err| panic!("{err}"));

    // no cheating! :))
    let mut contexts = game::Context::permutations(question_limit);
    contexts.shuffle(&mut thread_rng());
    for mut context in contexts {
        println!("begin");
        'main: for i in 0.. {
            let question = read_line(String::new()).unwrap_or_else(|err| panic!("{err}"));
            if question.to_lowercase() == "done" {
                break 'main;
            }
            if i >= question_limit {
                panic!("You've asked too many questions!");
            }
            context.ask(question).unwrap_or_else(|err| panic!("{err}"));
        }
        '_guess: for person in context.participants() {
            let guess = read_line(String::new()).unwrap_or_else(|err| panic!("{err}"));
            if !context
                .guess_field(&person, &guess)
                .unwrap_or_else(|err| panic!("{err}"))
            {
                let mut message =
                    format!("The guess that {person} studies {guess} is incorrect!\n");
                message += &format!("Log:\n{}\n", context.log());
                for p in context.participants() {
                    message += &format!("{} studies {}!\n", &p, context.field_of(&p).unwrap());
                }
                panic!("{message}");
            }
        }
        let end = read_line(String::new()).unwrap_or_else(|err| panic!("{err}"));
        if end != "end" {
            panic!("Expected the keyword \"end\"!");
        }
    }
    println!("end");
}

#[cfg(not(feature = "test-strategy"))]
fn main() {
    use rustyline::error::ReadlineError;

    let mut context = game::Context::new();
    context.hello();
    let mut line_reader = match rustyline::DefaultEditor::new() {
        Ok(reader) => reader,
        Err(err) => {
            eprintln!("Unable to initialize line reader! {err}");
            return;
        }
    };
    let mut i = 0;
    'main: loop {
        if i >= game::NUM_QUESTIONS {
            if cfg!(feature = "endless") {
                println!(
                    "Enter {} when you've figured out everyone's fields of expertise!",
                    "done".bold().bright_blue()
                );
            } else {
                break 'main;
            }
        }
        let question = match line_reader.readline(&format!("Question {}: ", i + 1).dimmed()) {
            Ok(question) => {
                line_reader.add_history_entry(question.as_str()).unwrap();
                question.trim().to_string()
            }
            Err(ReadlineError::Interrupted) | Err(ReadlineError::Eof) => {
                return;
            }
            Err(err) => {
                eprintln!("Error reading line: {err}");
                println!("{}", "quit".bold().white().on_red());
                return;
            }
        };
        match question.to_lowercase().as_str() {
            "done" => break 'main,
            "quit" | "exit" => {
                println!("{}", "Au revoir !".italic().bright_purple());
                return;
            }
            _ => {}
        }
        match context.ask(question) {
            Ok(()) => i += 1,
            Err(error) => println!("{}", error),
        }
    }

    // time to guess!
    let mut all_correct = true;
    context.summary();
    println!("Time to guess everyone's field!");
    for person in context.participants() {
        'guess: loop {
            let Ok(guess) = read_line(format!("{} studies:", &person)) else {
                println!("{}", "or not...".italic().red());
                return;
            };
            match context.guess_field(&person, &guess) {
                Ok(is_correct) => {
                    all_correct &= is_correct;
                    break 'guess;
                }
                Err(error) => println!("{}", error),
            }
        }
    }

    // drumroll...
    if all_correct {
        println!(
            "\n{}: you got them all right, and it only took {i} question{s}!",
            "Well done".bold().green(),
            s = if i != 1 { "s" } else { "" },
        );
    } else {
        println!("\nThat is unfortunately {}.", "incorrect".bold().red());
        for person in context.participants() {
            println!(
                "{} studies {}!",
                &person,
                context
                    .field_of(&person)
                    .expect("If you're reading this, Bob's your uncle.")
            );
        }
    }

    println!(
        "\n~~ {} ~~\n",
        "Merci d'avoir joué !".italic().bright_purple()
    );
}
