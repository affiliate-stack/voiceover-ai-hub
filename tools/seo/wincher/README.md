# Wincher Website SEO Connector

This folder contains a read-only Wincher API connector for a website repository.

## Setup

Install dependencies from this folder:

```bash
python3 -m pip install -r requirements.txt
```

Create a shared credentials file in the target repo:

```text
tools/seo/.env
```

Required values:

```text
WINCHER_API_TOKEN=
WINCHER_WEBSITE_ID=
```

The scripts also read `tools/seo/wincher/.env` as a fallback for connector-specific setups.

## Commands

List websites:

```bash
python3 wincher_connector.py --mode websites
```

List keywords for one website:

```bash
python3 wincher_connector.py --mode keywords --website-id YOUR_WEBSITE_ID
```

Export websites and keywords to CSV:

```bash
python3 wincher_export.py --mode all --website-id YOUR_WEBSITE_ID
```

Export only keywords:

```bash
python3 wincher_export.py --mode keywords --website-id YOUR_WEBSITE_ID
```

## Outputs

CSV files are written to:

```text
tools/seo/wincher/outputs/
```

Typical files:

```text
wincher_websites.csv
wincher_keywords_YOUR_WEBSITE_ID.csv
```

## Safety

- Do not print or expose `WINCHER_API_TOKEN`.
- Do not commit `.env`.
- Do not commit `outputs/` unless the target repo intentionally stores SEO snapshots.
- API usage is read-only.
