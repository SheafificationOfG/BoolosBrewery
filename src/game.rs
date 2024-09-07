use crate::language::*;
use crate::util::indexed_string::ToIndexedString;
use crate::util::parsing::Syntax;

use rand::{seq::SliceRandom, thread_rng};
use std::fmt::Display;

use colored::Colorize;

#[cfg(feature = "test-strategy")]
use itertools::Itertools;

#[cfg(all(feature = "easy", feature = "hard"))]
compile_error!("Cannot simultaneously enable \"easy\" and \"hard\" mode!");

pub const NUM_PEOPLE: usize = {
    if cfg!(feature = "easy") {
        2
    } else if cfg!(feature = "hard") {
        4
    } else {
        3
    }
};

#[cfg(not(feature = "test-strategy"))]
pub const NUM_QUESTIONS: usize = {
    if cfg!(feature = "easy") {
        1 // optimal
    } else if cfg!(feature = "hard") {
        7 // GSheaf's best effort
    } else {
        3 // optimal
    }
};

pub const NUM_WORDS: usize = {
    if cfg!(feature = "hard") {
        3
    } else {
        2
    }
};

/// Context for simulation
pub struct Context {
    /// Assignment of person to field (private, because you're supposed to figure this out yourself `;)`)
    field_assignment: Vec<Field>,
    /// "foo/bar[/baz]" convention for the mathematician.
    word_assignment: WordAssignment,
    /// History of questions asked
    history: Vec<(Question, ResponseConst)>,
}

pub trait Interpret {
    type To;
    fn interpret(&self, context: &Context) -> InterpretResult<Self::To>;
}

//////// Interpretation implementations ////////

impl Interpret for Question {
    type To = ResponseConst;
    fn interpret(&self, context: &Context) -> InterpretResult<Self::To> {
        context
            .response_of(&self.person, self.expression.interpret(context)?)
            .ok_or(InterpretError(format!("{} is not present!", self.person)))
    }
}

impl Interpret for Bool {
    type To = bool;
    fn interpret(&self, context: &Context) -> InterpretResult<Self::To> {
        use Bool::*;
        match self {
            Wrapped(expr) => expr.interpret(context),
            Unary(op, expr) => {
                use UnaryOp::*;
                match op {
                    Not => expr.interpret(context).map(|x| !x),
                }
            }
            Binary(op, lhs, rhs) => {
                use BinaryOp::*;
                let lhs = lhs.interpret(context)?;
                let rhs = rhs.interpret(context)?;
                Ok(match op {
                    And => lhs && rhs,
                    Or => lhs || rhs,
                    Implies => !lhs || rhs,
                    Compare(Cmp::Is) => lhs == rhs,
                    Compare(Cmp::Not) => lhs != rhs,
                })
            }
            CompareResponse(cmp, lhs, rhs) => {
                use Cmp::*;
                let lhs = lhs.interpret(context)?;
                let rhs = rhs.interpret(context)?;
                Ok(match cmp {
                    Is => lhs == rhs,
                    Not => lhs != rhs,
                })
            }
            Studies(person, field) => Ok(field
                == context.field_of(person).ok_or(InterpretError(format!(
                    "What {} studies is irrelevant!",
                    person
                )))?),
            Const(value) => {
                use BoolConst::*;
                Ok(match value {
                    True => true,
                    False => false,
                })
            }
        }
    }
}

impl Interpret for Response {
    type To = ResponseConst;
    fn interpret(&self, context: &Context) -> InterpretResult<Self::To> {
        use Response::*;
        match self {
            Ask(question) => question.interpret(context),
            Const(response) => Ok(*response),
        }
    }
}

//////// Other implementations ////////

pub type InterpretResult<T> = Result<T, InterpretError>;

pub struct InterpretError(String);

impl Display for InterpretError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl Context {
    #[cfg(not(feature = "test-strategy"))]
    pub fn new() -> Self {
        use Field::*;
        let mut field_assignment: Vec<Field> = [Mathematics, Physics, Engineering, Philosophy]
            .iter()
            .take(NUM_PEOPLE)
            .cloned()
            .collect();

        if cfg!(not(feature = "derand")) {
            field_assignment.shuffle(&mut thread_rng());
        }

        Self {
            field_assignment,
            word_assignment: WordAssignment::new(),
            history: vec![],
        }
    }

