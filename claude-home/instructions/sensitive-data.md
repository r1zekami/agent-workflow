## Sensitive infrastructure data — HARD RULE

When you work with an external API or aggregate data from real systems,
**specifics never go into the chat with the user**: host and machine names,
directory and inventory structure (folders, groups, pools), usernames, IPs,
domains, and other near-sensitive details.
Allowed, in this order of preference:

1. **(default) Bare statistics** — numbers with a description, no names.
2. **Mask at extraction** — aggregate or mask inside the script that pulls the data,
   so raw values never reach your context at all. Print only the masked or aggregated
   result; don't dump raw API responses to stdout.
3. **Real values — pointwise and ONLY on the user's explicit request** for that
   specific item. The request covers that item, not the rest of the dataset.

When unsure whether something is safe to show, save or send — run the
`leak-auditor` subagent on it first.

The same applies to your reasoning, beads issues, commit messages, specs, and
second-brain notes including the session log; test fixtures use made-up names,
not values from a real dump. If specifics leak into the chat anyway, say so.
