# Future tools roadmap

## Current status — 12 July 2026

Phase 1's first release is now live: the English and Korean Script Timers let visitors select a 15, 30, 45, 60, or 90-second target, see a buffer-aware word budget, and learn how many words to add or remove from their current draft. The ElevenLabs Credit Calculator source note was also rechecked and clarified.

**Do not start another tool yet.** The next action is measurement, not development:

1. Request indexing for the updated English and Korean Script Timer URLs in Google Search Console after deployment.
2. On or after **9 August 2026** (28 days), record impressions, clicks, click-through rate, average position, landing-page queries, and any useful consented aggregate tool-use signal.
3. On or after **10 October 2026** (90 days), compare those results with the pre-release baseline and decide whether the timer needs the remaining Phase 1 refinements or whether to build one Phase 3 tool.
4. Keep sharing the Script Timer through relevant site navigation, helpful articles, and appropriate social/profile links. Do not use spammy link building or publish thin supporting pages.

The decision after measurement is simple:

- Queries about pronunciation, pauses, markup, or text-to-speech controls → build the **SSML Helper**.
- Queries about ads, explainers, video scripts, hooks, or examples → build the **Script Template Generator**.
- No meaningful search or usage signal yet → improve the Script Timer examples, copy, and internal linking before adding a new tool.

## Decision summary

This is a static, bilingual GitHub Pages site centred on an independent ElevenLabs guide. It already has two useful browser-only tools in English and Korean:

- Script Timer: `tools/script_length/script_length.html`
- ElevenLabs Character and Credit Calculator: `tools/character_cost/character_cost.html`

The next release should **refine and connect the existing tools**, not rebuild them. After that, publish only one new tool at a time and measure whether it earns search demand or helps visitors before adding the next one.

## What is already live

### Script Timer

The Script Timer already provides:

- A five-language calculation selector (English, French, Spanish, German, and Korean) with slow, normal, and fast pacing.
- Live word and character counts, estimated duration, 15/30/45/60/90-second slot guidance, a fixed 12% safety buffer, Copy summary, and local draft preferences.
- Dedicated English and Korean landing pages with canonical URLs and reciprocal language links.

The language selector changes the calculation. The English and Korean pages are still needed because they provide localised interface copy and search intent. Do not replace the two pages with one mixed-language URL.

### ElevenLabs Character and Credit Calculator

This is not a generic voice-over quote calculator. It estimates ElevenLabs text-to-speech characters, credits, audio minutes, and a plan fit using versioned public-plan assumptions. It already supports pasted text, monthly volume, safety buffer, regeneration multiplier, custom credit rates, a custom plan allowance, Copy summary, and local preferences.

Keep it focused on **ElevenLabs usage planning**. Do not turn it into a talent-rate or commercial-rights estimator unless the site later has reliable, region-specific pricing sources and a clear business reason to support quotes. Those are different user problems and should be separate tools, if built at all.

## Evidence and constraints

- The latest connected Search Console export showed that the English Script Timer generated most of the site's impressions but no clicks. Its first job is therefore stronger relevance, clearer snippets, and a more useful result—not a new collection of thin pages.
- The current public site and tools load quickly; PageSpeed is not the main growth constraint.
- GitHub Pages supports HTML, CSS, JavaScript, same-origin data files, and `localStorage`. It does not safely hold secret API keys, server-side user accounts, or a private database.
- Existing affiliate calls to action are already disclosed and marked `rel="sponsored"`. Future affiliate links must follow the same pattern.

Before any new phase begins, refresh the Search Console and PageSpeed exports; search demand and third-party prices change over time.

## Rules for every future tool

- Solve one specific visitor problem and return a useful result without sign-in.
- Keep essential explanatory text, examples, FAQs, and internal links in the HTML. JavaScript may power the interaction, but it should not be the only meaningful content on the page.
- Ship English and Korean equivalents together when the tool is intended for both audiences. Maintain canonical URLs, reciprocal `hreflang` links, navigation links, and sitemap entries.
- Explain calculation assumptions, units, source date, and uncertainty. Use estimates only where estimates are honest.
- Store text only in the visitor's browser. Never include user script text in a URL, analytics event, public repository, or third-party request.
- Provide labelled controls, keyboard access, focus states, `aria-live` feedback for changing results, copy/reset actions, and mobile testing.
- Load no analytics or third-party code before consent. Update the privacy page if a tool introduces any new storage or external request.
- Use structured data only for visible, accurate content. Do not add fake reviews, ratings, or site-search markup.
- Mark affiliate destinations clearly near the call to action and use `rel="sponsored noopener noreferrer"`.

