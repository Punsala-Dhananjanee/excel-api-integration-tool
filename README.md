# 🔥 Excel API Integration Tool

A Python tool that fetches data from any REST API and saves it to a beautifully formatted Excel file with auto-update scheduling.

---

## Features

- Fetch data from multiple APIs in one run
- Save data to formatted Excel with styled headers and auto-filter
- Auto-update on a configurable schedule
- Column mapping — map any API field to a custom Excel column name
- Retry logic — automatically retries failed requests 3 times
- Summary sheet — overview of all fetched sheets and row counts
- Secure — API keys stored in .env, never pushed to GitHub
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

```
excel-api-integration-tool/
│
├── main.py
├── config.yaml
├── requirements.txt
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   ├── config.py
│   ├── logger.py
│   ├── fetcher.py
│   ├── excel_writer.py
│   └── scheduler.py
│
├── tests/
│   └── test_core.py
│
├── data/
│   └── output/
│
└── logs/
```

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/Punsala-Dhananjanee/excel-api-integration-tool.git
cd excel-api-integration-tool
```

**2. Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run once**

```bash
python main.py --once
```

**5. Run with auto-update scheduler**

```bash
python main.py
```

---

## Configuration

Edit `config.yaml` to add your APIs:

```yaml
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
```

---

## Configuration Reference

| Key | Description | Default |
|-----|-------------|---------|
| apis[].url | API endpoint URL | required |
| apis[].method | GET or POST | GET |
| apis[].sheet_name | Excel sheet name | API name |
| apis[].columns | Column mapping | raw keys |
| excel.output_dir | Output folder | data/output |
| excel.filename | Output filename | api_data.xlsx |
| scheduler.interval_minutes | Refresh interval | 30 |

---

## Keeping API Keys Safe

- Store keys in a `.env` file in the root folder
- `.env` is listed in `.gitignore` and never pushed to GitHub
- For GitHub Actions add your key in Settings > Secrets > Actions

---

## Run Tests

```bash
pytest tests/ -v --cov=src
```

---

## License

MIT