    #[cfg(feature = "test-strategy")]
    pub fn permutations(question_limit: usize) -> Vec<Self> {
        use Field::*;
        let mut cases = Vec::<Self>::new();
        for field_assignment in [Mathematics, Physics, Engineering, Philosophy]
            .iter()
            .take(NUM_PEOPLE)
            .cloned()
            .permutations(NUM_PEOPLE)
        {
            for word_assignment in WordAssignment::permutations(question_limit) {
                cases.push(Self {
                    field_assignment: field_assignment.to_vec(),
                    word_assignment,
                    history: vec![],
                })
            }
        }
        cases
    }

    #[cfg(not(feature = "test-strategy"))]
    pub fn hello(&self) {
        divider();
        println(format!("Welcome to {}!", "Boolos' Brewery".green()).italic());
        divider();
        divider();
        if cfg!(feature = "easy") {
            println(format!(
                "You are with {} and {}.",
                Person::Alice,
                Person::Bob
            ));
            println(format!(
                "One of them studies {}, and one of them studies {}.",
                Field::Mathematics,
                Field::Physics,
            ));
            println(format!(
                "One of them says {foo} for \"yes\", and {bar} for \"no\"; the other says the opposite.",
                foo = ResponseConst::Foo,
                bar = ResponseConst::Bar,
            ));
        } else if cfg!(feature = "hard") {
            println(format!(
                "You are with {}, {}, {}, and {}.",
                Person::Alice,
                Person::Bob,
                Person::Charlie,
                Person::Dan,
            ));
            println(format!(
                "One of them studies {}, one {}, one {}, and one {}.",
                Field::Mathematics,
                Field::Physics,
                Field::Engineering,
                Field::Philosophy,
            ));
            println(format!(
                "Everyone responds to you with {}, {}, or {}.",
                ResponseConst::Foo,
                ResponseConst::Bar,
                ResponseConst::Baz,
            ));
            println("Two of these three words correspond to \"yes\" and \"no\" in some order for the mathematician, and the mathematician only uses these words.".to_string());
            println("The physicist uses the same words as the mathematician, but with the opposite meanings.");
            println(format!(
                "The engineer may respond with {}, {}, or {}, but the choice is random.",
                ResponseConst::Foo,
                ResponseConst::Bar,
                ResponseConst::Baz,
            ));
            println("The philosopher will only respond with the word the mathematician and the physicist don't use.");
        } else {
            println(format!(
                "You are with {}, {}, and {}.",
                Person::Alice,
                Person::Bob,
                Person::Charlie,
            ));
            println(format!(
                "One of them studies {}, one {} and one {}.",
                Field::Mathematics,
                Field::Physics,
                Field::Engineering,
            ));
            println(format!(
                "Everyone responds to you with {} or {}.",
                ResponseConst::Foo,
                ResponseConst::Bar,
            ));
            println(
                "The mathematician uses one of the words for \"yes\", and the other for \"no\".",
            );
            println("The physicist uses opposite conventions.");
            println(format!(
                "The engineer may respond with {} or {}, but the choice is random.",
                ResponseConst::Foo,
                ResponseConst::Bar,
            ));
        }
        divider();

        if cfg!(feature = "derand") {
            println("[[game has been de-randomised]]".on_yellow());
        }
        if cfg!(any(feature = "derand", feature = "cheat")) {
            for person in self.participants() {
                println(format!(
                    "{} studies {}.",
                    &person,
                    self.field_of(&person).unwrap()
                ));
            }
            println(format!(
                "For the mathematician, \"{}\" means yes, and \"{}\" means no.",
                self.word_assignment.yes, self.word_assignment.no
            ));
        } else {
            println(format!(
                "It should take {n} question{s} to figure out who is which!",
                n = NUM_QUESTIONS,
                s = if NUM_QUESTIONS != 1 { "s" } else { "" }
            ));
        }
        divider();
    }

    #[cfg(feature = "test-strategy")]
    fn response_of(&self, person: &Person, expr: bool) -> Option<ResponseConst> {
        self.field_of(person).map(|field| {
            self.word_assignment
                .scripted_response_of(field, expr, self.history.len())
        })
    }

    #[cfg(not(feature = "test-strategy"))]
    fn response_of(&self, person: &Person, expr: bool) -> Option<ResponseConst> {
        self.field_of(person)
            .map(|field| self.word_assignment.response_of(field, expr))
    }

    pub fn field_of(&self, person: &Person) -> Option<&Field> {
        use Person::*;
        self.field_assignment.get(match person {
            Alice => 0,
            Bob => 1,
            Charlie => 2,
            Dan => 3,
        })
    }

