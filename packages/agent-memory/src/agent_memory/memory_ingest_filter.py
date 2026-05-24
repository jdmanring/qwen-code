import hashlib
import json
import os
import sys
from collections import deque


class MemoryPolicy:
    def __init__(
        self,
        cloud_signals: list[str] | None = None,
        noise_words: list[str] | None = None,
        dedup_window_size: int = 1000,
    ) -> None:
        self.cloud_signals = cloud_signals or [
            "architecture",
            "preference",
            "always",
            "never",
            "standard",
            "policy",
            "remember",
            "long-term",
            "project",
        ]
        self.noise_words = set(noise_words or ["ok", "okay", "yes", "no", "thanks", "cool", "nice"])
        self.dedup_window_size = dedup_window_size

    def classify_tier(self, text: str) -> str:
        lowered = text.lower()
        for signal in self.cloud_signals:
            if signal in lowered:
                return "cloud"
        return "local"

    def is_noise(self, text: str) -> bool:
        words = text.lower().strip().split()
        if not words:
            return True
        return all(word.strip(".,!?") in self.noise_words for word in words)


class MemoryIngestFilter:
    def __init__(self, config_path: str | None = None) -> None:
        # Default config path if not provided
        if config_path is None:
            config_path = os.getenv(
                "STACK_SETTINGS_PATH", os.path.expanduser("~/.qwen/settings.json")
            )

        self.policy = self._load_policy(config_path)

        # Bounded deduplication window
        self.seen_hashes: deque[str] = deque(maxlen=self.policy.dedup_window_size)
        self.seen_set: set[str] = set()  # For O(1) lookup

    def _load_policy(self, config_path: str) -> MemoryPolicy:
        """Loads memory policy from config file with fallbacks."""
        try:
            if os.path.exists(config_path):
                with open(config_path) as f:
                    config = json.load(f)
                    mem_config = config.get("memory", {}).get("policy", {})
                    return MemoryPolicy(
                        cloud_signals=mem_config.get("cloud_signals"),
                        noise_words=mem_config.get("noise_words"),
                        dedup_window_size=mem_config.get("dedup_window_size", 1000),
                    )
        except (OSError, json.JSONDecodeError) as e:
            print(
                f"[memory:ingest_filter] Failed to load config from {config_path}: {e}."
                " Using defaults.",
                file=sys.stderr,
            )

        return MemoryPolicy()

    def classify_tier(self, text: str) -> str:
        return self.policy.classify_tier(text)

    def should_store(self, text: str) -> bool:
        text = text.strip()
        if not text:
            return False

        if self.policy.is_noise(text):
            return False

        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

        # Deduplication logic with bounded window
        if digest in self.seen_set:
            return False

        # If window is full, remove the oldest item from the set
        if len(self.seen_hashes) >= self.policy.dedup_window_size:
            oldest = self.seen_hashes.popleft()
            self.seen_set.discard(oldest)

        self.seen_hashes.append(digest)
        self.seen_set.add(digest)

        return True
