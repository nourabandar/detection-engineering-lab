# Detection Engineering Lab

A hands-on detection engineering lab with structured detection rules, local validation, and optional rule synchronization to Elastic Security.


## Overview

- Define example detection rules in `detections/*.toml`
- Validate their required fields with Python
- Preview or synchronize detection rules with Elastic Security through the Kibana API
- Review a simple local rule inventory
- Run checks automatically with GitHub Actions

## Project layout

```text
detections/                  Example TOML rules
src/validate_rules.py        Validate local detection definitions
src/sync_rules.py            Preview or publish rules to Elastic
src/report.py                Print local detection inventory
tests/                       Unit tests for validation
.github/workflows/           CI validation
```

## Quick start

Requires **Python 3.11+**.

```bash
python -m pip install -r requirements.txt
python -m src.validate_rules
python -m src.report
python -m src.sync_rules                      # preview only
python -m unittest discover -s tests
```

## Optional Elastic Security synchronization

Configure environment variables from `.env.example` **in your shell or your local, untracked `.env`**. The scripts do not automatically read `.env`.

```bash
export KIBANA_URL="https://your-kibana.example"
export KIBANA_API_KEY="YOUR_API_KEY"
python -m src.sync_rules --apply
```

The sync command defaults to a preview. It only writes to Elastic when you pass `--apply`, and the example rule is disabled upon initial creation. Review detection queries and permissions before applying them. The rule must be enabled separately when ready for monitoring.

## Safety and limitations

- Uses sample detection definitions; not validated against a real SIEM in this repository.
- Do not commit API keys, production logs, private network details, or sensitive information.
- The script is a starting point. Elastic deployments may have different API compatibility or rule requirements.

## Attribution

Reference implementation and inspiration: [isherwood-sec/detection-engineering](https://github.com/isherwood-sec/detection-engineering) by **isherwood-sec**.

## Status

Reconstructed starter implementation; not yet claimed to be deployed or tested against a production Elastic instance.
