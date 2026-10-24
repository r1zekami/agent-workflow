# Code report

After implementing code, the final message in the chat is a report with the sections below, in this order. A section with nothing to say is omitted, never filled with "n/a". A list of changed files is never part of the report: changes per release go to the release notes.

1. **Signatures off plan**: only signatures that differ from the approved proposal (rule `code-negotiation`) or were not in it, in the same format, each with one line on why. Signatures that match the proposal are not repeated.
2. **Pipeline**: a text diagram: from where, through what, to where.
3. **Payloads**: every payload the pipeline builds, each shown whole in the notation of rule `code-negotiation`.
4. **How to verify**: command and expected result, plus what was already run.
5. **Not done**: assumptions and open questions.
