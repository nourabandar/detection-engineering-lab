"""Unit tests for detection definition validation."""
import unittest

from src.sync_rules import payload
from src.validate_rules import load_rules, validate_rule


class DetectionValidationTests(unittest.TestCase):
    def setUp(self):
        self.rule = {
            "rule_id": "test-rule",
            "name": "Test rule",
            "description": "A test",
            "language": "kuery",
            "query": "event.category : process",
            "index": ["logs-*"],
            "severity": "medium",
            "risk_score": 42,
            "tags": ["test"],
            "enabled": False,
        }

    def test_valid_rule(self):
        self.assertEqual(validate_rule(self.rule), [])

    def test_reject_invalid_risk_score(self):
        self.rule["risk_score"] = 101
        self.assertTrue(validate_rule(self.rule))

    def test_reject_empty_index(self):
        self.rule["index"] = []
        self.assertTrue(validate_rule(self.rule))

    def test_example_rules_parse(self):
        self.assertGreaterEqual(len(load_rules()), 1)

    def test_payload_defaults_disabled(self):
        self.assertFalse(payload(self.rule)["enabled"])


if __name__ == "__main__":
    unittest.main()
