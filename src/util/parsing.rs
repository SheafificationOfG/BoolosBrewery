use crate::util::indexed_string::*;

use std::fmt::Display;

use colored::Colorize;

/// Scan `src` from `index` and return the next character satisfying `cond` (if any).
pub fn next_char_with<F>(src: &IndexedString, index: usize, cond: F) -> Option<&IndexedChar>
where
    F: Fn(&char) -> bool,
{
    src[index..].iter().find(|token| cond(&token.character()))
}

/// Scan `src` from `index` and return next graphic character (if any).
pub fn next_graphic_char(src: &IndexedString, index: usize) -> Option<&IndexedChar> {
    next_char_with(src, index, char::is_ascii_graphic)
}

/// Scans from `index` and returns the final index after fully matching with `string_match`,
/// otherwise returning `None`.
pub fn full_match<Str>(src: &IndexedString, mut index: usize, string_match: Str) -> Option<usize>
where
    Str: ToString,
{
    for ch in string_match.to_string().chars() {
        if index < src.len() && src[index].character() == ch {
            index += 1;
        } else {
            return None;
        }
    }
    Some(index)
}

/// Scan from `index` against all strings in `string_matches`, and returns the largest full match;
/// otherwise, returns `None`.
pub fn full_match_any<I>(src: &IndexedString, index: usize, string_matches: I) -> Option<usize>
where
    I: IntoIterator<Item: ToString>,
{
    string_matches
        .into_iter()
        .filter_map(|string_match| full_match(src, index, string_match))
        .max()
}

/// Checks if given index points right after the end of a token
pub fn end_of_token(src: &IndexedString, index: usize) -> bool {
    index == src.len()
        || index == 0
        || !src[index].character().is_ascii_graphic()
        || src[index - 1].character().is_alphanumeric() != src[index].character().is_alphanumeric()
}

/// Parsing rules for question types
pub trait Syntax
where
    Self: Sized,
{
    type Context: Copy + Default;

    /// Parse from `index` assuming first character is non-whitespace.
    fn parse_impl(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self>;

    /// Parse syntax, skipping whitespace.
    fn parse_in_context(
        src: &IndexedString,
        index: usize,
        context: Self::Context,
    ) -> ParseResult<'_, Self> {
        let index = next_graphic_char(src, index)
            .map(IndexedChar::index)
            .take_if(|index| *index < src.len())
            .ok_or(ParseError::new(src, index, "Unexpected end of line!"))?;
        Self::parse_impl(src, index, context)
    }

    /// Frontend parse function
    fn parse(src: &IndexedString) -> ParseResult<'_, Self> {
        Self::parse_in_context(src, 0, Self::Context::default())
    }
}

pub trait SyntaxHighlight
where
    Self: Syntax,
{
    fn pretty(&self) -> String;
}

pub type ParseResult<'a, T> = Result<Token<T>, ParseError<'a>>;

/// Container for parsing information, pointing to the index immediately after the token.
#[derive(Debug)]
pub struct Token<T>
where
    T: Syntax,
{
    pub meaning: T,
    pub end_index: usize,
}

impl<T> Token<T>
where
    T: Syntax,
{
    pub fn ok<E>(meaning: T, end_index: usize) -> Result<Self, E> {
        Ok(Token { meaning, end_index })
    }
}

/// Information for somewhat informative parsing error messages
#[derive(Debug)]
pub struct ParseError<'a> {
    source: &'a IndexedString,
    index: usize,
    index_to: Option<usize>,
    message: String,
    parent: Option<Box<ParseError<'a>>>,
}

impl<'a> ParseError<'a> {
    pub fn new<Str>(source: &'a IndexedString, index: usize, message: Str) -> Self
    where
        Str: ToString,
    {
        ParseError {
            source,
            index,
            index_to: None,
            message: message.to_string(),
            parent: None,
        }
    }

    pub fn until(mut self, index_to: usize) -> Self {
        self.index_to = Some(index_to);
        self
    }

    pub fn maybe_until(mut self, index_to: Option<usize>) -> Self {
        self.index_to = index_to;
        self
    }

    pub fn following(mut self, error: ParseError<'a>) -> Self {
        self.parent = Some(Box::new(error));
        self
    }

    pub fn throw<T>(self) -> ParseResult<'a, T>
    where
        T: Syntax,
    {
        Err(self)
    }
}

impl<'a> Display for ParseError<'a> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if let Some(parent) = &self.parent {
            Display::fmt(parent, f)?;
        }
        writeln!(f, "{}", self.message)?;
        writeln!(
            f,
            "{} {}",
            ">>".white().on_red(),
            String::de_index(self.source).yellow()
        )?;
        write!(
            f,
            "  {space: <offset$}",
            space = ' ',
            offset = self.index + 1
        )?;
        let index_to = self.index_to.unwrap_or(self.index + 1);
        writeln!(
            f,
            "{underline}",
            underline = format!("{caret:~<len$}", caret = '^', len = index_to - self.index,).red(),
        )?;
        Ok(())
    }
}
