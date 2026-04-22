# Excel API Integration Tool

A Python tool that fetches data from any REST API and saves it to a beautifully formatted Excel file with auto-update scheduling built in.

---

## Features

- Fetch data from multiple APIs in one run
- Save data to formatted Excel with styled headers, alternating rows, auto-filter, frozen panes
- Auto-update on a configurable schedule (every 30 minutes by default)
- Column mapping — map any API field to a custom Excel column name
- Retry logic — automatically retries failed requests up to 3 times
- Summary sheet — overview of all fetched sheets and row counts
- Logging — console and daily rotating log files
- Secure — API keys stored in .env file, never exposed to GitHub
- CI/CD — GitHub Actions runs tests on every push

---

## Tech Stack

- Python 3.10+
- openpyxl
- requests
- schedule
- python-dotenv
- PyYAML

---

## Project Structure

    excel-api-integration-tool/
        main.py
        config.yaml
        requirements.txt
        .gitignore
        .github/
            workflows/
                ci.yml
        src/
            config.py
            logger.py
            fetcher.py
            excel_writer.py
            scheduler.py
        tests/
            test_core.py
        data/
            output/
        logs/

---

## Setup

**1. Clone the repository**

    git clone https://github.com/YOUR_USERNAME/excel-api-integration-tool.git
    cd excel-api-integration-tool

**2. Create virtual environment**

    python -m venv venv
    venv\Scripts\activate

**3. Install dependencies**

    pip install -r requirements.txt

**4. Configure your APIs in config.yaml**

    apis:
      - name: "Users"
        url: "https://jsonplaceholder.typicode.com/users"
        method: "GET"
        params: {}
        headers: {}
        sheet_name: "Users"
        columns:
          - { source: "id",    header: "ID" }
          - { source: "name",  header: "Name" }
          - { source: "email", header: "Email" }

**5. Run once**

    python main.py --once

**6. Run with auto-update scheduler**

    python main.py

---

## Output

When the tool runs successfully you will see this in the terminal:

    [2026-04-22 14:00:00] INFO  - Config loaded from: config.yaml
    [2026-04-22 14:00:00] INFO  - Starting one-time data fetch...
    [2026-04-22 14:00:00] INFO  - Fetching: Users
    [2026-04-22 14:00:02] INFO  - 10 rows fetched
    [2026-04-22 14:00:02] INFO  - [OK] Data saved to: data/output/api_data.xlsx

The Excel file is saved to the data/output/ folder with:

- A Summary sheet showing all sheets and row counts
- One sheet per API with formatted headers and data

---

## Keeping API Keys Safe

- Store keys in a .env file in the root folder
- The .env file is listed in .gitignore and never pushed to GitHub
- For GitHub Actions, add your key in repo Settings > Secrets > Actions
- Never paste your API key directly in config.yaml

---

## Run Tests

    pip install pytest pytest-cov
    pytest tests/ -v --cov=src

---

## Configuration Reference

| Key | Description | Default |
|-----|-------------|---------|
| apis[].url | API endpoint URL | required |
| apis[].method | HTTP method GET or POST | GET |
| apis[].sheet_name | Target Excel sheet name | API name |
| apis[].columns | Column mapping list | raw keys |
| excel.output_dir | Where to save Excel files | data/output |
| excel.filename | Output filename | api_data.xlsx |
| excel.overwrite | Overwrite existing file | true |
| excel.add_summary_sheet | Add summary overview sheet | true |
| scheduler.interval_minutes | Refresh interval in minutes | 30 |
| scheduler.run_immediately | Fetch once before first wait | true |

---

## License

MIT
