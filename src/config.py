import yaml
import os
import re
from dotenv import load_dotenv
from .logger import get_logger

load_dotenv()

logger = get_logger(__name__)


def expand_env_vars(obj):
    if isinstance(obj, str):
        return re.sub(r'\$\{(\w+)\}', lambda m: os.getenv(m.group(1), m.group(0)), obj)
    elif isinstance(obj, dict):
        return {k: expand_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [expand_env_vars(i) for i in obj]
    return obj


def load_config(path: str = "config.yaml") -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    config = expand_env_vars(config)
    logger.info(f"Config loaded from: {path}")
    return config
