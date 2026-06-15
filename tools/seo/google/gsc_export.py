import argparse
import csv
import os
import warnings
from datetime import date, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TOOL_ROOT = BASE_DIR.parent
DEFAULT_OUTPUT_DIR = BASE_DIR / "outputs"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL.*")
warnings.filterwarnings(
    "ignore",
    message="You are using a Python version 3.9 past its end of life.*",
    category=FutureWarning,
)
warnings.filterwarnings(
    "ignore",
    message="You are using a non-supported Python version.*",
    category=FutureWarning,
)


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


def default_dates():
    # Search Console dates are reported in Pacific Time and recent data can be incomplete.
    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=27)
    return start.isoformat(), end.isoformat()


def parse_dimensions(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_args():
    start_date, end_date = default_dates()
    parser = argparse.ArgumentParser(
        description="Export read-only Google Search Console data to CSV."
    )
    parser.add_argument(
        "--mode",
        choices=["sites", "sitemaps", "search-analytics", "all"],
        default="search-analytics",
        help="Which Search Console data to export.",
    )
    parser.add_argument(
        "--site-url",
        default=os.environ.get("GSC_SITE_URL", ""),
        help="Search Console property URL, for example https://example.com/ or sc-domain:example.com.",
    )
    parser.add_argument(
        "--start-date",
        default=start_date,
        help="Start date in YYYY-MM-DD. Defaults to 28 finalized-ish days.",
    )
    parser.add_argument(
        "--end-date",
        default=end_date,
        help="End date in YYYY-MM-DD. Defaults to three days ago.",
    )
    parser.add_argument(
        "--dimensions",
        default="query,page",
        help="Comma-separated Search Analytics dimensions, for example query,page,date,device,country.",
    )
    parser.add_argument(
        "--search-type",
        default="web",
        choices=["web", "image", "video", "news", "discover", "googleNews"],
        help="Search Console result type.",
    )
    parser.add_argument(
        "--row-limit",
        type=int,
        default=25000,
        help="Rows per API request. Search Console max is 25000.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Folder where CSV exports should be written.",
    )
    parser.add_argument(
        "--auth-mode",
        choices=["auto", "oauth", "service-account", "bearer-token"],
        default="auto",
        help="Use OAuth desktop/client secrets, a service account, or a temporary bearer token.",
    )
    return parser.parse_args()


def resolve_local_path(value):
    if not value:
        return None
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    return path


def build_service(auth_mode="auto"):
    try:
        from google.auth.credentials import Credentials as BaseCredentials
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google.oauth2 import service_account
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as ex:
        raise RuntimeError(
            "Missing Google API dependencies. Run: python3 -m pip install -r requirements.txt"
        ) from ex

    service_account_file = resolve_local_path(os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", ""))
    client_secrets_file = resolve_local_path(
        os.environ.get("GOOGLE_CLIENT_SECRETS_FILE", "client_secret.json")
    )
    token_file = resolve_local_path(os.environ.get("GOOGLE_TOKEN_FILE", "token.json"))
    access_token = os.environ.get("GOOGLE_ACCESS_TOKEN", "").strip()

    if auth_mode == "bearer-token" or (auth_mode == "auto" and access_token):
        if not access_token:
            raise ValueError("GOOGLE_ACCESS_TOKEN is required for bearer-token auth.")

        class StaticBearerCredentials(BaseCredentials):
            def __init__(self, token):
                super().__init__()
                self.token = token

            def refresh(self, request):
                return None

        credentials = StaticBearerCredentials(access_token)
        return build("searchconsole", "v1", credentials=credentials)

    use_service_account = auth_mode == "service-account" or (
        auth_mode == "auto" and service_account_file and service_account_file.exists()
    )

    if use_service_account:
        if not service_account_file or not service_account_file.exists():
            raise FileNotFoundError("GOOGLE_SERVICE_ACCOUNT_FILE was not found.")
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=SCOPES,
        )
    else:
        credentials = None
        if token_file and token_file.exists():
            credentials = Credentials.from_authorized_user_file(token_file, SCOPES)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if not client_secrets_file or not client_secrets_file.exists():
                    raise FileNotFoundError(
                        "GOOGLE_CLIENT_SECRETS_FILE was not found. Download OAuth client credentials and save them locally."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file,
                    SCOPES,
                )
                credentials = flow.run_local_server(port=0)

            if token_file:
                token_file.write_text(credentials.to_json(), encoding="utf-8")

    return build("searchconsole", "v1", credentials=credentials)


def safe_filename(value):
    keep = []
    for char in value:
        if char.isalnum() or char in ("-", "_", "."):
            keep.append(char)
        else:
            keep.append("_")
    return "".join(keep).strip("_") or "site"


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_sites(service, output_dir):
    payload = service.sites().list().execute()
    entries = payload.get("siteEntry", [])
    rows = [
        {
            "site_url": entry.get("siteUrl"),
            "permission_level": entry.get("permissionLevel"),
        }
        for entry in entries
    ]
    path = output_dir / "gsc_sites.csv"
    write_csv(path, ["site_url", "permission_level"], rows)
    print(f"Wrote {path}: {len(rows)} rows")
    return rows


def export_sitemaps(service, site_url, output_dir):
    if not site_url:
        raise ValueError("A Search Console site URL is required for sitemap export.")

    payload = service.sitemaps().list(siteUrl=site_url).execute()
    entries = payload.get("sitemap", [])
    rows = [
        {
            "site_url": site_url,
            "path": entry.get("path"),
            "last_submitted": entry.get("lastSubmitted"),
            "is_pending": entry.get("isPending"),
            "is_sitemaps_index": entry.get("isSitemapsIndex"),
            "type": entry.get("type"),
            "last_downloaded": entry.get("lastDownloaded"),
            "warnings": entry.get("warnings"),
            "errors": entry.get("errors"),
            "contents": "; ".join(
                f"{item.get('type')} submitted={item.get('submitted')} indexed={item.get('indexed')}"
                for item in entry.get("contents", [])
            ),
        }
        for entry in entries
    ]
    path = output_dir / f"gsc_sitemaps_{safe_filename(site_url)}.csv"
    write_csv(
        path,
        [
            "site_url",
            "path",
            "last_submitted",
            "is_pending",
            "is_sitemaps_index",
            "type",
            "last_downloaded",
            "warnings",
            "errors",
            "contents",
        ],
        rows,
    )
    print(f"Wrote {path}: {len(rows)} rows")
    return rows


def fetch_search_analytics(
    service,
    site_url,
    start_date,
    end_date,
    dimensions,
    search_type,
    row_limit,
):
    if not site_url:
        raise ValueError("A Search Console site URL is required for Search Analytics export.")
    if row_limit < 1 or row_limit > 25000:
        raise ValueError("--row-limit must be between 1 and 25000.")

    rows = []
    start_row = 0
    while True:
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "type": search_type,
            "rowLimit": row_limit,
            "startRow": start_row,
            "dataState": "final",
        }
        payload = (
            service.searchanalytics()
            .query(siteUrl=site_url, body=body)
            .execute()
        )
        batch = payload.get("rows", [])
        rows.extend(batch)
        if len(batch) < row_limit:
            break
        start_row += len(batch)

    return rows


