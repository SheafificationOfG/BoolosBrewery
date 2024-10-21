use crate::util::indexed_string::*;
use crate::util::parsing::{
    self, next_graphic_char, ParseError, ParseResult, Syntax, SyntaxHighlight, Token,
};

use std::fmt::Display;

use colored::Colorize;

//////// Grammar enums ////////

#[derive(Debug, PartialEq, Eq)]
pub struct Question {
    pub person: Person,
    pub expression: Bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Person {
    Alice,
    Bob,
    Charlie,
    Dan,

    Mathematician,
    Physicist,
    Engineer,
    Philosopher,
}

#[derive(Debug, PartialEq, Eq)]
pub enum Bool {
    Wrapped(Box<Bool>),
    Unary(UnaryOp, Box<Bool>),
    Binary(BinaryOp, Box<Bool>, Box<Bool>),
    CompareResponse(Cmp, Box<Response>, Box<Response>),
    Studies(Person, Field),
    Const(BoolConst),
}

#[derive(Debug, PartialEq, Eq)]
pub enum BoolConst {
    True,
    False,
}

#[derive(Debug, PartialEq, Eq)]
pub enum UnaryOp {
    Not,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum BinaryOp {
    And,
    Or,
    Implies,
    Compare(Cmp),
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum Cmp {
    Is,
    Not,
}

pub struct StudyKeyword;

#[derive(Debug, PartialEq, Eq)]
pub enum Response {
    Ask(Question),
    Const(ResponseConst),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ResponseConst {
    Foo,
    Bar,
    Baz,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Field {
    Mathematics,
    Physics,
    Engineering,
    Philosophy,
}

//////// Syntax implementations ////////

impl Syntax for Question {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self> {
        let Token {
            meaning: person,
            end_index: index,
        } = Person::parse_in_context(src, index, context).map_err(|parse_error| {
            ParseError::new(src, index, "Questions must be directed to someone.")
                .following(parse_error)
        })?;

        if context.you.is_none() && matches!(person, Person::Mathematician | Person::Physicist | Person::Engineer | Person::Philosopher) {
            return Err(ParseError::new(src, index, format!("You don't know who the {} is!", person)));
        }

        let context = Self::Context { you: Some(person) };

        let index = parsing::next_graphic_char(src, index)
            .take_if(|token| token.character() == ':')
            .ok_or(ParseError::new(src, index, "Expected ':'."))?
            .index()
            + 1;
        let Token {
            meaning: expression,
            end_index: index,
        } = Bool::parse_in_context(src, index, context).map_err(|parse_error| {
            ParseError::new(src, index, format!("{person} expects a yes/no question."))
                .following(parse_error)
        })?;
        let index = parsing::next_graphic_char(src, index)
            .take_if(|token| token.character() == '?')
            .ok_or(ParseError::new(src, index, "Questions end with a '?'."))?
            .index()
            + 1;
        Token::ok(Question { person, expression }, index)
    }

    fn parse_in_context(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self> {
        let token = next_graphic_char(src, index).ok_or(ParseError::new(
            src,
            index,
            "Unexpected end of line!",
        ))?;
        if token.character() == '"' {
            let question = Self::parse_in_context(src, token.index() + 1, context)?;
            let end_index = {
                match next_graphic_char(src, question.end_index) {
                    Some(end_token) => {
                        if end_token.character() == '"' {
                            Ok(end_token.index() + 1)
                        } else {
                            Err(
                                ParseError::new(src, token.index(), "Expected an end quote '\"'!")
                                    .until(end_token.index()),
                            )
                        }
                    }
                    None => Err(
                        ParseError::new(src, token.index(), "Missing end quote '\"'!")
                            .until(question.end_index),
                    ),
                }
            }?;
            Token::ok(question.meaning, end_index)
        } else {
            Self::parse_impl(src, token.index(), context)
        }
    }
}

impl Syntax for Person {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use Person::*;
        let you = |index: usize, end_index: usize| {
            Token::ok(
                context.you.ok_or(
                    ParseError::new(src, index, "Not sure who \"you\" refers to in this scope.")
                        .until(end_index),
                )?,
                end_index,
            )
        };

        match src[index].character() {
            'A' | 'a' => Alice.match_aliases(src, index),
            'B' | 'b' => Bob.match_aliases(src, index),
            'C' | 'c' => Charlie.match_aliases(src, index),
            'D' | 'd' => Dan.match_aliases(src, index),

            'M' | 'm' => Mathematician.match_aliases(src, index),
            'P' | 'p' => Physicist.match_aliases(src, index).or_else(|phys_error| {
                Philosopher
                    .match_aliases(src, index)
                    .or_else(|phil_error| phil_error.following(phys_error).throw())
            }),
            'E' | 'e' => Engineer.match_aliases(src, index),

            'U' | 'u' if parsing::end_of_token(src, index + 1) => you(index, index + 1),
            'Y' | 'y' => {
                let end_index = parsing::full_match_any(src, index, ["You", "you"])
                    .take_if(|index| parsing::end_of_token(src, *index))
                    .ok_or(
                        ParseError::new(src, index, "Could not parse token. Did you mean \"you\"?")
                            .maybe_until(
                                parsing::next_char_with(src, index, char::is_ascii_whitespace)
                                    .map(IndexedChar::index),
                            ),
                    )?;
                you(index, end_index)
            }
            _ => ParseError::new(src, index, "Cannot recognise person name.").throw(),
        }
    }
}

impl Bool {
    /// Parse a single term, ignoring binary operations.
    fn parse_single_term(
        src: &IndexedString,
        index: usize,
        context: ParseContext,
    ) -> ParseResult<'_, Self> {
        use Bool::*;
        let token = parsing::next_graphic_char(src, index)
            .take_if(|token| token.index() < src.len())
            .ok_or(ParseError::new(
                src,
                index,
                "Unexpected end of line while parsing Boolean expression!",
            ))?;
        if token.character() == '(' {
            let Token {
                meaning,
                end_index: index,
            } = Self::parse_in_context(src, token.index() + 1, context)?;
            let end_index = parsing::next_graphic_char(src, index).map_or(
                Err(ParseError::new(src, index, "Missing closing parenthesis!").until(src.len())),
                |token| {
                    if token.character() == ')' {
                        Ok(token.index())
                    } else {
                        Err(ParseError::new(
                            src,
                            index,
                            format!("Expected ')', got '{}'", token.character()),
                        )
                        .until(token.index()))
                    }
                },
            )? + 1;
            Token::ok(Wrapped(Box::new(meaning)), end_index)
        } else if token.character() == '"' {
            let Token {
                meaning: question,
                end_index: index,
            } = Question::parse_in_context(src, token.index(), context)?;
            let Token {
                meaning: cmp,
                end_index: index,
            } = Cmp::parse_in_context(src, index, context).map_err(|parse_error| {
                ParseError::new(src, index, "Expected a comparison with another response.")
                    .following(parse_error)
            })?;
            let Token {
                meaning: rhs,
                end_index,
            } = Response::parse_in_context(src, index, context).map_err(|parse_error| {
                ParseError::new(src, index, "Expected another response after comparison.")
                    .following(parse_error)
            })?;
            Token::ok(
                CompareResponse(cmp, Box::new(Response::Ask(question)), Box::new(rhs)),
                end_index,
            )
        } else {
            let index = token.index();
            if let Ok(Token { meaning, end_index }) =
                BoolConst::parse_in_context(src, index, context)
            {
                Token::ok(Const(meaning), end_index)
            } else if let Ok(Token {
                meaning: op,
                end_index: index,
            }) = UnaryOp::parse_in_context(src, index, context)
            {
                let Token {
                    meaning: expression,
                    end_index,
                } = Bool::parse_single_term(src, index, context).map_err(|parse_error| {
                    ParseError::new(
                        src,
                        index,
                        format!("Unary \"{op}\" expects an operand.", op = op.name()),
                    )
                    .following(parse_error)
                })?;
                Token::ok(Unary(op, Box::new(expression)), end_index)
            } else if let Ok(Token {
                meaning: lhs,
                end_index: index,
            }) = Response::parse_in_context(src, index, context)
            {
                let Token {
                    meaning: cmp,
                    end_index: index,
                } = Cmp::parse_in_context(src, index, context).map_err(|parse_error| {
                    ParseError::new(src, index, "Expected a comparison with another response.")
                        .following(parse_error)
                })?;
                match Response::parse_in_context(src, index, context).map_err(|parse_error| {
                    ParseError::new(src, index, "Expected another response after comparison.")
                        .following(parse_error)
                }) {
                    Ok(Token {
                        meaning: rhs,
                        end_index,
                    }) => Token::ok(
                        CompareResponse(cmp, Box::new(lhs), Box::new(rhs)),
                        end_index,
                    ),
                    Err(parse_error) => {
                        // perhaps they tried comparing a response to a Bool, e.g. "foo is true?"
                        let Token {
                            meaning: expression,
                            end_index,
                        } = Self::parse_in_context(src, index, context)
                            .map_err(|next_error| next_error.following(parse_error))?;

                        // foo is true? == "You: true?" is foo?
                        let you = context.you.ok_or(ParseError::new(
                            src, index, "Cannot compare a response to a Boolean unless you ask someone specific!"
                        ).until(end_index))?;
                        Token::ok(
                            CompareResponse(
                                cmp,
                                Box::new(Response::Ask(Question {
                                    person: you,
                                    expression,
                                })),
                                Box::new(lhs),
                            ),
                            end_index,
                        )
                    }
                }
            } else if let Ok(Token {
                meaning: person,
                end_index: index,
            }) = Person::parse_in_context(src, index, context)
            {
                let index = parsing::next_graphic_char(src, index)
                    .ok_or(ParseError::new(src, index, "Unexpected end of line."))?
                    .index();
                let index = StudyKeyword::parse_in_context(src, index, context)?.end_index;
                let Token {
                    meaning: field,
                    end_index,
                } = Field::parse_in_context(src, index, context).map_err(|parse_error| {
                    ParseError::new(
                        src,
                        index,
                        format!("What field were you asking if {person} studies?"),
                    )
                    .following(parse_error)
                })?;
                Token::ok(Studies(person, field), end_index)
            } else {
                ParseError::new(src, index, "Cannot parse expression.").throw()
            }
        }
    }

    /// Apply operator precedence to expressions without parentheses.
    fn reassociate(lhs: Box<Bool>, op: BinaryOp, rhs: Box<Bool>) -> Self {
        use Bool::*;
        if let Binary(left_op, lhs, mid) = *lhs {
            if left_op < op {
                // operator precedence is already respected
                Binary(op, Box::new(Binary(left_op, lhs, mid)), rhs)
            } else {
                // may need to recursively reassociate on the left
                Binary(left_op, Box::new(Self::reassociate(lhs, op, mid)), rhs)
            }
        } else {
            Binary(op, lhs, rhs)
        }
    }
}
impl Syntax for Bool {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self> {
        let mut left_token = Self::parse_single_term(src, index, context)?;

        // now, try to append binary ops term-by-term until failure
        while let Ok(Token {
            meaning: op,
            end_index: index,
        }) = BinaryOp::parse_in_context(src, left_token.end_index, context)
        {
            match Self::parse_single_term(src, index, context).map_err(|parse_error| {
                ParseError::new(
                    src,
                    index,
                    format!(
                        "Expected an expression after binary \"{op}\".",
                        op = op.name()
                    ),
                )
                .following(parse_error)
            }) {
                Ok(Token {
                    meaning: rhs,
                    end_index: index,
                }) => {
                    left_token.meaning =
                        Self::reassociate(Box::new(left_token.meaning), op, Box::new(rhs));
                    left_token.end_index = index;
                }
                Err(parse_error) => {
                    if let BinaryOp::Compare(cmp) = op {
                        // perhaps they tried comparing with a response
                        let Token {
                            meaning: response,
                            end_index,
                        } = Response::parse_in_context(src, index, context)
                            .map_err(|next_error| next_error.following(parse_error))?;
                        let you = context.you.ok_or(ParseError::new(
                            src, index, "Cannot interpret Boolean as a response unless you ask someone directly!"
                        ))?;
                        left_token = Token {
                            meaning: Self::CompareResponse(
                                cmp,
                                Box::new(Response::Ask(Question {
                                    person: you,
                                    expression: left_token.meaning,
                                })),
                                Box::new(response),
                            ),
                            end_index,
                        }
                    } else {
                        return parse_error.throw();
                    }
                }
            }
        }
        Ok(left_token)
    }
}

impl Syntax for UnaryOp {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        _context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use UnaryOp::*;
        match src[index].character() {
            '!' | 'n' => {
                let end_index = parsing::full_match_any(src, index, Not.aliases())
                    .take_if(|index| parsing::end_of_token(src, *index))
                    .ok_or(ParseError::new(
                        src,
                        index,
                        format!(
                            "Cannot parse unary op. Did you mean \"{op}\"?",
                            op = Not.name()
                        ),
                    ))?;
                Token::ok(Not, end_index)
            }
            _ => ParseError::new(src, index, "Cannot parse unary op.").throw(),
        }
    }
}

impl Syntax for BinaryOp {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use BinaryOp::*;
        match src[index].character() {
            '&' | 'a' => And.match_aliases(src, index),
            '|' | 'o' => Or.match_aliases(src, index),
            _ => Implies.match_aliases(src, index).or_else(|implies_error| {
                Cmp::parse_in_context(src, index, context).map_or_else(
                    |cmp_error| {
                        if src[index].character() == '=' {
                            cmp_error.following(implies_error).throw()
                        } else {
                            cmp_error.throw()
                        }
                    },
                    |Token {
                         meaning: cmp,
                         end_index,
                     }| Token::ok(Compare(cmp), end_index),
                )
            }),
        }
    }
}

impl Syntax for StudyKeyword {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        _context: Self::Context,
    ) -> ParseResult<'_, Self> {
        let end_index = parsing::full_match_any(src, index, ["studies", "study", "in"])
            .take_if(|index| parsing::end_of_token(src, *index))
            .ok_or(
                ParseError::new(
                    src,
                    index,
                    format!("Expected the keyword \"{}\".", "studies".blue()),
                )
                .maybe_until(
                    parsing::next_char_with(src, index, char::is_ascii_whitespace)
                        .map(IndexedChar::index),
                ),
            )?;
        Token::ok(Self {}, end_index)
    }
}

