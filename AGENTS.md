# Repository Guidelines

## Project Structure & Module Organization
`bot.py` orchestrates the Telegram application and wires the command handlers defined in `handlers/user_commands.py`, `handlers/verify_commands.py`, and `handlers/admin_commands.py`. Service-specific logic, assets, and docs live in the sibling directories (`Boltnew/`, `k12/`, `military/`, `one/`, `spotify/`, `youtube/`), so place any new verification flow alongside its peers. Shared data access sits in `database_mysql.py`, helpers in `utils/`, and configuration defaults in `config.py` plus `env.example`. Deployment notes are documented in `DEPLOY.md`, while container assets are in `Dockerfile` and `docker-compose.yml`.

## Build, Test, and Development Commands
Create a virtual environment, install the pinned runtime dependencies, and download the Playwright browser that renders ID cards before running the bot:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
python bot.py
```
Use `docker compose up -d` for parity with production, and `docker compose logs -f bot` to observe runtime behavior. Keep `.env` aligned with `env.example` to avoid missing configuration keys.

## Coding Style & Naming Conventions
Stick to Python 3.11 features, 4-space indents, and `snake_case` for functions or module-level helpers. Handlers should be asynchronous (`async def verify3_command`) and accept injected collaborators (e.g., `db`) via `functools.partial` just like the existing ones. Service classes or utilities should adopt descriptive CamelCase names (`SpotifyVerifier`) while constants remain `UPPER_SNAKE_CASE`. Reuse the central `logging.basicConfig` configuration and emit actionable log messages that identify the SheerID `programId` or Telegram user involved.

## Testing Guidelines
Automated coverage is currently light, so every contribution should include at least a reproducible manual scenario: run `python bot.py`, point `.env` at a staging MySQL schema, and exercise the relevant `/verify*` command with a redacted SheerID URL to prove success/failure handling. When adding pure functions (e.g., data generators in `utils/`), accompany them with `tests/test_<module>.py` and call them via `python -m pytest tests -k generator` so reviewers can rerun them quickly. Capture logs from `docker compose logs -f bot` in the pull request when fixing regressions.

## Commit & Pull Request Guidelines
Follow the short, descriptive style already present in history (`feat: add Spotify and YouTube verification`, `chore: remove update summary document`). Start messages with an imperative verb, keep the subject under ~72 characters, and reference tracking issues using `Fixes #123` in the body. Pull requests should describe motivation, outline config/database changes, list the commands you ran, and attach screenshots or Telegram transcript snippets that demonstrate the bot’s responses. If you touch service modules, mention which SheerID `programId` or provider the change targets so reviewers know what to retest.

## Security & Configuration Tips
Never commit `.env`, private keys, or database dumps; rely on `env.example` for placeholders. Limit the MySQL user you configure in `database_mysql.py` to the minimum privileges needed for CRUD on the bot schema. Rotate Telegram Bot API tokens immediately if they are suspected to leak into logs. When sharing reproduction steps, sanitize verification links because they embed `verificationId` tokens that can be used to impersonate users. Consult `DEPLOY.md` before changing Docker images so that required Playwright fonts and Chromium dependencies remain intact.
