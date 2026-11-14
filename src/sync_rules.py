"""Preview or create example rules using Elastic Security's Kibana API.

This demo only creates rules. It does not update existing rules or enable them.
"""
from __future__ import annotations

import argparse
import json
import os
from urllib import error, request
from urllib.parse import urlparse

from .validate_rules import load_rules


def payload(rule: dict) -> dict:
    """Convert a validated TOML definition into a Kibana query rule."""
    return {
        "rule_id": rule["rule_id"],
        "name": rule["name"],
        "description": rule["description"],
        "type": "query",
        "language": rule["language"],
        "query": rule["query"],
        "index": rule["index"],
        "severity": rule["severity"],
        "risk_score": rule["risk_score"],
        "tags": rule.get("tags", []),
        "interval": "5m",
        "from": "now-10m",
        "enabled": False,  # safe default for new lab rules
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview or create Elastic Security rules")
    parser.add_argument("--apply", action="store_true", help="Create rules in Kibana")
    args = parser.parse_args()
    rules = load_rules()
    if not args.apply:
        for _, rule in rules:
            print(json.dumps(payload(rule), indent=2))
        print("Preview only. Pass --apply to make API requests.")
        return

    url = os.environ.get("KIBANA_URL", "").rstrip("/")
    key = os.environ.get("KIBANA_API_KEY", "")
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc or not key:
        parser.error("--apply requires an HTTPS KIBANA_URL and KIBANA_API_KEY")

    for path, rule in rules:
        body = json.dumps(payload(rule)).encode("utf-8")
        req = request.Request(
            f"{url}/api/detection_engine/rules",
            data=body,
            headers={
                "Authorization": f"ApiKey {key}",
                "Content-Type": "application/json",
                "kbn-xsrf": "true",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=20) as response:
                print(f"Created {path.name}: HTTP {response.status}")
        except error.HTTPError as exc:
            detail = exc.read(300).decode("utf-8", errors="replace")
            raise SystemExit(f"Could not create {path.name}: HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise SystemExit(f"Could not connect to Kibana: {exc}") from exc


if __name__ == "__main__":
    main()
