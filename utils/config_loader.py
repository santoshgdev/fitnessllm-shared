import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from JSON file.

    Args:
        config_path: Path to config file. If None, uses CONFIG_PATH env var or defaults to 'config.json'

    Returns:
        Dictionary containing configuration values
    """
    # Use CONFIG_PATH environment variable if available
    if config_path is None:
        config_path = os.getenv('CONFIG_PATH', 'config.json')

    config_file = Path(config_path)

    if not config_file.exists():
        print(f"Warning: Configuration file {config_path} not found.")
        print(f"Expected location: {config_file.absolute()}")
        return {}

    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing {config_path}: {e}")
        return {}


def set_env_vars(config: Dict[str, Any]) -> None:
    """Set environment variables from configuration dictionary.

    Args:
        config: Dictionary of key-value pairs to set as environment variables
    """
    for key, value in config.items():
        # Convert snake_case to UPPER_CASE for environment variables
        env_key = key.upper()
        os.environ[env_key] = str(value)
        print(f"Set {env_key}={value}")


def load_config_and_set_env(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration and set environment variables in one step.

    Args:
        config_path: Path to config file. If None, uses CONFIG_PATH env var or defaults to 'config.json'

    Returns:
        Dictionary containing configuration values
    """
    config = load_config(config_path)
    if config:
        set_env_vars(config)
        print(f"Loaded {len(config)} configuration values")
    else:
        print("No configuration loaded")
    return config


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value from environment variables.

    Args:
        key: Configuration key (will be converted to uppercase)
        default: Default value if not found

    Returns:
        Configuration value or default
    """
    env_key = key.upper()
    return os.getenv(env_key, default)


# Legacy main function for backward compatibility
def main():
    """Legacy main function for backward compatibility."""
    load_config_and_set_env()


if __name__ == "__main__":
    main()