impl Syntax for BoolConst {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        _context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use BoolConst::*;
        True.match_aliases(src, index)
            .or_else(|_| False.match_aliases(src, index))
    }
}

impl Syntax for Response {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use Response::*;
        if let Ok(Token {
            meaning: question,
            end_index,
        }) = Question::parse_in_context(src, index, context)
        {
            Token::ok(Ask(question), end_index)
        } else {
            let Token { meaning, end_index } =
                ResponseConst::parse_in_context(src, index, context)?;
            Token::ok(Const(meaning), end_index)
        }
    }
}

impl Syntax for ResponseConst {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        _context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use ResponseConst::*;
        match src[index].character() {
            'f' | 'F' => Foo.match_aliases(src, index),
            'b' | 'B' => Bar.match_aliases(src, index).or_else(|bar_error| {
                Baz.match_aliases(src, index)
                    .or_else(|baz_error| baz_error.following(bar_error).throw())
            }),
            _ => ParseError::new(src, index, "Failed to parse response.").throw(),
        }
    }
}

impl Syntax for Cmp {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        _context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use Cmp::*;
        match src[index].character() {
            '=' | 'i' | 'I' => Is.match_aliases(src, index),
            '!' | 'n' | 'N' | 'x' | 'X' => Not.match_aliases(src, index),
            _ => ParseError::new(src, index, "Failed to parse as comparison.").throw(),
        }
    }
}

