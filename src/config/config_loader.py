"""Configuration loading and validation."""

import os
import sys
from typing import Dict, Any, Optional
import yaml

# Add src to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_CONFIG = {
    "timeout": 30,
    "max_retries": 3,
    "log_level": "INFO",
    "environment": "production"
}

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults."""
    config = DEFAULT_CONFIG.copy()
    
    # Determine config file path
    if config_path and os.path.exists(config_path):
        config_file = config_path
    else:
        config_file = os.path.join(os.path.dirname(__file__), "settings.yaml")
        
    # Load from YAML file if exists
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                config.update(file_config)
            logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.warning(f"Failed to load config file {config_file}: {e}")
    
    # Override with environment variables
    env_overrides = {
        "TIMEOUT": ("timeout", int),
        "MAX_RETRIES": ("max_retries", int),
        "LOG_LEVEL": ("log_level", str),
        "ENVIRONMENT": ("environment", str)
    }
    
    for env_var, (config_key, cast_type) in env_overrides.items():
        value = os.environ.get(env_var)
        if value is not None:
            try:
                config[config_key] = cast_type(value)
                logger.debug(f"Overrode {config_key} with environment variable")
            except ValueError:
                logger.warning(f"Invalid value for {env_var}, ignoring")
                
    logger.info("Configuration loaded successfully")
    return config
