import os
from pathlib import Path
from typing import Any

import yaml
from cryptography.fernet import Fernet, InvalidToken


class SecureConfigManager:
    """
    Manages application configurations by loading from YAML,
    overriding with environment variables, and decrypting sensitive values.
    """

    def __init__(self, yaml_path: str, encryption_key: str | None = None) -> None:
        """
        Initialize the SecureConfigManager.

        Args:
            yaml_path (str): Path to the YAML configuration file.
            encryption_key (Optional[str]): Symmetric key for Fernet decryption.
        """
        self._config = self._load_yaml(yaml_path)
        self._apply_env_overrides()

        self._fernet = None
        if encryption_key:
            try:
                self._fernet = Fernet(encryption_key)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid encryption key provided: {e}")

    def _load_yaml(self, path: str) -> dict:
        """
        Reads and parses the YAML file using safe_load.
        """
        p = Path(path)
        if not p.exists():
            return {}

        with p.open("rt", encoding="utf-8") as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML file: {e}")

        if config is None:
            return {}
        if not isinstance(config, dict):
            raise TypeError("YAML configuration must be a mapping (dictionary)")

        return config

    def _apply_env_overrides(self) -> None:
        """
        Overrides configuration keys with environment variables prefixed with APP_.
        Example: 'database_url' -> 'APP_DATABASE_URL'
        """
        prefix = "APP_"
        for key in list(self._config.keys()):
            env_key = f"{prefix}{key.upper()}"
            env_value = os.environ.get(env_key)
            if env_value is not None:
                self._config[key] = env_value

    def _decrypt_value(self, value: str) -> str:
        """
        Decrypts a value if it starts with the 'ENC:' prefix.
        """
        if not value.startswith("ENC:"):
            return value

        if self._fernet is None:
            raise ValueError(
                "Encrypted value found, but no encryption key was provided during initialization"
            )

        ciphertext = value[len("ENC:") :]
        try:
            plaintext_bytes = self._fernet.decrypt(ciphertext.encode("utf-8"))
            return plaintext_bytes.decode("utf-8")
        except InvalidToken:
            raise ValueError("Invalid encryption key or corrupted token")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value. Decrypts if the value is an encrypted string.

        Args:
            key (str): The configuration key to retrieve.
            default (Any): The value to return if the key is not found.

        Returns:
            Any: The configuration value (decrypted if applicable).
        """
        value = self._config.get(key, default)

        if isinstance(value, str):
            return self._decrypt_value(value)

        return value