impl Syntax for Field {
    type Context = ParseContext;
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        _context: Self::Context,
    ) -> ParseResult<'_, Self> {
        use Field::*;
        match src[index].character() {
            'M' | 'm' => Mathematics.match_aliases(src, index),
            'P' | 'p' => Physics.match_aliases(src, index).or_else(|phys_error| {
                Philosophy
                    .match_aliases(src, index)
                    .or_else(|phil_error| phil_error.following(phys_error).throw())
            }),
            'E' | 'e' => Engineering.match_aliases(src, index),
            _ => ParseError::new(src, index, "Failed to parse field name.").throw(),
        }
    }
}

//////// Colour palettes ////////

impl SyntaxHighlight for Question {
    fn pretty(&self) -> String {
        format!(
            "{person}{colon} {expr}{qmark}",
            person = self.person.pretty(),
            colon = ":".yellow(),
            expr = self.expression.pretty(),
            qmark = "?".yellow(),
        )
    }
}

impl SyntaxHighlight for Person {
    fn pretty(&self) -> String {
        self.name().bold().cyan().to_string()
    }
}

impl SyntaxHighlight for Bool {
    fn pretty(&self) -> String {
        use Bool::*;
        match self {
            Wrapped(expression) => expression.pretty(),
            Unary(unary_op, expr) => {
                format!("{op} {expr}", op = unary_op.pretty(), expr = expr.pretty())
            }
            Binary(binary_op, lhs, rhs) => {
                format!(
                    "{open}{lhs} {op} {rhs}{close}",
                    open = "(".dimmed(),
                    op = binary_op.pretty(),
                    lhs = lhs.pretty(),
                    rhs = rhs.pretty(),
                    close = ")".dimmed(),
                )
            }
            CompareResponse(cmp, lhs, rhs) => {
                format!(
                    "{lhs} {cmp} {rhs}",
                    cmp = cmp.pretty(),
                    lhs = lhs.pretty(),
                    rhs = rhs.pretty(),
                )
            }
            Studies(person, field) => {
                format!(
                    "{person} {studies} {field}",
                    person = person.pretty(),
                    studies = "studies".blue(),
                    field = field.pretty(),
                )
            }
            Const(value) => value.pretty(),
        }
    }
}

