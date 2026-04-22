import pytest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from unittest.mock import patch, MagicMock
from src.fetcher import APIFetcher
from src.excel_writer import ExcelWriter


MOCK_CONFIG = {
    "apis": [
        {
            "name": "Test API",
            "url": "https://jsonplaceholder.typicode.com/posts",
            "method": "GET",
            "params": {},
            "headers": {},
            "sheet_name": "Test Sheet",
            "columns": [
                {"source": "id",    "header": "ID"},
                {"source": "title", "header": "Title"},
            ],
        }
    ],
    "excel": {
        "output_dir": "data/test_output",
        "filename": "test_output.xlsx",
        "overwrite": True,
        "add_summary_sheet": True,
        "freeze_panes": True,
        "auto_filter": True,
    },
    "scheduler": {"interval_minutes": 5, "run_immediately": False},
}


class TestAPIFetcher:
    def setup_method(self):
        self.fetcher = APIFetcher(MOCK_CONFIG)

    def test_extract_rows_with_mapping(self):
        raw = [{"id": 1, "title": "Hello", "body": "World"}]
        columns = [{"source": "id", "header": "ID"}, {"source": "title", "header": "Title"}]
        rows = self.fetcher._extract_rows(raw, columns)
        assert rows == [{"ID": 1, "Title": "Hello"}]

    def test_extract_rows_no_mapping(self):
        raw = [{"id": 1, "name": "Test"}]
        rows = self.fetcher._extract_rows(raw, [])
        assert rows == raw

    def test_get_nested_flat(self):
        obj = {"id": 42}
        assert self.fetcher._get_nested(obj, "id") == 42

    def test_get_nested_dot_notation(self):
        obj = {"user": {"address": {"city": "Colombo"}}}
        assert self.fetcher._get_nested(obj, "user.address.city") == "Colombo"

    def test_get_nested_missing_key(self):
        obj = {"id": 1}
        assert self.fetcher._get_nested(obj, "missing.key") is None

    @patch("src.fetcher.requests.get")
    def test_fetch_all_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [{"id": 1, "title": "Post 1"}]
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = self.fetcher.fetch_all()
        assert "Test Sheet" in result
        assert result["Test Sheet"][0]["ID"] == 1

    @patch("src.fetcher.requests.get")
    def test_fetch_all_failure(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        result = self.fetcher.fetch_all()
        assert result == {}


class TestExcelWriter:
    def setup_method(self):
        self.writer = ExcelWriter(MOCK_CONFIG)

    def test_write_creates_file(self, tmp_path):
        self.writer.cfg["output_dir"] = str(tmp_path)
        self.writer.output_dir = str(tmp_path)
        data = {"Sheet1": [{"Col A": "val1", "Col B": 42}]}
        path = self.writer.write(data)
        assert os.path.exists(path)

    def test_write_empty_data(self, tmp_path):
        self.writer.cfg["output_dir"] = str(tmp_path)
        self.writer.output_dir = str(tmp_path)
        path = self.writer.write({})
        assert os.path.exists(path)
