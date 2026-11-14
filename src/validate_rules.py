"""Validate example detection-rule TOML files. Python 3.11+."""
from __future__ import annotations

from pathlib import Path
import tomllib

RULES_DIR = Path(__file__).resolve().parent.parent / "detections"
REQUIRED_TEXT = ("rule_id", "name", "description", "language", "query", "severity")
SEVERITIES = {"low", "medium", "high", "critical"}


def validate_rule(rule: dict) -> list[str]:
    """Return human-readable validation errors; never mutate input."""
    errors = []
    for field in REQUIRED_TEXT:
        if not isinstance(rule.get(field), str) or not rule[field].strip():
            errors.append(f"{field} must be a nonempty string")
    if rule.get("severity") not in SEVERITIES:
        errors.append("severity must be low, medium, high, or critical")
    score = rule.get("risk_score")
    if type(score) is not int or not 0 <= score <= 100:
        errors.append("risk_score must be an integer from 0 to 100")
    indexes = rule.get("index")
    if not isinstance(indexes, list) or not indexes or not all(
        isinstance(x, str) and x.strip() for x in indexes
    ):
        errors.append("index must be a nonempty list of nonempty strings")
    tags = rule.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(x, str) for x in tags):
        errors.append("tags must be a list of strings")
    if type(rule.get("enabled", False)) is not bool:
        errors.append("enabled must be a boolean")
    if rule.get("language") not in {"kuery", "lucene"}:
        errors.append("language must be kuery or lucene")
    return errors


def load_rules(directory: Path = RULES_DIR) -> list[tuple[Path, dict]]:
    """Load valid TOML detection definitions, raising on errors."""
    rules = []
    seen = set()
    paths = sorted(directory.glob("*.toml"))
    if not paths:
        raise ValueError(f"No TOML rule files found in {directory}")
    for path in paths:
        try:
            with path.open("rb") as handle:
                rule = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise ValueError(f"{path.name}: invalid TOML: {exc}") from exc
        errors = validate_rule(rule)
        if errors:
            raise ValueError(f"{path.name}: " + "; ".join(errors))
        if rule["rule_id"] in seen:
            raise ValueError(f"{path.name}: duplicate rule_id {rule['rule_id']}")
        seen.add(rule["rule_id"])
        rules.append((path, rule))
    return rules


def main() -> None:
    rules = load_rules()
    print(f"Validated {len(rules)} rule(s):")
    for path, rule in rules:
        print(f"  - {path.name}: {rule['name']}")


if __name__ == "__main__":
    main()
