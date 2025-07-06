
# Exports_to_LS_Imports

Batch export JSON annotation files to CSV, with robust testing, formatting, and linting automation.

---

## Features
- Batch convert JSON annotation files to CSV using `ExportToCSV`.
- All code and tests are colocated, composable, and easy to maintain.
- Automated testing, linting, and formatting workflows.
- Strict workspace best practices enforced (see `.github/python-instructions.md`).

---

## Project Structure

- `src/` — Main Python source code (e.g. `json_to_csv.py`)
- `tests/` — All test scripts and test data
  - `tests/data/` — Reference JSON files for tests
- `.github/` — Workspace best practices
- `.vscode/` — VS Code tasks for automation
- `pyproject.toml` — Unified config for pytest, Black, isort, flake8

---

## Step-by-Step: Getting Started

### 1. Clone and set up environment

```sh
git clone <your-repo-url>
cd Exports_to_LS_Imports
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
# Or, if using pyproject.toml for tools:
pip install black isort flake8 pytest
```

### 3. Run the batch exporter

```sh
python src/json_to_csv.py <input_json_path> <output_csv_path>
# Or use your own script that imports ExportToCSV
```

### 4. Run all tests

```sh
pytest
# Or use the VS Code test task
```

### 5. Format and lint code

```sh
black src/ tests/
isort src/ tests/
flake8 src/ tests/
# Or use VS Code tasks for formatting/linting
```

---

## Best Practices

All contributors MUST follow the rules in `.github/python-instructions.md` (coding, testing, commit messages, etc). See that file for details and shortcuts.

---

## Example: Using ExportToCSV in Python

```python
from json_to_csv import ExportToCSV
import json

with open('tests/data/original_format_reference.json') as f:
    data = json.load(f)
exporter = ExportToCSV(data)
records = exporter.to_records()
# ...
```