impl SyntaxHighlight for UnaryOp {
    fn pretty(&self) -> String {
        self.name().red().to_string()
    }
}

impl SyntaxHighlight for BinaryOp {
    fn pretty(&self) -> String {
        match self {
            Self::Compare(Cmp::Is) => "if and only if",
            Self::Compare(Cmp::Not) => "xor",
            _ => self.name(),
        }
        .bright_blue()
        .to_string()
    }
}

impl SyntaxHighlight for Cmp {
    fn pretty(&self) -> String {
        self.name().bright_magenta().to_string()
    }
}

impl SyntaxHighlight for Response {
    fn pretty(&self) -> String {
        use Response::*;
        match self {
            Ask(question) => format!(
                "{quot}{question}{quot}",
                quot = "\"".dimmed().yellow(),
                question = question.pretty()
            ),
            Const(response) => response.pretty(),
        }
    }
}

impl SyntaxHighlight for Field {
    fn pretty(&self) -> String {
        self.name().bold().magenta().to_string()
    }
}

impl SyntaxHighlight for BoolConst {
    fn pretty(&self) -> String {
        use BoolConst::*;
        match self {
            True => self.name().green(),
            False => self.name().red(),
        }
        .bold()
        .to_string()
    }
}

impl SyntaxHighlight for ResponseConst {
    fn pretty(&self) -> String {
        use ResponseConst::*;
        match self {
            Foo => self.name().green(),
            Bar => self.name().blue(),
            Baz => self.name().yellow(),
        }
        .bold()
        .to_string()
    }
}

