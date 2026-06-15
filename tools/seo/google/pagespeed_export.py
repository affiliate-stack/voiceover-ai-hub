import argparse
import csv
import json
import os
import warnings
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit, urlunsplit

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL.*")

import requests


BASE_DIR = Path(__file__).resolve().parent
TOOL_ROOT = BASE_DIR.parent
DEFAULT_OUTPUT_DIR = BASE_DIR / "outputs"
BASE_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
DEFAULT_CATEGORIES = ["performance", "accessibility", "best-practices", "seo"]


def load_local_env(path):
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_local_env(TOOL_ROOT / ".env")
load_local_env(BASE_DIR / ".env")


def parse_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export read-only PageSpeed Insights data for public URLs."
    )
    parser.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="URL to analyze. Can be passed multiple times. Defaults to PAGESPEED_URLS.",
    )
    parser.add_argument(
        "--strategy",
        choices=["mobile", "desktop", "both"],
        default="both",
        help="PageSpeed strategy to run.",
    )
    parser.add_argument(
        "--category",
        action="append",
        dest="categories",
        choices=DEFAULT_CATEGORIES,
        help="Lighthouse category to request. Can be passed multiple times.",
    )
    parser.add_argument(
        "--locale",
        default="ko",
        help="Locale for PageSpeed formatted strings.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Folder where exports should be written.",
    )
    parser.add_argument(
        "--save-json",
        action="store_true",
        help="Also save compact raw JSON responses for deeper analysis.",
    )
    return parser.parse_args()


def safe_filename(value):
    keep = []
    for char in value:
        if char.isalnum() or char in ("-", "_", "."):
            keep.append(char)
        else:
            keep.append("_")
    return "".join(keep).strip("_") or "url"


def get_urls(args):
    if args.urls:
        return args.urls
    return parse_csv(os.environ.get("PAGESPEED_URLS", ""))


def get_strategies(value):
    return ["mobile", "desktop"] if value == "both" else [value]


def request_pagespeed(url, strategy, categories, locale):
    request_target = normalize_url_for_api(url)
    params = {
        "url": request_target,
        "strategy": strategy,
        "locale": locale,
        "utm_source": "local-seo-export",
        "utm_campaign": "google-website-seo",
    }
    api_key = os.environ.get("PAGESPEED_API_KEY", "").strip()
    if api_key:
        params["key"] = api_key

    request_url = f"{BASE_URL}?{urlencode(params)}"
    for category in categories:
        request_url += f"&category={category}"

    response = requests.get(request_url, timeout=120)
    if response.status_code != 200:
        if response.status_code == 429 and not api_key:
            raise RuntimeError(
                "PageSpeed unauthenticated quota exceeded. Add PAGESPEED_API_KEY to .env and rerun."
            )
        if response.status_code == 429:
            raise RuntimeError(
                "PageSpeed quota exceeded for the configured API key/project."
            )
        raise RuntimeError(
            f"PageSpeed API error {response.status_code}: {response.text[:500]}"
        )
    return response.json()


def normalize_url_for_api(url):
    parsed = urlsplit(url)
    if not parsed.scheme or not parsed.netloc:
        return url

    hostname = parsed.hostname.encode("idna").decode("ascii") if parsed.hostname else ""
    netloc = hostname
    if parsed.port:
        netloc = f"{netloc}:{parsed.port}"
    if parsed.username:
        userinfo = parsed.username
        if parsed.password:
            userinfo = f"{userinfo}:{parsed.password}"
        netloc = f"{userinfo}@{netloc}"

    path = quote(parsed.path or "/", safe="/%")
    query = quote(parsed.query, safe="=&%?/:,+")
    fragment = quote(parsed.fragment, safe="=&%?/:,+")
    return urlunsplit((parsed.scheme, netloc, path, query, fragment))


def score_to_int(score):
    if score is None:
        return ""
    return round(float(score) * 100)


def get_audit(lighthouse, audit_id):
    audits = lighthouse.get("audits", {})
    audit = audits.get(audit_id) or {}
    return audit.get("displayValue", "")


def summarize_response(url, strategy, payload):
    lighthouse = payload.get("lighthouseResult", {})
    categories = lighthouse.get("categories", {})
    audits = lighthouse.get("audits", {})
    runtime_error = lighthouse.get("runtimeError") or {}

    opportunity_items = []
    for audit_id, audit in audits.items():
        details = audit.get("details") or {}
        savings = details.get("overallSavingsMs")
        score = audit.get("score")
        if savings and score is not None and score < 1:
            opportunity_items.append(
                {
                    "id": audit_id,
                    "title": audit.get("title", audit_id),
                    "savings_ms": round(float(savings)),
                    "score": score,
                }
            )
    opportunity_items.sort(key=lambda item: item["savings_ms"], reverse=True)

    top_opportunities = " | ".join(
        f"{item['title']} ({item['savings_ms']} ms)"
        for item in opportunity_items[:5]
    )

    return {
        "url": url,
        "strategy": strategy,
        "final_url": lighthouse.get("finalUrl"),
        "fetch_time": lighthouse.get("fetchTime"),
        "analysis_utc_timestamp": payload.get("analysisUTCTimestamp"),
        "performance": score_to_int((categories.get("performance") or {}).get("score")),
        "accessibility": score_to_int((categories.get("accessibility") or {}).get("score")),
        "best_practices": score_to_int((categories.get("best-practices") or {}).get("score")),
        "seo": score_to_int((categories.get("seo") or {}).get("score")),
        "first_contentful_paint": get_audit(lighthouse, "first-contentful-paint"),
        "largest_contentful_paint": get_audit(lighthouse, "largest-contentful-paint"),
        "total_blocking_time": get_audit(lighthouse, "total-blocking-time"),
        "cumulative_layout_shift": get_audit(lighthouse, "cumulative-layout-shift"),
        "speed_index": get_audit(lighthouse, "speed-index"),
        "interactive": get_audit(lighthouse, "interactive"),
        "runtime_error_code": runtime_error.get("code", ""),
        "runtime_error_message": runtime_error.get("message", ""),
        "top_opportunities": top_opportunities,
    }


def write_csv(path, rows):
    fieldnames = [
        "url",
        "strategy",
        "final_url",
        "fetch_time",
        "analysis_utc_timestamp",
        "performance",
        "accessibility",
        "best_practices",
        "seo",
        "first_contentful_paint",
        "largest_contentful_paint",
        "total_blocking_time",
        "cumulative_layout_shift",
        "speed_index",
        "interactive",
        "runtime_error_code",
        "runtime_error_message",
        "top_opportunities",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    args = parse_args()
    urls = get_urls(args)
    if not urls:
        raise ValueError("Provide --url or set PAGESPEED_URLS in .env.")

    categories = args.categories or DEFAULT_CATEGORIES
    strategies = get_strategies(args.strategy)
    output_dir = Path(args.output_dir)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rows = []

    for url in urls:
        for strategy in strategies:
            payload = request_pagespeed(url, strategy, categories, args.locale)
            rows.append(summarize_response(url, strategy, payload))

            if args.save_json:
                json_path = (
                    output_dir
                    / "raw"
                    / f"pagespeed_{safe_filename(url)}_{strategy}_{timestamp}.json"
                )
                json_path.parent.mkdir(parents=True, exist_ok=True)
                json_path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

    csv_path = output_dir / f"pagespeed_summary_{timestamp}.csv"
    write_csv(csv_path, rows)
    print(f"Wrote {csv_path}: {len(rows)} rows")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("General error:")
        print(str(ex))
        raise SystemExit(1)
