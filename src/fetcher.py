import requests
import time
from typing import Optional
from .logger import get_logger

logger = get_logger(__name__)

RETRY_ATTEMPTS = 3
RETRY_DELAY = 2


class APIFetcher:
    def __init__(self, config: dict):
        self.apis = config.get("apis", [])

    def fetch_all(self) -> dict:
        results = {}
        for api_conf in self.apis:
            name = api_conf.get("name", api_conf["url"])
            logger.info(f"Fetching: {name}")
            data = self._fetch_with_retry(api_conf)
            if data is not None:
                sheet = api_conf.get("sheet_name", name)
                columns = api_conf.get("columns", [])
                results[sheet] = self._extract_rows(data, columns)
                logger.info(f"  -> {len(results[sheet])} rows fetched")
            else:
                logger.warning(f"  -> Skipped (fetch failed): {name}")
        return results

    def _fetch_with_retry(self, api_conf: dict) -> Optional[list]:
        url = api_conf["url"]
        method = api_conf.get("method", "GET").upper()
        params = api_conf.get("params", {})
        headers = api_conf.get("headers", {})
        auth_token = api_conf.get("auth_token")

        if auth_token:
            headers["Authorization"] = auth_token

        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                if method == "GET":
                    response = requests.get(url, params=params, headers=headers, timeout=15)
                elif method == "POST":
                    response = requests.post(url, json=params, headers=headers, timeout=15)
                else:
                    logger.error(f"Unsupported HTTP method: {method}")
                    return None

                response.raise_for_status()
                data = response.json()

                if isinstance(data, dict):
                    data = [data]

                return data

            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt}/{RETRY_ATTEMPTS} failed for {url}: {e}")
                if attempt < RETRY_ATTEMPTS:
                    time.sleep(RETRY_DELAY * attempt)

        return None

    def _extract_rows(self, data: list, columns: list) -> list:
        if not columns:
            return data

        rows = []
        for item in data:
            row = {}
            for col in columns:
                source = col["source"]
                header = col.get("header", source)
                value = self._get_nested(item, source)
                row[header] = value
            rows.append(row)
        return rows

    def _get_nested(self, obj: dict, key: str):
        keys = key.split(".")
        val = obj
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return None
        return val