## Delivery order and release gates

| Phase | Outcome | Build only when | Effort |
| --- | --- | --- | --- |
| 0 | Tool quality baseline and measurement | Always—this is part of each release | Small |
| 1 | Refine Script Timer | First target-duration release published 12 July 2026; measure before further changes | Small–medium |
| 2 | Maintain and clarify ElevenLabs Credit Calculator | Source assumptions reviewed 12 July 2026; recheck before any future number change | Small |
| 3 | One new static utility: SSML Helper **or** Script Template Generator | Phase 1 has been live long enough to collect data | Medium |
| 4 | Curated AI voice-tools directory | There is capacity to maintain vendor facts quarterly | Medium–large |
| 5 | Optional separate production-budget planner | Reliable sources and a defined audience exist | Medium–large |
| 6 | Secure AI, audio preview, accounts, or saving | Static tools prove demand and a secure backend is approved | Large |

Do not begin several new tools in parallel. Finish, test, publish, and measure one release before opening the next.

## Phase 0 — baseline for each release

### Required before publishing

- Check calculations at empty, normal, maximum, and unusual input values.
- Check English/Korean parity, mobile layout, keyboard navigation, Copy/Reset behaviour, and browser storage behaviour.
- Validate HTML, structured-data JSON, `sitemap.xml`, canonical URLs, and language links.
- Confirm the deployed page—not only the local file—shows the intended title, description, tool, and disclosure.
- Check that no personal script text is sent over the network.
- Add a contextual internal link from the homepage and from at least one related tool; do not rely on the sitemap alone for discovery.

### Measurement

Record a simple baseline before release, then review after 28 and 90 days:

- Impressions, clicks, click-through rate, and average position by landing page and query group in Search Console.
- Tool use only through consent-respecting, aggregated measurement if analytics consent exists; never record script content.
- PageSpeed and accessibility after functional changes.
- For affiliate pages, outbound click trends only after enough traffic exists to make the sample meaningful.

Use Search Console URL Inspection to request indexing manually after a meaningful deployment. Treat a sitemap as a discovery hint, not a guarantee of indexing.

## Phase 1 — refine the Script Timer

### Goal

Make the existing Script Timer more actionable for someone fitting a voice-over, advertisement, lesson, or video into a fixed duration.

### Do not rebuild

Keep the existing live calculation features: language and pace selectors, word count, duration, standard slot guide, 12% safety buffer, Copy, local draft preferences, and separate English/Korean pages.

### Proposed improvements

1. Add a target-duration mode for 15, 30, 45, 60, and 90 seconds. Show the visitor the approximate word or character budget for their selected language and pace, and the number to add or remove from the current draft.
2. Make the current fixed safety buffer more understandable. Either expose a simple choice such as no/light/natural pause allowance or keep the fixed value but explain it beside the result. Do not present it as a precise recording guarantee.
3. Add practical, visible examples for a 30-second ad, 60-second explainer, and 90-second introduction. These should use the same stated timing assumptions as the calculator.
4. Review the hard-coded pace values and Korean counting approach. Show a small “assumptions reviewed” date and keep the advice to make a final test recording.
5. Keep the interface focused. Do not add accounts, sharing links containing scripts, audio generation, or a large list of advanced controls.

### SEO support

- English focus: “script timer”, “script length calculator”, “script time”, and “word count to read time”.
- Korean focus: script length, narration pace, and characters-per-minute planning; do not claim a universally exact Korean read-time formula.
- Add links from both homepages and both credit calculators using natural, descriptive anchor text.

### Definition of done

The user can paste a script, select pace and target duration, understand whether it fits, see a safe planning estimate, copy the result, and use the equivalent English/Korean page without losing essential functionality.

## Phase 2 — maintain the ElevenLabs Credit Calculator

### Goal

Keep the existing calculator accurate, transparent, and clearly scoped to ElevenLabs usage planning.

### Required work

1. Recheck the displayed public plan allowances, credit assumptions, and source URL before changing the tool. Record the review date in the visible source note and in the code comment or data file.
2. Keep all plan values in one easy-to-review local data structure. Do not scrape the vendor’s pricing page in the visitor’s browser.
3. Preserve custom credit-rate and custom-plan inputs, because model and contract rules may differ from public plans.
4. Clarify that the result is a planning estimate, not a vendor quote, a guaranteed bill, or a comparison of every ElevenLabs model.
5. Add only small improvements that directly serve the existing task—such as a clearer “based on pasted text” summary or a link back to the Script Timer. Do not add commercial usage-rights multipliers here.