def export_search_analytics(
    service,
    site_url,
    start_date,
    end_date,
    dimensions,
    search_type,
    row_limit,
    output_dir,
):
    api_rows = fetch_search_analytics(
        service,
        site_url,
        start_date,
        end_date,
        dimensions,
        search_type,
        row_limit,
    )

    rows = []
    for item in api_rows:
        keys = item.get("keys", [])
        row = {
            "site_url": site_url,
            "start_date": start_date,
            "end_date": end_date,
            "search_type": search_type,
            "clicks": item.get("clicks"),
            "impressions": item.get("impressions"),
            "ctr": item.get("ctr"),
            "position": item.get("position"),
        }
        for index, dimension in enumerate(dimensions):
            row[dimension] = keys[index] if index < len(keys) else ""
        rows.append(row)

    fieldnames = [
        "site_url",
        "start_date",
        "end_date",
        "search_type",
        *dimensions,
        "clicks",
        "impressions",
        "ctr",
        "position",
    ]
    dimension_part = "_".join(dimensions) or "summary"
    path = output_dir / (
        f"gsc_search_analytics_{safe_filename(site_url)}_"
        f"{dimension_part}_{start_date}_to_{end_date}.csv"
    )
    write_csv(path, fieldnames, rows)
    print(f"Wrote {path}: {len(rows)} rows")
    return rows


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    dimensions = parse_dimensions(args.dimensions)
    service = build_service(auth_mode=args.auth_mode)

    if args.mode in {"sites", "all"}:
        export_sites(service, output_dir)

    if args.mode in {"sitemaps", "all"}:
        export_sitemaps(service, args.site_url, output_dir)

    if args.mode in {"search-analytics", "all"}:
        export_search_analytics(
            service,
            args.site_url,
            args.start_date,
            args.end_date,
            dimensions,
            args.search_type,
            args.row_limit,
            output_dir,
        )


def explain_error(ex):
    status = getattr(getattr(ex, "resp", None), "status", None)
    if status == 401:
        return (
            "Google returned 401 Invalid Credentials. For --auth-mode bearer-token, "
            "GOOGLE_ACCESS_TOKEN must be a current OAuth 2 access token with Search Console access. "
            "API keys, ID tokens, expired access tokens, and refresh tokens by themselves will not work."
        )
    if status == 403:
        return (
            "Google returned 403 Forbidden. The credential was accepted, but it does not have "
            "Search Console API permission or access to this Search Console property."
        )
    return str(ex)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("General error:")
        print(explain_error(ex))
        raise SystemExit(1)
