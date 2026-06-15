# Google Search Console And PageSpeed Connector

This folder contains read-only local helpers for Google Search Console and PageSpeed Insights.

## What It Does

- Exports Search Console properties to CSV.
- Exports Search Console sitemaps to CSV.
- Exports Search Analytics rows to CSV.
- Runs PageSpeed Insights for one or more public URLs.
- Keeps credentials local and ignored by Git.

## Setup

Install dependencies from this folder:

```bash
python3 -m pip install -r requirements.txt
```

Create a shared credentials file in the target repo:

```text
tools/seo/.env
```

The scripts also read `tools/seo/google/.env` as a fallback.

## Search Console Auth Options

Use one of:

- OAuth desktop/client credentials: `GOOGLE_CLIENT_SECRETS_FILE` and `GOOGLE_TOKEN_FILE`.
- Service account: `GOOGLE_SERVICE_ACCOUNT_FILE`, with that service account added as a Search Console user.
- Temporary OAuth access token: `GOOGLE_ACCESS_TOKEN` and `--auth-mode bearer-token`.

Required Search Console scope:

```text
https://www.googleapis.com/auth/webmasters.readonly
```

## PageSpeed Auth

`PAGESPEED_API_KEY` is optional for light usage and recommended for repeated automated runs.

## Commands

List Search Console properties:

```bash
python3 gsc_export.py --mode sites
```

Export Search Console sites, sitemaps, and Search Analytics:

```bash
python3 gsc_export.py --mode all
```

Export query/page data for a date range:

```bash
python3 gsc_export.py --mode search-analytics --dimensions query,page --start-date 2026-05-01 --end-date 2026-05-31
```

Run PageSpeed for URLs from `.env`:

```bash
python3 pagespeed_export.py --strategy both
```

Run PageSpeed for one URL:

```bash
python3 pagespeed_export.py --url https://example.com/ --strategy both
```

Outputs are written to:

```text
tools/seo/google/outputs/
```

## Safety

- Do not print or expose API keys, OAuth tokens, refresh tokens, client secrets, or service account JSON.
- Do not commit `.env`, `token.json`, `client_secret*.json`, service account JSON, or `outputs/`.
- Search Console uses read-only scope.
- PageSpeed requests are GET-only.
