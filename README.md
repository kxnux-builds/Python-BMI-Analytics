# BMI Analytics

A polished, multi-profile desktop health tracker built in Python.BMI-Analytics combines a modern CustomTkinter GUI with SQLite-backed local storage and Matplotlib visualizations to help users log weight & height, compute BMI, monitor trends (including moving averages), and export historical data as CSV.

---

Table of contents
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Run the App](#run-the-app)
- [Usage (Quick Tour)](#usage-quick-tour)
- [Data & Privacy](#data--privacy)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Packaging / Distribution](#packaging--distribution)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Key Features
- Multi-profile support (create/switch profiles)
- Smart unit handling: metric and imperial conversions for weight & height (kg, lbs, m, cm, ft'in)
- Accurate BMI calculation and classification (Underweight / Normal / Overweight / Obese)
- Trend visualization with moving average smoothing and highlight for latest entry
- CSV export of per-profile history
- Local SQLite storage for secure, offline use
- Dark / Light theme toggle using CustomTkinter
- Ready-to-build desktop distribution (PyInstaller support)

---

## Tech Stack
- Python 3.8+
- CustomTkinter (modern, themed Tkinter wrapper)
- Matplotlib (charts & visualizations)
- SQLite (local persistence)
- PyInstaller (for building distributable executables)
- pytest (unit testing)

Install runtime dependencies:
```bash
pip install -r requirements.txt
```

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kxnux-builds/Python-BMI-Analytics.git
cd Python-BMI-Analytics
```

2. (Recommended) Create and activate a Python virtual environment:
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Run the App

Start the GUI:

```bash
python main.py
```

On first run the app will create local storage (SQLite DB file) and a default profile if none exists.

---

## Usage (Quick Tour)

- Top bar: switch between profiles or create a new one with “+ Add Profile”.
- Log Metrics:
  - Enter Weight and select unit (kg or lbs).
  - Enter Height and select unit (m, cm, or ft'in). The ft'in handler accepts formats like `5'10`, `5.10`, `5-10`, or `5 10`.
  - Click “Save Data” — values are validated, converted to metric, BMI is calculated and saved.
- Dashboard:
  - Time-series chart of BMI with a 3-point moving average and shaded "healthy" BMI band (18.5–24.9).
  - Latest value highlighted, statistics summarised below the chart.
- Manage Data & Export:
  - Scrollable history (saved in metric: weight in kg, height in meters).
  - Export history to CSV (filename: `bmi_export_<profile>_<YYYYMMDD>.csv`).
  - Delete individual records.
- Theme:
  - Toggle Dark Mode on the top-right of the window.

---

## Data & Privacy

All data is stored locally in an SQLite database file (bmi_data.db) in the project directory. No network access, no telemetry. You own your data; exporting to CSV is provided for backup/analysis.

---

## Project Structure

- main.py — Application entrypoint and UI (CustomTkinter) that wires components, charts, and the user experience.
- bmi_logic.py — Core conversion, validation, BMI calculation, categorization, and smoothing (moving average).
- analytics.py — Functions to compute summary statistics and trend language used in the UI.
- database.py — Database manager for SQLite (handles users and entries). (If you want, I can add schema/DDL or show improvements.)
- test_logic.py — Unit tests for core logic (run via pytest).
- requirements.txt — Python dependencies.
- main.spec — PyInstaller spec for building executables.
- LICENSE — MIT license.

Note: I reviewed main.py, bmi_logic.py and analytics.py to craft the README. If you’d like I can also open or improve database.py and tests directly.

---

## Testing

Run unit tests with pytest:

```bash
pytest -q
```

(Tests exercise core calculations and validation — helpful when refactoring.)

---

## Packaging / Distribution

A PyInstaller spec (main.spec) is included to build a single-file or one-folder distribution.

Example:
```bash
pyinstaller --onefile main.spec
```

After PyInstaller finishes, distribute the generated executable from the `dist/` folder. Test the packaged binary on each target platform (Windows/macOS/Linux) because GUI/Matplotlib backends can vary.

---

## Contributing

Contributions welcome. Suggested workflow:
1. Fork the repo.
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Run tests and linters locally.
4. Open a pull request with a clear description and screenshots (if UI changes).

Guidelines:
- Keep UI changes accessible and theme-friendly.
- Add tests for significant logic changes.
- Document DB migrations or schema changes.

---

## Troubleshooting

- Missing CustomTkinter:
  ```bash
  pip install customtkinter
  ```
- Matplotlib rendering issues (headless servers): ensure Tkinter is installed on your OS and Matplotlib is configured to use a GUI backend.
- PyInstaller builds failing due to missing binaries: test builds inside a clean VM or Docker image representative of the target OS.

If you want, I can add a CONTRIBUTING.md and CI configuration (GitHub Actions) to run tests automatically.

---

## Credits & Links

- Author: Kishanu Mondal
- GitHub: https://github.com/kxnux-builds
- LinkedIn: https://www.linkedin.com/in/kishanu-mondal/
- X (Twitter): https://x.com/Kxnux_Dev

---

## License

See the LICENSE file for license details:
[LICENSE](./LICENSE)

---