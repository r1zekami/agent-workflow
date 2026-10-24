# Sensitive infrastructure data: hard rule

When working with an external API or aggregating data from real systems, specifics never go into the chat: host and machine names, directory and inventory structure (folders, groups, pools), user names, IPs, domains and other near-sensitive details.

Allowed, in this order of preference:
1. **Bare statistics** (default): numbers with a description, no names.
2. **Mask at extraction**: aggregate or mask inside the script that pulls the data, so raw values never reach the agent's context. Only the masked or aggregated result is printed; raw API responses are never dumped to stdout.
3. **Real values, pointwise**: only on the user's explicit request for that specific item. The request covers that item, not the rest of the dataset.

The same applies to reasoning, issues, commit messages, specs, notes and session logs. Test fixtures and examples use made-up names, never values from a real dump.

When unsure whether something is safe to show or save, ask. Anything that leaves the machine by a push is audited first. If specifics leak into the chat anyway, say so.
