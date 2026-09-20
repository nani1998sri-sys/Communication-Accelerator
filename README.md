# Executive Communication & Career Growth Coach

A Telegram-based AI coach for daily communication practice, executive presence, CMAAS-focused scenarios, debates, presentations, interviews, and handling criticism.

## V1 architecture

- **Code:** Python in GitHub
- **Primary scheduler:** GitHub Actions
- **Backup scheduler:** Cloudflare Worker Cron
- **Interface:** Telegram
- **AI agent:** Python + an OpenAI-compatible LLM API
- **Memory:** local JSON fallback in V1; Supabase can be added later
- **Research:** optional adapter point reserved
- **Documents:** `documents/` folder in V1; add R2 later
- **Monitoring:** GitHub logs and Telegram

## Privacy

Do not paste identifiable client, employer, personal, financial, or confidential information into the bot. Anonymise every example.

## Setup

1. Create an empty GitHub repository.
2. Upload this project or push it with the commands below.
3. Create a Telegram bot using BotFather.
4. Start the bot and send `/chatid`; place the returned ID in `TELEGRAM_ALLOWED_CHAT_ID`.
5. Add the required GitHub Actions secrets.
6. Run the **daily-coach** workflow manually once.
7. Run **telegram-bot** manually for interactive long polling.

```bash
git init
git add .
git commit -m "Initial communication coach agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

## GitHub secrets

Required: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_CHAT_ID`, `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`.
Optional: `SEARCH_API_KEY`, `SEARCH_API_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`.

## Commands

`/start`, `/daily`, `/practice`, `/word`, `/phrase`, `/debate`, `/presentation`, `/interview`, `/feedback`, `/chatid`, `/help`.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.cli daily
python -m app.cli bot
```

## Cloudflare backup

Configure Worker secrets: `GITHUB_OWNER`, `GITHUB_REPO`, `GITHUB_WORKFLOW_ID`, `GITHUB_REF`, `GITHUB_TOKEN`, and `CRON_SHARED_SECRET`. The Worker triggers the GitHub workflow through `workflow_dispatch`.
