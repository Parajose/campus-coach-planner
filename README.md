# Campus Coach Planner

**Turn student demand into a practical trip plan.**

Estimate coaches, seat occupancy, route costs and break-even demand for vacation travel. Start with fictional Essikado–Accra and Essikado–Kumasi scenarios.

Built by [Joseph Tetteh (TJay)](https://github.com/Parajose) · Python + vanilla HTML/CSS/JavaScript · MIT license

## Run in under a minute

Requires **Python 3.10+**. There are **no third-party dependencies**.

```bash
git clone https://github.com/Parajose/campus-coach-planner.git
cd campus-coach-planner
python app.py
```

On Windows, use `py app.py` if `python` is unavailable. Open **http://127.0.0.1:8000**. Run one project at a time because all use port 8000. Stop with Ctrl+C. Open through the server, not by double-clicking `index.html`.

The sample runs automatically. Edit the JSON and click **Analyse scenario**, or use **Reset sample**. Each result table has a CSV export. Invalid input clears old results and explains the error.

## Features

- Responsive dashboard with sample data and interactive scenario inputs
- Transparent calculations in a separate, testable Python module
- CSV exports and readable input validation
- Local HTTP API with no required account or external service
- Automated numerical and edge-case checks using standard-library unittest

## Planning rules

For each independent route:

- Coaches = ceil(students / capacity).
- Revenue = students × fare.
- Cost = (coaches × coach cost + other cost) × (1 + contingency / 100).
- Other cost is charged once per active route. Zero students means zero coaches and zero cost.
- Break-even students = ceil(full planned cost / fare). A zero fare with positive cost has no finite break-even.
- Seat allocations fill each coach in order without exceeding capacity. No individual passenger identities are assigned.

The dashboard exports route summaries and coach allocations separately. A break-even flag shows whether the calculated demand fits the currently planned seats; increasing demand can require another coach and a fresh calculation.

## Scope and demo data

All sample fares and coach costs are **fictional**; they are not STC or other operator quotes. The app does not reserve buses, sell tickets, collect money or integrate with transport operators. It assumes dedicated coaches per route and does not optimise multi-stop routing, departure times or shared fleets. Monetary results are planning estimates rounded to two decimals, not accounting-grade settlement figures.

## Roadmap

Add operator quote comparison, passenger manifests with consent, departure scheduling and a properly authenticated booking system as separate features. Obtain real operator costs before making business decisions.

## Project layout

| File | Purpose |
| --- | --- |
| `app.py` | Local HTTP server and JSON API |
| `core.py` | Validation and domain calculations |
| `index.html` | Responsive interface and safe DOM rendering |
| `sample.json` | Reproducible fictional sample |
| `test_core.py` | Calculation and validation tests |
| `LICENSE` | MIT license |

## Test

```bash
python -m unittest -v
```

## API

`GET /api/demo` returns sample inputs. `POST /api/analyse` accepts the same JSON shape and returns `summary`, `rows`, `chart`, `notes` and project-specific details. Invalid input returns HTTP 400 with an `error` message. Requests are limited to 1 MB. The server is intentionally local-only.

```bash
curl -H "Content-Type: application/json" --data-binary @sample.json http://127.0.0.1:8000/api/analyse
```

## Development status

Working initial portfolio release. Tests cover the core calculations and selected failure cases; this is not an independently certified engineering or institutional system. Contributions that add benchmark validation, accessibility improvements and documented use cases are welcome.
