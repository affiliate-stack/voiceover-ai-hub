# API Reference Used By This Package

## Wincher

Base URL:

```text
https://api.wincher.com/v1
```

Authentication:

```text
Authorization: Bearer WINCHER_API_TOKEN
Accept: application/json
```

## Endpoints Used

List websites:

```text
GET /websites
```

Parameters used:

```text
limit=100
offset=0
include_ranking=false
include_keyword_count_history=false
include_serp_features=false
```

List keywords for one website:

```text
GET /websites/{website_id}/keywords
```

Parameters used:

```text
limit=100
offset=0
include_ranking=true
```

Pagination:

- The exporter requests pages with `limit=100`.
- It increments `offset` until no rows remain, the API `count` is reached, or fewer than `limit` rows are returned.

## Exported Keyword Fields

The keyword CSV includes:

- website ID
- keyword ID
- keyword
- ranking position
- ranking change
- ranking URL
- ranking page position
- preferred URL
- volume
- CPC
- competition
- groups
- search intents
- ranking updated date
- created date

## Read-Only Scope

This package only sends `GET` requests. It does not create, update, or delete Wincher data.

## Google Search Console

Service:

```text
searchconsole v1
```

Scope:

```text
https://www.googleapis.com/auth/webmasters.readonly
```

Read methods used:

```text
sites.list
sitemaps.list
searchanalytics.query
```

Search Analytics request fields:

- `startDate`
- `endDate`
- `dimensions`
- `type`
- `rowLimit`
- `startRow`
- `dataState=final`

The exporter paginates Search Analytics with `startRow` until fewer than `rowLimit` rows are returned.

## PageSpeed Insights

Endpoint:

```text
GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed
```

Parameters used:

- `url`
- `strategy`
- `locale`
- `category`
- `key`, if `PAGESPEED_API_KEY` is configured
- `utm_source=local-seo-export`
- `utm_campaign=google-website-seo`

Categories requested by default:

- performance
- accessibility
- best-practices
- seo

The exporter summarizes:

- performance score
- accessibility score
- best practices score
- SEO score
- FCP
- LCP
- TBT
- CLS
- speed index
- interactive
- top opportunities

## Read-Only Scope

All included tools are read-only. Wincher and PageSpeed use GET requests. Search Console uses read-only OAuth scope.
