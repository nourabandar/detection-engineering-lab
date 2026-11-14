"""Print a local rule inventory; no network calls."""
from collections import Counter

from .validate_rules import load_rules


def main() -> None:
    rules = load_rules()
    counts = Counter(rule["severity"] for _, rule in rules)
    print(f"Detection rules: {len(rules)}")
    for severity in ("low", "medium", "high", "critical"):
        print(f"  {severity.title()}: {counts[severity]}")
    for path, rule in rules:
        print(f"- {rule['rule_id']} ({path.name})")


if __name__ == "__main__":
    main()
