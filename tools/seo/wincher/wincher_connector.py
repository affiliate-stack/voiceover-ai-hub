import argparse
import os
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL.*")

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
TOOL_ROOT = BASE_DIR.parent
BASE_URL = "https://api.wincher.com/v1"
DEFAULT_WEBSITE_ID = ""

load_dotenv(TOOL_ROOT / ".env")
load_dotenv(BASE_DIR / ".env")


def parse_args():
    parser = argparse.ArgumentParser(description="Read-only Wincher connector.")
    parser.add_argument(
        "--mode",
        choices=["websites", "keywords"],
        default="keywords",
        help="What to list.",
    )
    parser.add_argument(
        "--website-id",
        default=os.environ.get("WINCHER_WEBSITE_ID", DEFAULT_WEBSITE_ID),
        help="Wincher website ID for keyword listing.",
    )
    parser.add_argument(
        "--include-ranking",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include Wincher ranking data in keyword output.",
    )
    return parser.parse_args()


def get_headers():
    token = os.environ["WINCHER_API_TOKEN"]

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def metric_value(item, field):
    value = item.get(field)

    if isinstance(value, dict):
        return value.get("value")

    return value


def get_ranking_position(keyword):
    ranking = keyword.get("ranking")

    if not isinstance(ranking, dict):
        return None

    position = ranking.get("position")

    if isinstance(position, dict):
        return position.get("value")

    return position


def get_ranking_url(keyword):
    ranking = keyword.get("ranking")

    if not isinstance(ranking, dict):
        return None

    pages = ranking.get("pages", [])

    if pages:
        return pages[0].get("url")

    return None


def list_websites():
    url = f"{BASE_URL}/websites"

    response = requests.get(
        url,
        headers=get_headers(),
        params={
            "limit": 100,
            "offset": 0,
            "include_ranking": "false",
            "include_keyword_count_history": "false",
            "include_serp_features": "false",
        },
        timeout=30,
    )

    if response.status_code != 200:
        print("Wincher API error:")
        print(f"Status code: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    websites = data.get("data", [])

    if not websites:
        print("No websites found.")
        return

    for website in websites:
        print(
            website.get("id"),
            website.get("domain"),
            website.get("display_name"),
            "keywords:",
            website.get("keyword_count"),
            "online:",
            website.get("is_online"),
        )


def list_keywords(website_id, include_ranking=True):
    url = f"{BASE_URL}/websites/{website_id}/keywords"

    response = requests.get(
        url,
        headers=get_headers(),
        params={
            "limit": 100,
            "offset": 0,
            "include_ranking": str(include_ranking).lower(),
        },
        timeout=30,
    )

    if response.status_code != 200:
        print("Wincher API error:")
        print(f"Status code: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    keywords = data.get("data", [])

    if not keywords:
        print("No keywords found.")
        return

    for keyword in keywords:
        groups = ", ".join(group.get("name", "") for group in keyword.get("groups", []))

        print(
            keyword.get("id"),
            keyword.get("keyword"),
            "ranking:",
            get_ranking_position(keyword),
            "url:",
            get_ranking_url(keyword),
            "preferred_url:",
            keyword.get("preferred_url"),
            "volume:",
            metric_value(keyword, "volume"),
            "cpc:",
            metric_value(keyword, "cpc"),
            "competition:",
            metric_value(keyword, "competition"),
            "groups:",
            groups,
        )


if __name__ == "__main__":
    try:
        args = parse_args()

        if args.mode == "websites":
            list_websites()
        else:
            list_keywords(args.website_id, args.include_ranking)
    except Exception as ex:
        print("General error:")
        print(str(ex))
