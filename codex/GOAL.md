# Codex Goal

Deploy and use the SEO API toolkit in this website repository without exposing credentials.

## Objective

1. Install the read-only Wincher connector under `tools/seo/wincher`.
2. Install the read-only Google Search Console and PageSpeed connectors under `tools/seo/google`.
3. Configure local credentials in `tools/seo/.env`.
4. Find the correct `WINCHER_WEBSITE_ID` if the user does not know it.
5. Confirm the correct `GSC_SITE_URL`.
6. Export Wincher website and keyword data to CSV.
7. Export Google Search Console data to CSV.
8. Run PageSpeed Insights and export summaries to CSV.
9. Analyze the combined API data against the website source files.
10. Propose high-impact SEO fixes.
11. Implement fixes only after the user asks to execute them.
12. Verify edits with local checks.

## Constraints

- Never print or expose `WINCHER_API_TOKEN`.
- Never print or expose Google API keys, OAuth tokens, refresh tokens, client secrets, or service account JSON.
- Never commit `.env`, credential JSON, token JSON, or output CSVs unless explicitly requested.
- Keep API usage read-only.
- Keep website edits scoped and reviewable.
- Prefer existing site structure and style.

## Definition Of Done

- Wincher scripts run successfully.
- Google scripts run successfully.
- `WINCHER_WEBSITE_ID` is known and stored locally.
- `GSC_SITE_URL` is known and stored locally.
- CSV exports exist in `tools/seo/wincher/outputs/` and `tools/seo/google/outputs/`.
- SEO opportunities are summarized with page-level recommendations.
- Any implemented changes pass validation.
