# Credentials

## Wincher

```text
WINCHER_API_TOKEN
```

This is the bearer token used for the Wincher REST API.

## Optional But Recommended

```text
WINCHER_WEBSITE_ID
```

This avoids passing `--website-id` every time.

## Credential File Location

Preferred shared location:

```text
tools/seo/.env
```

Fallback connector-specific location:

```text
tools/seo/wincher/.env
```

The scripts load both, with `tools/seo/.env` first and connector-local `.env` second.

## Example

```text
WINCHER_API_TOKEN=replace_with_real_token
WINCHER_WEBSITE_ID=123456
WEBSITE_DOMAIN=https://example.com
GITHUB_REPOSITORY=owner/repo
```

## Finding `WINCHER_WEBSITE_ID`

Run:

```bash
cd tools/seo/wincher
python3 wincher_connector.py --mode websites
```

Use the ID printed beside the matching domain.

## Security Rules

- Never commit `.env`.
- Never paste `WINCHER_API_TOKEN` into Codex, chat, GitHub issues, PR descriptions, logs, or screenshots.
- If a token is exposed, rotate it in Wincher before continuing.
- Keep exported CSVs local unless the repository owner explicitly wants SEO snapshots committed.

## Google Search Console

Required:

```text
GSC_SITE_URL
```

Use the exact property string from Search Console:

```text
https://example.com/
```

or:

```text
sc-domain:example.com
```

Use one authentication method.

OAuth desktop/client:

```text
GOOGLE_CLIENT_SECRETS_FILE=client_secret.json
GOOGLE_TOKEN_FILE=token.json
```

Service account:

```text
GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json
```

Temporary bearer token:

```text
GOOGLE_ACCESS_TOKEN=
```

Notes:

- Search Console does not use a simple API key for private property data.
- OAuth uses read-only scope: `https://www.googleapis.com/auth/webmasters.readonly`.
- `token.json` may contain a refresh token. Treat it as a secret.
- Service accounts must be added as Search Console users before they can read a property.

## PageSpeed Insights

Optional:

```text
PAGESPEED_API_KEY=
```

Recommended for frequent automated runs.

URLs:

```text
PAGESPEED_URLS=https://example.com/,https://example.com/about/
```

## Google Security Rules

- Never commit `token.json`.
- Never commit `client_secret*.json`.
- Never commit service account JSON.
- Never paste access tokens, refresh tokens, API keys, or credential JSON into Codex or GitHub.
- If a Google credential is exposed, revoke or rotate it before continuing.
