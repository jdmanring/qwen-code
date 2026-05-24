from pathlib import Path
from typing import Any

import pytest
import yaml
from cryptography.fernet import Fernet
from tests.secure_config import SecureConfigManager


@pytest.fixture
def encryption_key() -> str:
    return Fernet.generate_key().decode()


@pytest.fixture
def encrypted_val(encryption_key: str) -> str:
    f = Fernet(encryption_key.encode())
    return "ENC:" + f.encrypt(b"secret_password").decode()


@pytest.fixture
def config_file(tmp_path: Path):
    def _create_config(data: dict[str, Any]) -> str:
        p = tmp_path / "config.yaml"
        with p.open("w") as f:
            yaml.dump(data, f)
        return str(p)

    return _create_config


def test_load_yaml_success(config_file: Any) -> None:
    path = config_file({"key": "value", "num": 123})
    mgr = SecureConfigManager(path)
    assert mgr.get("key") == "value"
    assert mgr.get("num") == 123


def test_load_yaml_missing_file() -> None:
    mgr = SecureConfigManager("non_existent.yaml")
    assert mgr.get("any") is None


def test_load_yaml_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "empty.yaml"
    p.write_text("")
    mgr = SecureConfigManager(str(p))
    assert mgr.get("any") is None


def test_load_yaml_malformed(tmp_path: Path) -> None:
    p = tmp_path / "bad.yaml"
    p.write_text("key: : value")  # Invalid YAML
    with pytest.raises(ValueError, match="Error parsing YAML file"):
        SecureConfigManager(str(p))


def test_load_yaml_not_a_dict(tmp_path: Path) -> None:
    p = tmp_path / "list.yaml"
    p.write_text("- item1\n- item2")
    with pytest.raises(TypeError, match="YAML configuration must be a mapping"):
        SecureConfigManager(str(p))


def test_env_override_existing(config_file: Any, monkeypatch: Any) -> None:
    path = config_file({"database_url": "localhost"})
    monkeypatch.setenv("APP_DATABASE_URL", "prod-db")
    mgr = SecureConfigManager(path)
    assert mgr.get("database_url") == "prod-db"


def test_env_override_non_existing(config_file: Any, monkeypatch: Any) -> None:
    path = config_file({"existing": "val"})
    monkeypatch.setenv("APP_NEW_KEY", "new_val")
    mgr = SecureConfigManager(path)
    # This confirms the current behavior: new keys are NOT added via env
    assert mgr.get("new_key") is None


def test_env_override_type_change(config_file: Any, monkeypatch: Any) -> None:
    path = config_file({"port": 8080})
    monkeypatch.setenv("APP_PORT", "9090")
    mgr = SecureConfigManager(path)
    val = mgr.get("port")
    assert val == "9090"
    assert isinstance(val, str)  # Bug: type changed from int to str


def test_decryption_success(
    config_file: Any, encryption_key: str, encrypted_val: str
) -> None:
    path = config_file({"password": encrypted_val})
    mgr = SecureConfigManager(path, encryption_key=encryption_key)
    assert mgr.get("password") == "secret_password"


def test_decryption_no_key(config_file: Any, encrypted_val: str) -> None:
    path = config_file({"password": encrypted_val})
    mgr = SecureConfigManager(path)  # No key
    with pytest.raises(ValueError, match="no encryption key was provided"):
        mgr.get("password")


def test_decryption_invalid_key(
    config_file: Any, encryption_key: str, encrypted_val: str
) -> None:
    path = config_file({"password": encrypted_val})
    wrong_key = Fernet.generate_key().decode()
    mgr = SecureConfigManager(path, encryption_key=wrong_key)
    with pytest.raises(ValueError, match="Invalid encryption key or corrupted token"):
        mgr.get("password")


def test_decryption_corrupted_token(config_file: Any, encryption_key: str) -> None:
    path = config_file({"password": "ENC:not-a-valid-token"})
    mgr = SecureConfigManager(path, encryption_key=encryption_key)
    with pytest.raises(ValueError, match="Invalid encryption key or corrupted token"):
        mgr.get("password")


def test_decryption_empty_token(config_file: Any, encryption_key: str) -> None:
    path = config_file({"password": "ENC:"})
    mgr = SecureConfigManager(path, encryption_key=encryption_key)
    with pytest.raises(ValueError, match="Invalid encryption key or corrupted token"):
        mgr.get("password")


def test_get_default_decryption(config_file: Any, encryption_key: str) -> None:
    path = config_file({})
    mgr = SecureConfigManager(path, encryption_key=encryption_key)
    # If default starts with ENC:, it will try to decrypt it
    with pytest.raises(ValueError, match="Invalid encryption key or corrupted token"):
        mgr.get("missing", default="ENC:invalid")


def test_invalid_encryption_key_init() -> None:
    with pytest.raises(ValueError, match="Invalid encryption key provided"):
        SecureConfigManager("any.yaml", encryption_key="too-short")