//////// Display implementations ////////

impl Display for Question {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for Person {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for Bool {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for UnaryOp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for BinaryOp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for Response {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for Cmp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for ResponseConst {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

impl Display for Field {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.pretty())
    }
}

//////// DSL context ////////

#[derive(Clone, Copy, Default)]
pub struct ParseContext {
    you: Option<Person>,
}

//////// Other implementations ////////

trait Aliases
where
    Self: Syntax,
{
    fn aliases(&self) -> &'static [&'static str];
    fn name(&self) -> &'static str {
        self.aliases()[0]
    }
    fn match_aliases(self, src: &IndexedString, index: usize) -> ParseResult<'_, Self> {
        let end_index = parsing::full_match_any(src, index, self.aliases())
            .take_if(|index| parsing::end_of_token(src, *index))
            .ok_or(
                ParseError::new(
                    src,
                    index,
                    format!(
                        "Could not parse token. Did you mean \"{name}\"?",
                        name = self.name()
                    ),
                )
                .maybe_until(
                    parsing::next_char_with(src, index, char::is_ascii_whitespace)
                        .map(IndexedChar::index),
                ),
            )?;
        Token::ok(self, end_index)
    }
}

impl Aliases for Person {
    fn aliases(&self) -> &'static [&'static str] {
        use Person::*;
        match self {
            Alice => &["Alice", "alice", "A", "a"],
            Bob => &["Bob", "bob", "B", "b"],
            Charlie => &["Charlie", "charlie", "C", "c"],
            Dan => &["Dan", "dan", "D", "d"],

            Mathematician => &["Mathematician", "mathematician", "Math", "math"],
            Physicist => &["Physicist", "physicist", "Phys", "phys"],
            Engineer => &["Engineer", "engineer", "Engg", "engg"],
            Philosopher => &["Philosopher", "philosopher", "Phil", "phil"],
        }
    }
}

