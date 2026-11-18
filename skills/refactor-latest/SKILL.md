---
name: refactor-latest
description: Use when the user asks to refactor the changes of the current session to the user's code rules (code-design, code-docs). Sets the scope to the session's changes and runs skill refactor.
---

# Refactor the changes of the current session

Load skill `refactor` and follow it with the scope `refactor-latest`: the changes of the current session.

Text in the user's message next to this skill is additional instructions; it may name a base commit or branch for the scope.