### Definition of done

All public numbers have a source and review date, users can override assumptions, and the wording never implies that the site controls ElevenLabs pricing.

## Phase 3 — choose one new static utility

Choose **one**, based on fresh Search Console queries, visitor feedback, and how much editorial maintenance is available. Do not build both at once.

### Option A: SSML Helper

Best if the site is attracting creators who already use text-to-speech tools and want better control over pronunciation or pacing.

- Source textarea and editable SSML output.
- Selection-based buttons for emphasis, pauses, prosody, `say-as`, and phoneme patterns.
- XML-aware escaping and validation; do not rely only on regular-expression highlighting.
- Copy, Reset, and local-only draft retention.
- Provider-neutral guidance that makes clear SSML support differs by vendor. Do not offer paid audio preview without a secure backend.

### Option B: Script Template Generator

Best if visitors need a quick voice-over starting point more than markup help.

- Use case, tone, language, target duration, and optional product/audience/call-to-action fields.
- Human-written template blocks assembled locally, not an external AI request.
- Editable output, Copy action, and a link into the Script Timer using a local handoff only—not a public URL containing the script.
- Output must be framed as a draft. Avoid claims, invented facts, and repetitive pages indexed as thin content.

### Definition of done

The chosen tool works offline after page load, keeps text local, has a clear visible explanation, and is linked from both language versions of the site.

## Phase 4 — curated AI voice-tools directory

### Goal

Build a genuinely helpful comparison resource, not a database-shaped affiliate page.

### Preconditions

- A named owner is willing to review entries and links at least quarterly.
- The initial list is intentionally small and has original editorial notes.
- Vendor facts, prices, and feature claims can be checked from primary sources on the review date.

### Recommended structure

- Make the directory page useful without JavaScript: render the initial cards and essential descriptions in HTML, then use JavaScript only to improve filtering.
- Use one local data source for optional filters and consistent facts.
- Start with fields such as `name`, `official_url`, `affiliate_url`, `languages`, `use_cases`, `pricing_model`, `free_tier`, `api`, `voice_cloning`, `ssml`, `commercial_use`, `last_reviewed`, and `editorial_notes`.
- Provide filters for language, use case, free plan, API, commercial use, cloning, and budget only after enough reviewed entries exist to make filters useful.
- Display a concise “best for”, key limitation, last-reviewed date, and disclosure next to each call to action.
- Use a plain official link where no affiliate relationship exists; use a labelled affiliate link and the required `rel` values where it does.

### What to avoid

- Auto-generated vendor summaries, unverified pricing claims, copied marketing copy, hundreds of empty filter combinations, and one thin indexable page per tool.
- Claiming “best” without defining the use case and the editorial basis.

### Definition of done

Every listing has original value, a verified destination, a current review date, a transparent relationship disclosure, and an understandable no-results state.

## Phase 5 — optional production-budget planner

This is separate from the ElevenLabs Credit Calculator and should be built only if visitors actually need it.

### Preconditions

- Define the audience and country or market scope.
- Use reliable, dated sources for every default cost assumption, or make all figures visitor-entered.
- Obtain a clear legal/editorial review of the disclaimer and terminology.

### Safe scope

If built, call it a **production-budget planner**, not a quote generator. Let visitors combine recording, editing, usage, revisions, language, and currency assumptions into a private local estimate. Clearly state it is not a binding quote or market-rate promise.

## Phase 6 — features requiring a secure backend

Commercial TTS preview, OpenAI-powered writing, user accounts, cross-device saved projects, private submissions, or any secret-key API require a serverless or hosted backend.

Do this only after the static tools show demand and a separate technical/privacy plan is approved. That plan must include:

- Server-side environment variables for keys.
- Authentication where needed, rate limits, budget limits, abuse protection, and monitoring.
- A privacy notice covering script text and audio, with a retention/deletion policy.
- No client-side exposure of paid API keys.

## Immediate next action

**Measure the published Script Timer release; do not build another tool before the 28-day review.**

At the review, decide whether to make the remaining Phase 1 refinements (clearer pause/buffer explanation and practical 30/60/90-second examples) or to select exactly one Phase 3 tool using the query signals above. The 90-day review is the checkpoint for a larger decision, not a deadline to add features.
