# Deployment Guide

Use this guide in the target website repository.

## 1. Copy Files

Copy these package folders into the target repo:

```text
tools/seo/
docs/
codex/
```

At minimum, the target repo needs:

```text
tools/seo/.env.example
tools/seo/wincher/
tools/seo/google/
docs/GITIGNORE_SNIPPET.txt
```

## 2. Update `.gitignore`

Append the contents of:

```text
docs/GITIGNORE_SNIPPET.txt
```

to the target repository `.gitignore`.

## 3. Create Local Credentials

From target repo root:

```bash
cp tools/seo/.env.example tools/seo/.env
```

Fill:

```text
WINCHER_API_TOKEN=your_real_token
WINCHER_WEBSITE_ID=optional_default_website_id
GSC_SITE_URL=https://example.com/
GOOGLE_CLIENT_SECRETS_FILE=client_secret.json
GOOGLE_TOKEN_FILE=token.json
PAGESPEED_API_KEY=optional_pagespeed_key
PAGESPEED_URLS=https://example.com/,https://example.com/about/
WEBSITE_DOMAIN=https://example.com
GITHUB_REPOSITORY=owner/repo
```

If `WINCHER_WEBSITE_ID` is unknown, leave it blank and find it after installing dependencies.

## 4. Install Dependencies

Wincher:

```bash
cd tools/seo/wincher
python3 -m pip install -r requirements.txt
```

Google:

```bash
cd ../google
python3 -m pip install -r requirements.txt
```

## 5. Configure Google Search Console

For OAuth:

1. Enable the Google Search Console API in Google Cloud Console.
2. Create an OAuth Desktop client.
3. Download the OAuth JSON.
4. Save it locally as:

```text
tools/seo/google/client_secret.json
```

The first OAuth run opens a browser and writes:

```text
tools/seo/google/token.json
```

Both files must stay local and ignored.

For PageSpeed:

1. Enable PageSpeed Insights API.
2. Create an API key if repeated automated calls are expected.
3. Store it in `tools/seo/.env` as `PAGESPEED_API_KEY`.

## 6. Verify Wincher API Access

```bash
cd tools/seo/wincher
python3 wincher_connector.py --mode websites
```

This should print website IDs, domains, display names, keyword counts, and online status.

Do not paste the API token into terminal output or chat.

## 7. Find The Wincher Website ID

Use the website ID shown by:

```bash
python3 wincher_connector.py --mode websites
```

Then add it to:

```text
tools/seo/.env
```

as:

```text
WINCHER_WEBSITE_ID=123456
```

## 8. Verify Google API Access

Search Console:

```bash
cd ../google
python3 gsc_export.py --mode sites
```

PageSpeed:

```bash
python3 pagespeed_export.py --url https://example.com/ --strategy both
```

## 9. Export Data

Wincher:

```bash
cd ../wincher
python3 wincher_export.py --mode all --website-id YOUR_WEBSITE_ID
```

Search Console:

```bash
cd ../google
python3 gsc_export.py --mode all
```

PageSpeed:

```bash
python3 pagespeed_export.py --strategy both
```

Expected outputs:

```text
tools/seo/wincher/outputs/wincher_websites.csv
tools/seo/wincher/outputs/wincher_keywords_YOUR_WEBSITE_ID.csv
tools/seo/google/outputs/gsc_sites.csv
tools/seo/google/outputs/gsc_sitemaps_*.csv
tools/seo/google/outputs/gsc_search_analytics_*.csv
tools/seo/google/outputs/pagespeed_summary_*.csv
```

## 10. Commit Policy

Usually commit:

- `tools/seo/wincher/*.py`
- `tools/seo/wincher/requirements.txt`
- `tools/seo/wincher/.env.example`
- `tools/seo/google/*.py`
- `tools/seo/google/requirements.txt`
- `tools/seo/google/.env.example`
- docs
- `.gitignore` updates

Never commit:

- `tools/seo/.env`
- `tools/seo/wincher/.env`
- `tools/seo/google/.env`
- `tools/seo/wincher/outputs/`
- `tools/seo/google/outputs/`
- `tools/seo/google/token.json`
- `tools/seo/google/client_secret*.json`
- `tools/seo/google/credentials*.json`
- `tools/seo/google/service-account*.json`
- tokens, secrets, screenshots of credentials, or copied API responses containing private data
