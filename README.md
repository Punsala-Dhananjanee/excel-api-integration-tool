# 💎 Excel API Integration Tool

A Python tool that **fetches data from any REST API** and saves it to a beautifully formatted **Excel file** — with **auto-update scheduling** built in.

---

## Features

- Fetch data from multiple APIs in one run
- Save data to formatted Excel with styled headers, alternating rows, auto-filter, frozen panes
- Auto-update on a configurable schedule (e.g., every 30 minutes)
- Column mapping — map any API field to a custom Excel column name
- Retry logic — automatically retries failed requests
- Summary sheet — overview of all fetched sheets and row counts
- Logging — console + daily rotating log files
- Secure — API keys stored in .env, never exposed to GitHub
- CI/CD — GitHub Actions runs tests on every push

---

## Project Structure
excel-api-integration-tool/
├── main.py
├── config.yaml
├── requirements.txt
├── .env
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── config.py
│   ├── logger.py
│   ├── fetcher.py
│   ├── excel_writer.py
│   └── scheduler.py
├── tests/
│   └── test_core.py
├── data/
│   └── output/
└── logs/
---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/excel-api-integration-tool.git
cd excel-api-integration-tool
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your .env file
OPENAI_API_KEY=sk-proj-your-key-here
### 5. Configure your APIs in config.yaml

```yaml
apis:
  - name: "My API"
    url: "https://jsonplaceholder.typicode.com/users"
    method: "GET"
    params: {}
    headers: {}
    sheet_name: "Users"
    columns:
      - { source: "id",    header: "ID" }
      - { source: "name",  header: "Name" }
      - { source: "email", header: "Email" }
```

### 6. Run once

```bash
python main.py --once
```

### 7. Run with auto-update scheduler

```bash
python main.py
```

---

## Keeping API Keys Safe

- Store keys in .env file only
- .env is listed in .gitignore and never pushed to GitHub
- For GitHub Actions, add your key in repo Settings > Secrets > Actions

---

## Run Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src
```

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
| scheduler.interval_minutes | Refresh interval in minutes | 30 |

---

## Tech Stack

- Python 3.10+
- openpyxl
- requests
- schedule
- python-dotenv
- PyYAML

---

## License

MIT