impl Aliases for UnaryOp {
    fn aliases(&self) -> &'static [&'static str] {
        use UnaryOp::*;
        match self {
            Not => &["not", "!"],
        }
    }
}

impl Aliases for BinaryOp {
    fn aliases(&self) -> &'static [&'static str] {
        use BinaryOp::*;
        match self {
            And => &["and", "&&"],
            Or => &["or", "||"],
            Implies => &["implies", "=>"],
            Compare(cmp) => cmp.aliases(),
        }
    }
}

impl Aliases for BoolConst {
    fn aliases(&self) -> &'static [&'static str] {
        use BoolConst::*;
        match self {
            True => &["True", "true", "1"],
            False => &["False", "false", "0"],
        }
    }
}

impl Aliases for ResponseConst {
    fn aliases(&self) -> &'static [&'static str] {
        use ResponseConst::*;
        match self {
            Foo => &["Foo", "foo"],
            Bar => &["Bar", "bar"],
            Baz => &["Baz", "baz"],
        }
    }
}

impl Aliases for Cmp {
    fn aliases(&self) -> &'static [&'static str] {
        use Cmp::*;
        match self {
            Is => &["is", "iff", "=="],
            Not => &["not", "xor", "!="],
        }
    }
}

impl Aliases for Field {
    fn aliases(&self) -> &'static [&'static str] {
        use Field::*;
        match self {
            Mathematics => &["Mathematics", "mathematics", "Math", "math"],
            Physics => &["Physics", "physics", "Phys", "phys"],
            Engineering => &["Engineering", "engineering", "Engg", "engg"],
            Philosophy => &["Philosophy", "philosophy", "Phil", "phil"],
        }
    }
}
