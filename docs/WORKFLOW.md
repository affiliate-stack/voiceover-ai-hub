# SEO API Workflow

This workflow is designed for a static site or website repository where Codex can read and edit files.

## Goal

Use Wincher, Google Search Console, and PageSpeed Insights data to identify practical SEO fixes in the website:

- pages ranking near page 1
- ranking URL mismatches
- missing or weak preferred URLs
- keywords with search volume but weak ranking
- content gaps
- titles and meta descriptions that do not match ranking opportunities
- internal-link opportunities
- Search Console impressions/clicks/CTR gaps
- PageSpeed and Lighthouse issues

## Step 1. Export API Data

Wincher:

```bash
cd tools/seo/wincher
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

## Step 2. Inspect CSVs

Wincher:

```text
outputs/wincher_keywords_YOUR_WEBSITE_ID.csv
```

Important columns:

- `keyword`
- `ranking_position`
- `ranking_change`
- `ranking_url`
- `ranking_page_position`
- `preferred_url`
- `volume`
- `competition`
- `groups`
- `search_intents`

Search Console:

```text
tools/seo/google/outputs/gsc_search_analytics_*.csv
```

Important columns:

- query
- page
- clicks
- impressions
- ctr
- position

PageSpeed:

```text
tools/seo/google/outputs/pagespeed_summary_*.csv
```

Important columns:

- performance
- accessibility
- best_practices
- seo
- largest_contentful_paint
- total_blocking_time
- cumulative_layout_shift
- top_opportunities

## Step 3. Prioritize Fixes

Highest priority:

1. Keywords ranking positions 4-20 with clear page intent.
2. Keywords where `ranking_url` does not match `preferred_url`.
3. Search Console queries with high impressions and low CTR.
4. Pages with useful impressions but weak average position.
5. Keywords with volume but no clear landing page.
6. Pages ranking for several related terms but missing a focused heading/section.
7. Pages with weak title/meta compared with the ranking keyword.
8. Pages with PageSpeed issues that affect Core Web Vitals.

## Step 4. Map Keywords To Pages

For each target keyword, decide:

- which page should rank
- whether the current ranking URL is correct
- what search intent the page should satisfy
- what on-page content is missing
- what internal links should point to it
- whether Search Console confirms real impressions
- whether PageSpeed issues could block performance

## Step 5. Propose Changes Before Editing

For each change, list:

- file path
- current issue
- proposed edit
- expected SEO reason
- risk level
- source signal, for example Wincher, Search Console, or PageSpeed

If the user asks to execute fixes, edit the files after this review.

## Step 6. Implement Carefully

Good first fixes:

- improve `title` and meta description
- add a concise FAQ section
- add one useful section that answers the ranking keyword
- add internal links from related pages
- fix canonical or sitemap mismatches
- align H1/H2 with real user intent
- improve CTR by matching title/meta to confirmed queries
- fix obvious LCP/CLS/TBT issues reported by PageSpeed

Avoid:

- keyword stuffing
- changing brand/offer facts
- creating pages that cannot be maintained
- overwriting user content without review
- optimizing for a keyword that neither Wincher nor Search Console supports

## Step 7. Verify

After edits:

```bash
git diff --check
```

Also verify:

- one H1 per page
- internal links resolve
- JSON-LD parses if changed
- sitemap/robots stay valid if changed
- no credentials were printed or committed
