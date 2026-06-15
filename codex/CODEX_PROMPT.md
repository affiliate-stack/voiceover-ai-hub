# Prompt For Codex In The Target Repository

Use this prompt after copying the package into another website repository.

```text
Read the Wincher handoff docs in this repo:

- README.md
- docs/DEPLOYMENT.md
- docs/CREDENTIALS.md
- docs/WORKFLOW.md
- codex/GOAL.md

Deploy the read-only SEO API toolkit:

- Wincher under tools/seo/wincher
- Google Search Console and PageSpeed Insights under tools/seo/google

Do not expose credentials. Do not print WINCHER_API_TOKEN, Google API keys, OAuth tokens, refresh tokens, client secrets, or service account JSON. Do not commit .env, token files, credential JSON, or outputs.

First, check whether tools/seo/.env exists and contains WINCHER_API_TOKEN and WINCHER_WEBSITE_ID. If WINCHER_WEBSITE_ID is missing, run:

cd tools/seo/wincher
python3 wincher_connector.py --mode websites

Use the matching domain to identify WINCHER_WEBSITE_ID.

Then export Wincher data:

python3 wincher_export.py --mode all --website-id YOUR_WEBSITE_ID

Then configure Google Search Console and PageSpeed from tools/seo/.env:

GSC_SITE_URL=
GOOGLE_CLIENT_SECRETS_FILE=client_secret.json
GOOGLE_TOKEN_FILE=token.json
PAGESPEED_API_KEY=
PAGESPEED_URLS=

From tools/seo/google, verify and export:

python3 gsc_export.py --mode sites
python3 gsc_export.py --mode all
python3 pagespeed_export.py --strategy both

After export, analyze the Wincher, Search Console, and PageSpeed CSVs against the website source files. Identify:

- pages ranking near page 1
- ranking URL vs preferred URL mismatches
- keywords with volume but weak ranking
- Search Console queries with high impressions and low CTR
- Search Console page/query mismatches
- pages with weak average position but useful impressions
- PageSpeed/Lighthouse issues affecting important pages
- content gaps
- internal link opportunities
- title/meta/H1/H2 improvements

Before editing, provide a concise plan with file paths and expected SEO impact. If I say "execute", apply the fixes, validate them, and summarize exactly what changed.
```
