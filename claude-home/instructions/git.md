## Git workflow: short rules

**Push hard gate**: never push to a remote repository without explicit
permission. Either get a clear yes from the user for that specific push, or ask
the user to run it. This holds regardless of branch, how trivial the change
looks, or whether a prior push was already approved: approval does not carry
over to the next push. Before asking for a push, run the `leak-auditor` subagent
on everything the push would send, and include its verdict in the request.

**Commit title**: `type(scope): short description`: `feat`/`fix`/`refactor`/etc.,
the module or entity name in the project as scope, and one concise line of what
was done.
```
fix(export): fix incorrect status rendering in logs
```

**Commit body**: brief and factual, a little more detail than the title. No
local or incidental nuances, no rationale, no minor signature tweaks. State what
was done, not why or what almost happened along the way.

**Co-authorship footer**: keep whatever attribution trailer the current session
was given (e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`). This
is a separate, session-level requirement, not replaced by this file.

**No agent artifacts in the repo**: scratch files, logs, and other byproducts of
the agent's run must never be committed. Either do not stage them or make sure
`.gitignore` covers them. Check before committing.
