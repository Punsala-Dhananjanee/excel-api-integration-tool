import time
import schedule
import threading
from .fetcher import APIFetcher
from .excel_writer import ExcelWriter
from .logger import get_logger

logger = get_logger(__name__)


class Scheduler:
    def __init__(self, config: dict):
        self.config = config
        self.fetcher = APIFetcher(config)
        self.writer = ExcelWriter(config)
        self.interval = config.get("scheduler", {}).get("interval_minutes", 30)
        self.run_immediately = config.get("scheduler", {}).get("run_immediately", True)
        self._stop_event = threading.Event()

    def _job(self):
        logger.info("🔄 Running scheduled data refresh...")
        try:
            data = self.fetcher.fetch_all()
            if data:
                path = self.writer.write(data)
                logger.info(f"✅ Excel updated: {path}")
            else:
                logger.warning("⚠️  No data received — Excel not updated.")
        except Exception as e:
            logger.error(f"❌ Scheduler job failed: {e}", exc_info=True)

    def start(self):
        if self.run_immediately:
            self._job()

        schedule.every(self.interval).minutes.do(self._job)
        logger.info(f"📅 Next run in {self.interval} minutes. Press Ctrl+C to stop.")

        try:
            while not self._stop_event.is_set():
                schedule.run_pending()
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("🛑 Scheduler stopped by user.")

    def stop(self):
        self._stop_event.set()
