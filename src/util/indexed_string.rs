//! Convenience types for string parsing.

use std::fmt::{Debug, Formatter, Result};

#[derive(Clone, Copy, PartialEq, Eq)]
pub struct IndexedChar {
    idx: usize,
    ch: char,
}

impl IndexedChar {
    pub fn index(&self) -> usize {
        self.idx
    }
    pub fn character(&self) -> char {
        self.ch
    }
}

impl Debug for IndexedChar {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "[{ch}/{idx}]", ch = self.ch, idx = self.idx)
    }
}

pub type IndexedString = Vec<IndexedChar>;

pub trait ToIndexedString {
    fn to_indexed_string(&self) -> IndexedString;
}

impl ToIndexedString for str {
    fn to_indexed_string(&self) -> IndexedString {
        self.chars()
            .enumerate()
            .map(|(idx, ch)| IndexedChar { idx, ch })
            .collect()
    }
}

impl ToIndexedString for IndexedString {
    fn to_indexed_string(&self) -> IndexedString {
        String::de_index(self).to_indexed_string()
    }
}

pub trait DeIndexString {
    fn de_index(indexed_string: &IndexedString) -> Self;
}

impl DeIndexString for String {
    fn de_index(indexed_string: &IndexedString) -> Self {
        indexed_string.iter().map(IndexedChar::character).collect()
    }
}