    pub fn ask(&mut self, src: String) -> Result<(), InterpretError> {
        let src = src.to_indexed_string();
        let question = Question::parse(&src)
            .map_err(|parse_error| InterpretError(format!("{}", parse_error)))?
            .meaning;
        let person = &question.person;
        let response = question.interpret(self)?;

        if cfg!(feature = "test-strategy") {
            println!("{response}");
        } else {
            divider();
            println(format!("You asked {question}"));
            println(format!("{person} responds: {response}."));
            divider();
        }

        self.history.push((question, response));
        Ok(())
    }

    pub fn participants(&self) -> Vec<Person> {
        use Person::*;
        self.field_assignment
            .iter()
            .zip([Alice, Bob, Charlie, Dan])
            .map(move |(_, person)| person)
            .collect()
    }

    pub fn guess_field(&self, person: &Person, guess: String) -> Result<bool, InterpretError> {
        let field = self
            .field_of(person)
            .ok_or(InterpretError(format!("{} isn't here!", person)))?;
        let guess = guess.to_indexed_string();
        let guess = Field::parse(&guess)
            .map_err(|parse_error| InterpretError(format!("{}", parse_error)))?
            .meaning;
        Ok(guess == *field)
    }

    #[cfg(not(feature = "test-strategy"))]
    pub fn summary(&self) {
        divider();
        println("Summary");
        divider();
        for (question, response) in self.history.iter() {
            println(format!("You asked {question}"));
            println(format!(
                "{person} responded with: {response}",
                person = question.person
            ));
        }
        divider();
    }

    #[cfg(feature = "test-strategy")]
    pub fn log(&self) -> String {
        let mut summary = String::new();
        for (index, (question, response)) in self.history.iter().enumerate() {
            summary += &format!("Q{i}: {question}\nA{i}: {response}\n", i = index + 1);
        }
        summary
    }
}

struct WordAssignment {
    yes: ResponseConst,
    no: ResponseConst,
    idk: ResponseConst,
    #[cfg(feature = "test-strategy")]
    engg_script: Vec<ResponseConst>,
}
impl WordAssignment {
    #[cfg(not(feature = "test-strategy"))]
    fn new() -> Self {
        use ResponseConst::*;
        let mut assignment = [Foo, Bar, Baz];

        if cfg!(not(feature = "derand")) {
            assignment[..NUM_WORDS].shuffle(&mut thread_rng());
        }

        let [yes, no, idk] = assignment;
        Self { yes, no, idk }
    }

    #[cfg(feature = "test-strategy")]
    fn permutations(question_limit: usize) -> Vec<Self> {
        use ResponseConst::*;
        let mut perms = Vec::<Self>::new();
        for word_perm in [Foo, Bar, Baz]
            .iter()
            .take(NUM_WORDS)
            .cloned()
            .permutations(NUM_WORDS)
        {
            for engg_script in [Foo, Bar, Baz]
                .iter()
                .take(NUM_WORDS)
                .cloned()
                .combinations_with_replacement(question_limit)
            {
                perms.push(Self {
                    yes: word_perm[0],
                    no: word_perm[1],
                    idk: *word_perm.get(2).unwrap_or(&Baz),
                    engg_script,
                })
            }
        }
        perms
    }

    fn response_of(&self, field: &Field, expr: bool) -> ResponseConst {
        use Field::*;
        match field {
            Mathematics => {
                if expr {
                    self.yes
                } else {
                    self.no
                }
            }
            Physics => {
                if expr {
                    self.no
                } else {
                    self.yes
                }
            }
            Engineering => {
                if cfg!(feature = "derand") {
                    self.idk
                } else {
                    #[cfg(not(feature = "hard"))]
                    let mut choices = [self.yes, self.no];
                    #[cfg(feature = "hard")]
                    let mut choices = [self.yes, self.no, self.idk];

                    choices.shuffle(&mut thread_rng());

                    choices[0]
                }
            }
            Philosophy => self.idk,
        }
    }

    #[cfg(feature = "test-strategy")]
    fn scripted_response_of(&self, field: &Field, expr: bool, index: usize) -> ResponseConst {
        match field {
            Field::Engineering => self.engg_script[index],
            _ => self.response_of(field, expr),
        }
    }
}

//////// Styling? ////////

fn println<Str: ToString>(line: Str) {
    println!(
        "{pipe} {line}",
        pipe = "|".bright_blue(),
        line = line.to_string()
    );
}

fn divider() {
    println!("{}", "+---".bright_blue());
}
