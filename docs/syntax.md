# Question grammar

Everyone at Boolos' Brewery speaks English, but my program cannot, so we make do with a much more limited language.
The grammar is as follows:

| Symbol |   | Definition |
| ------:|:-:|:---------- |
| *question* |:| *person* `:` *bool* `?` |
||\|| `"` *question* `"` |
||;||
| *person* |:| `A` \| `Alice` |
||\|| `B` \| `Bob` |
||\|| `C` \| `Charlie`[^1] |
||\|| `D` \| `Dan`[^2] |
||;||
| *bool* |:| `(` *bool* `)` |
||\|| *unary\_op* *bool* |
||\|| *bool* *binary\_op* *bool* |
||\|| *response* *cmp* *response* |
||\|| *person* `studies` *field* |
||\|| `1` \| `true` |
||\|| `0` \| `false` |
||;||
| *unary\_op* |:| `!` \| `not` |
||;||
| *binary\_op*[^3] |:| `&&` \| `and` |
||\|| `\|\|` \| `or` |
||\|| `=>` \| `implies` |
||\|| *cmp* |
||;||
| *cmp* |:| `==` \| `is` \| `iff` |
||\|| `!=` \| `not` \| `xor` |
||;||
| *response* |:| *question* |
||\|| `foo` |
||\|| `bar` |
||\|| `baz`[^2] |
||;||
| *field* |:| `Math` \| `Mathematics` |
||\|| `Phys` \| `Physics` |
||\|| `Engg` \| `Engineering`[^1] |
||\|| `Phil` \| `Philosophy`[^2] |
||;||


### Syntax sugar
`You` or `U` can be used to refer to the person being asked the (inner-most) question.
```yaml
Alice: You study mathematics?
# translates to
Alice: Alice studies mathematics?
```

You may also compare a *response* with a *bool*.
```yaml
Alice: Foo is true?
# translates to
Alice: "Alice: True?" is foo?
```

[^1]: Valid except in [easy mode](variants.md#easy-mode).
[^2]: Valid only in [hard mode](variants.md#the-hardest-er-logic-puzzle-ever-️).
[^3]: Operations are sorted by operator precedence.