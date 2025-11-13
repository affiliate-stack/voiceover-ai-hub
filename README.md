# voiceover-ai-hub
Static marketing site for showcasing AI text-to-speech and voiceover tools. Includes feature highlights, comparison sections, and affiliate call-to-actions. Not affiliated with or endorsed by any vendor. References to third-party products are for informational purposes only; trademarks belong to their owners.

## Privacy & consent

- `consent.js` blocks Google Analytics until a visitor opts in and keeps the decision in `localStorage` (`voaih-consent-v1`). Update the `GA_ID` constant in that file if a different property is used on another domain.
- Every page that should expose the consent controls needs the banner markup (`data-consent-banner` wrapper, buttons, and checkbox) plus at least one trigger element with `data-consent-open` so people can reopen their settings.
- `privacy.html` documents GDPR, LGPD, and CCPA notices. Duplicate or translate it per domain, and change the “Updated” date plus contact email to whatever inbox you monitor for privacy requests.
- To reuse this CMP on additional GitHub Pages sites, copy `consent.js`, reference it with `<script defer src="/consent.js"></script>`, drop in the banner + footer link, and point the privacy link to the correct path for that site. The consent logic is self-contained and does not rely on any build tools.
