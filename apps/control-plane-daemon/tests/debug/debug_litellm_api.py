import json
import os

from dotenv import load_dotenv
from litellm import completion

# 1. Load Environment
env_path = os.path.expanduser("~/.qwen/.env")
load_dotenv(env_path)

# 2. Load Settings
settings_path = os.path.expanduser("~/.qwen/settings.json")
with open(settings_path) as f:
    settings = json.load(f)

# 3. Extract LongCat Config
# Find LongCat-Flash-Lite in the openai provider group
model_id = "LongCat-Flash-Lite"
config = None
for group, models in settings.get("modelProviders", {}).items():
    for m in models:
        if m["id"] == model_id:
            config = {
                "group": group,
                "model_id": m["id"],
                "base_url": m.get("baseUrl"),
                "env_key": m.get("envKey"),
            }
            break

if not config:
    print("FAILED: Could not find LongCat-Flash-Lite in settings.json")
    exit(1)

# 4. Resolve Key
api_key = os.environ.get(config["env_key"])

print("--- DEBUG INFO ---")
print(f"Model ID: {config['model_id']}")
print(f"Provider Group: {config['group']}")
print(f"Base URL: {config['base_url']}")
print(f"Env Key Name: {config['env_key']}")
print(f"API Key Loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key Prefix: {api_key[:8]}...")
print("------------------")

# 5. Attempt Call
try:
    response = completion(
        model=f"{config['group']}/{config['model_id']}",
        messages=[{"role": "user", "content": "Hello"}],
        api_base=config["base_url"],
        api_key=api_key,
        temperature=0,
    )
    print("SUCCESS: API call returned a response.")
    print(f"Response: {response.choices[0].message.content}")
except (RuntimeError, ValueError, TypeError) as e:
    print(f"FAILED: API call failed with error: {e}")
