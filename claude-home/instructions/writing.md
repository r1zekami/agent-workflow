## Writing: READMEs, docs, notes, articles

Scope: every text meant to be read later by a person. READMEs, docs, specs,
second-brain notes, articles, commit bodies, issue and PR text. Not the chat
with the user. Applies in every approach and in every language: language.md
chooses the language, this file chooses the style.

The text must read as if a careful person wrote it as documentation: clear,
neutral, and only as long as it needs to be.

### 1. Impersonal, no trace of the conversation

The text describes the system, not how the text came to be.

- No author and no audience: no "I", "we", "you", "Claude", "the assistant".
- No decision history: not "the user decided", "confirmed", "agreed",
  "as requested", "per the discussion". A decision is written as a fact, with
  the reason only if there is one: `Tokens are read from the environment. Reason: the file is never shared.`
- "User" only means a user of the described system.
- No meta text: no "this document describes", "in this section", "as mentioned
  above", no summary that repeats the text.
- The text stands on its own. It is not a patch to an earlier version: no
  "now", "no longer", "was changed to", unless the change itself is the topic
  (a changelog or a decision record).

### 2. Plain wording, no filler

- Short sentences, one idea each. Concrete nouns, ordinary verbs.
- Cut anything the reader does not need: obvious statements, the history of
  how something was found, praise, warnings with no consequence.
- No intensifiers and no marketing words: robust, seamless, powerful,
  comprehensive, leverage, ensure, crucial, key, simply, just.
- No filler openers or closers: "It is worth noting", "Importantly", "In
  summary", "Overall".
- No patterns typical for generated text: "not just X, but Y", lists of three
  adjectives, rhetorical questions, a header over two sentences, bold in
  every line, emoji.
- Do not hedge what is known, and state a doubt once, where it applies.

### 3. No long dashes

No em dash and no en dash as punctuation. Use a colon, a comma, parentheses,
a period, or rebuild the sentence. A range uses a hyphen or "to" (`3-5`,
`from 3 to 5`). An empty table cell is `-`.

### 4. Formal, not figurative

Say what happens with the plain verb, not with a picture. Active or passive
voice is fine, the subject is the thing, not a person.

| Avoid | Write |
|---|---|
| The test guards the syntax. | The syntax is checked by `test_syntax`. |
| The module lives in `core/`. | The module is located in `core/`. |
| The hook catches bad input. | The hook rejects invalid input. |
| The cache knows when to expire. | The cache entry expires after 10 minutes. |
| This kicks off the build. | This starts the build. |

Personification (guards, protects, knows, wants, sits, lives, owns), slang and
idioms are out. Formal does not mean heavy: a simple thing stays a simple
sentence: "Run `make test`." is better than "The test suite may be executed by
invoking make test."

### 5. Precision where it matters

- Names, paths, commands, values and versions are exact and in backticks.
- A claim names its object: "the config is validated", not "it is validated".
- Numbers carry their unit. A rule carries its condition.

### Before finishing a text

Re-read once and check: no "I/we/you/user decided", no dash characters, no
filler or figurative verbs, nothing that the reader can do without. Fix in
place, do not add a note about the fix.
