#!/usr/bin/env python3

import argparse
import sys
from src.scheduler import Scheduler
from src.fetcher import APIFetcher
from src.excel_writer import ExcelWriter
from src.config import load_config
from src.logger import get_logger

logger = get_logger(__name__)


def run_once(config):
    fetcher = APIFetcher(config)
    writer = ExcelWriter(config)

    logger.info("Starting one-time data fetch...")
    data = fetcher.fetch_all()

    if data:
        output_path = writer.write(data)
        logger.info(f"[OK] Data saved to: {output_path}")
    else:
        logger.error("[ERROR] No data fetched. Check your API key in .env file.")


def run_scheduler(config):
    scheduler = Scheduler(config)
    logger.info(f"Starting scheduler (interval: {config['scheduler']['interval_minutes']} min)...")
    scheduler.start()


def main():
    parser = argparse.ArgumentParser(description="Excel API Integration Tool")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--once", action="store_true", help="Run once instead of scheduled")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.once:
        run_once(config)
    else:
        run_scheduler(config)


if __name__ == "__main__":
    main()
