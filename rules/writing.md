# Writing

The text reads as documentation a careful person wrote: clear, neutral, and only as long as it needs to be. The default language is English; this rule sets the style.

## 1. Impersonal, no trace of the conversation

- No author and no audience: no "I", "we", "you", "Claude", "the assistant".
- No decision history: not "the user decided", "confirmed", "as requested". A decision is a fact, with the reason only if there is one: `Tokens are read from the environment. Reason: the file is never shared.`
- "User" only means a user of the described system.
- No meta text: no "this document describes", "as mentioned above", no summary that repeats the text.
- The text is not a patch to an earlier version: no "now", "no longer", "was changed to", unless the change itself is the topic (changelog, decision record).

## 2. Plain wording, no filler

- Short sentences, one idea each. Concrete nouns, ordinary verbs.
- Cut what the reader does not need: obvious statements, how something was found, praise, warnings with no consequence.
- No intensifiers or marketing words: robust, seamless, powerful, comprehensive, leverage, ensure, crucial, key, simply, just.
- No filler openers or closers: "It is worth noting", "Importantly", "Overall".
- No generated-text patterns: "not just X, but Y", triples of adjectives, rhetorical questions, a header over two sentences, bold in every line, emoji.
- Do not hedge what is known; state a doubt once, where it applies.

## 3. No long dashes

No em dash or en dash as punctuation. Use a colon, comma, parentheses, period, or rebuild the sentence. Ranges: `3-5` or `from 3 to 5`. Empty table cell: `-`.

## 4. Formal, not figurative

| Avoid | Write |
|---|---|
| The test guards the syntax. | The syntax is checked by `test_syntax`. |
| The module lives in `core/`. | The module is located in `core/`. |
| The hook catches bad input. | The hook rejects invalid input. |
| The cache knows when to expire. | The cache entry expires after 10 minutes. |

No personification (guards, protects, knows, wants, lives, owns), slang or idioms. A simple thing stays a simple sentence: "Run `make test`."

## 5. Explicit referent

Every pronoun or demonstrative (it, its, they, this, that, such) resolves to one obvious noun in the same or the previous sentence; otherwise write the noun.

| Bad | Good |
|---|---|
| Take the first row with a label, and its value. | Take the first row with a label, and that row's value. |

## 6. Precision

- No invented figures: numbers and sample data are real and sourced, or clearly marked as examples.
- Names, paths, commands, values and versions are exact and in backticks.
- A claim names its object; numbers carry their unit; a rule carries its condition.

## 7. No hard line wraps

A paragraph or a list item is one line in the file, however long. No line breaks inside a sentence or a paragraph to keep lines at an even width: editors and viewers wrap lines themselves. Line breaks separate only blocks: paragraphs, list items, table rows, headings, code. Code blocks keep their own formatting.

## Before finishing

Re-read once: no "I/we/you/user decided", no dash characters, no filler or figurative verbs, no pronoun without its noun, no line breaks inside a paragraph. Fix in place.
