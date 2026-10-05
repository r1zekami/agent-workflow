# LiteLLM — gateway for worker agents

One local, OpenAI-compatible endpoint for every worker agent. Workers ask for an
alias; this gateway holds the provider keys, enforces budgets and logs usage.
Claude Code itself never goes through it.

| What | Where |
|---|---|
| Templates (this folder, in git) | `claude-code-setup/services/litellm/` |
| Runtime copy (with `.env`) | WSL `~/services/litellm/` |
| API | `http://127.0.0.1:4000` — from WSL and from Windows, not from the network |
| Admin UI | `http://127.0.0.1:4000/ui` — database admin users only |

## Aliases

| Alias | Model |
|---|---|
| `worker-deepseek-flash` | DeepSeek Flash — default worker |
| `worker-deepseek-v4-pro` | DeepSeek V4 Pro — harder tasks |

Add a model: a new entry in `config.yaml` (alias `worker-<provider>-<model>`,
explicit prices), its key in `.env`, then restart.

## First start (WSL)

```bash
mkdir -p ~/services/litellm && cd ~/services/litellm
cp /mnt/c/Users/<user>/home/agents/claude-code-setup/services/litellm/{compose.yaml,config.yaml,.env.example} .
umask 077; printf 'LITELLM_MASTER_KEY=sk-%s\nLITELLM_SALT_KEY=sk-%s\nPOSTGRES_PASSWORD=%s\nDEEPSEEK_API_KEY=\n' "$(openssl rand -hex 32)" "$(openssl rand -hex 32)" "$(openssl rand -hex 24)" > .env
nano .env          # paste the DeepSeek key
docker compose up -d && docker compose ps
```

Then in the admin UI:
1. **Own admin account** — `config.yaml` sets `disable_env_credential_login: true`,
   so on a fresh start comment that line out first and sign in as `admin` with
   the master key. Internal Users → Invite User, role Admin, open the link, set a
   password, sign in with it. Then restore the line and restart.
2. **Worker key** — Virtual Keys → Create New Key: only the `worker-*` models,
   max budget and a reset period. Workers only ever get that key — never the
   master key or provider keys.

## Operate

| Task | Command (in `~/services/litellm`) |
|---|---|
| Status | `docker compose ps` |
| Logs | `docker compose logs -f litellm` |
| Restart after a config change | `docker compose up -d --force-recreate litellm` |
| Stop / start | `docker compose stop` / `docker compose start` |
| Update | bump the image tag and digest in `compose.yaml` here, copy it over, `docker compose up -d` |

The containers restart with Docker, so the gateway comes up whenever WSL starts.
Keep `.env`: a new `LITELLM_SALT_KEY` makes stored credentials unreadable.

## Privacy

Outbound calls besides the providers are off: the price map and the UI blog
feed are read from the image (`LITELLM_LOCAL_*` in `compose.yaml`).
