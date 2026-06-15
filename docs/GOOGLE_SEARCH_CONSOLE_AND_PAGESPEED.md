# Google Search Console And PageSpeed Insights

This guide covers the Google tools included in the handoff package.

## Files

```text
tools/seo/google/gsc_export.py
tools/seo/google/pagespeed_export.py
tools/seo/google/requirements.txt
tools/seo/google/.env.example
```

## Google Cloud Setup

For Search Console OAuth:

1. Open Google Cloud Console.
2. Create or select a project.
3. Enable the Google Search Console API.
4. Configure the OAuth consent screen if required.
5. Create an OAuth Desktop client.
6. Download the JSON credentials file.
7. Save it locally as:

```text
tools/seo/google/client_secret.json
```

For PageSpeed Insights:

1. Enable the PageSpeed Insights API.
2. Create an API key.
3. Put the key in `tools/seo/.env` as:

```text
PAGESPEED_API_KEY=
```

## Search Console Credential Options

Preferred local OAuth:

```text
GOOGLE_CLIENT_SECRETS_FILE=client_secret.json
GOOGLE_TOKEN_FILE=token.json
```

Service account:

```text
GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json
```

Important: the service account email must be added as a Search Console user for the property.

Temporary access token:

```text
GOOGLE_ACCESS_TOKEN=
```

Run with:

```bash
python3 gsc_export.py --mode sites --auth-mode bearer-token
```

This expires and is only useful for one-off checks.

## Search Console Property

Set the exact property string:

```text
GSC_SITE_URL=https://example.com/
```

or:

```text
GSC_SITE_URL=sc-domain:example.com
```

## Commands

Install dependencies:

```bash
cd tools/seo/google
python3 -m pip install -r requirements.txt
```

List properties:

```bash
python3 gsc_export.py --mode sites
```

Export everything:

```bash
python3 gsc_export.py --mode all
```

Export Search Analytics only:

```bash
python3 gsc_export.py --mode search-analytics --dimensions query,page
```

Run PageSpeed:

```bash
python3 pagespeed_export.py --strategy both
```

Run PageSpeed for explicit URLs:

```bash
python3 pagespeed_export.py --url https://example.com/ --url https://example.com/about/ --strategy both
```

Save raw PageSpeed JSON:

```bash
python3 pagespeed_export.py --strategy both --save-json
```

## Output Files

Search Console:

```text
tools/seo/google/outputs/gsc_sites.csv
tools/seo/google/outputs/gsc_sitemaps_SITE.csv
tools/seo/google/outputs/gsc_search_analytics_SITE_START_END_DIMENSIONS.csv
```

PageSpeed:

```text
tools/seo/google/outputs/pagespeed_summary_TIMESTAMP.csv
tools/seo/google/outputs/raw/pagespeed_URL_STRATEGY_TIMESTAMP.json
```

## How To Use With Wincher

Use Wincher to identify tracked keyword rankings.

Use Search Console to validate:

- impressions
- clicks
- CTR
- average position
- query/page pairings

Use PageSpeed to prioritize technical fixes:

- slow LCP pages
- high total blocking time
- layout shift issues
- SEO/accessibility warnings

Cross-check all three before editing content.
