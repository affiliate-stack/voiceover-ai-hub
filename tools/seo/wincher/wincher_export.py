import argparse
import csv
import os
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL.*")

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
TOOL_ROOT = BASE_DIR.parent
BASE_URL = "https://api.wincher.com/v1"
DEFAULT_OUTPUT_DIR = BASE_DIR / "outputs"

load_dotenv(TOOL_ROOT / ".env")
load_dotenv(BASE_DIR / ".env")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export read-only Wincher website and keyword data to CSV."
    )
    parser.add_argument(
        "--mode",
        choices=["websites", "keywords", "all"],
        default="all",
        help="Which Wincher data to export.",
    )
    parser.add_argument(
        "--website-id",
        default=os.environ.get("WINCHER_WEBSITE_ID", ""),
        help="Wincher website ID for keyword export. Required for keywords mode.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Folder where CSV exports should be written.",
    )
    parser.add_argument(
        "--include-ranking",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include ranking data in keyword exports.",
    )
    return parser.parse_args()


def get_headers():
    token = os.environ["WINCHER_API_TOKEN"]
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def request_page(endpoint, params):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=get_headers(),
        params=params,
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Wincher API error {response.status_code}: {response.text[:500]}"
        )
    return response.json()


def fetch_paginated(endpoint, params=None):
    limit = 100
    offset = 0
    rows = []
    params = dict(params or {})

    while True:
        payload = request_page(
            endpoint,
            {
                **params,
                "limit": limit,
                "offset": offset,
            },
        )
        data = payload.get("data", [])
        rows.extend(data)

        count = payload.get("count")
        offset += len(data)

        if not data:
            break
        if count is not None and offset >= count:
            break
        if len(data) < limit:
            break

    return rows


def metric_value(item, field):
    value = item.get(field)
    if isinstance(value, dict):
        return value.get("value")
    return value


def get_ranking(keyword):
    ranking = keyword.get("ranking")
    if not isinstance(ranking, dict):
        return {}
    return ranking


def get_ranking_position(keyword):
    position = get_ranking(keyword).get("position")
    if isinstance(position, dict):
        return position.get("value")
    return position


def get_ranking_change(keyword):
    position = get_ranking(keyword).get("position")
    if isinstance(position, dict):
        return position.get("change")
    return None


def get_ranking_url(keyword):
    pages = get_ranking(keyword).get("pages", [])
    if pages:
        return pages[0].get("url")
    return None


def get_ranking_page_position(keyword):
    pages = get_ranking(keyword).get("pages", [])
    if pages:
        return pages[0].get("position")
    return None


def get_groups(keyword):
    return ", ".join(
        group.get("name", "") for group in keyword.get("groups", []) if group.get("name")
    )


def get_search_intents(keyword):
    intents = keyword.get("search_intents") or []
    return ", ".join(
        f"{item.get('intent')}:{item.get('probability')}"
        for item in intents
        if item.get("intent")
    )


def fetch_websites():
    return fetch_paginated(
        "/websites",
        {
            "include_ranking": "false",
            "include_keyword_count_history": "false",
            "include_serp_features": "false",
        },
    )


def fetch_keywords(website_id, include_ranking=True):
    if not website_id:
        raise ValueError("A website ID is required for keyword export.")
    return fetch_paginated(
        f"/websites/{website_id}/keywords",
        {
            "include_ranking": str(include_ranking).lower(),
        },
    )


def export_websites(path, websites):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "website_id",
            "domain",
            "display_name",
            "keyword_count",
            "is_online",
            "search_engine_domain",
            "country",
            "language",
            "location_name",
            "created_at",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for website in websites:
            search_engine = website.get("search_engine") or {}
            location = website.get("location") or {}
            writer.writerow(
                {
                    "website_id": website.get("id"),
                    "domain": website.get("domain"),
                    "display_name": website.get("display_name"),
                    "keyword_count": website.get("keyword_count"),
                    "is_online": website.get("is_online"),
                    "search_engine_domain": search_engine.get("domain"),
                    "country": search_engine.get("country") or location.get("country"),
                    "language": website.get("language"),
                    "location_name": location.get("name"),
                    "created_at": website.get("created_at"),
                }
            )


def export_keywords(path, website_id, keywords):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "website_id",
            "keyword_id",
            "keyword",
            "ranking_position",
            "ranking_change",
            "ranking_url",
            "ranking_page_position",
            "preferred_url",
            "volume",
            "cpc",
            "competition",
            "groups",
            "search_intents",
            "ranking_updated_at",
            "created_at",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for keyword in keywords:
            writer.writerow(
                {
                    "website_id": website_id,
                    "keyword_id": keyword.get("id"),
                    "keyword": keyword.get("keyword"),
                    "ranking_position": get_ranking_position(keyword),
                    "ranking_change": get_ranking_change(keyword),
                    "ranking_url": get_ranking_url(keyword),
                    "ranking_page_position": get_ranking_page_position(keyword),
                    "preferred_url": keyword.get("preferred_url"),
                    "volume": metric_value(keyword, "volume"),
                    "cpc": metric_value(keyword, "cpc"),
                    "competition": metric_value(keyword, "competition"),
                    "groups": get_groups(keyword),
                    "search_intents": get_search_intents(keyword),
                    "ranking_updated_at": keyword.get("ranking_updated_at"),
                    "created_at": keyword.get("created_at"),
                }
            )


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.mode in {"websites", "all"}:
        websites = fetch_websites()
        websites_path = output_dir / "wincher_websites.csv"
        export_websites(websites_path, websites)
        print(f"Wrote {websites_path}: {len(websites)} rows")

    if args.mode in {"keywords", "all"}:
        website_id = args.website_id
        if not website_id and args.mode == "all":
            websites = locals().get("websites") or fetch_websites()
            if websites:
                website_id = str(websites[0].get("id") or "")
        keywords = fetch_keywords(website_id, include_ranking=args.include_ranking)
        keywords_path = output_dir / f"wincher_keywords_{website_id}.csv"
        export_keywords(keywords_path, website_id, keywords)
        print(f"Wrote {keywords_path}: {len(keywords)} rows")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("General error:")
        print(str(ex))
        raise SystemExit(1)
