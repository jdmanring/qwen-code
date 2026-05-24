# Getting Started

### 1. Global Installation
The system requires a global installation of the Qwen Code package:

```bash
npm install -g qwen-code
```

### 2. Environment Bootstrapping
Initial execution automatically initializes the `~/.qwen` directory and generates the default configuration from `settings.example.json`.

### 3. Blueprint Localization
Project-level overrides and documentation are maintained in the Blueprint directory. This directory serves as the static definition (Blueprint) and is distinct from the runtime engine.

### 4. Configuration Overrides
To customize the runtime, the following overrides must be applied:

```bash
cp ../../QWEN.md ~/.qwen/QWEN.md           # prompt override
cp ../../settings.example.json ~/.qwen/settings.json
cp -r ../../sync_folder/* ~/.qwen/
```

### 5. System Activation

```bash
qwen-code   # or ./scripts/qwencode.sh if you need the Qdrant helper
```

*Reference:* `../design/install.md` and `../project/qwen_code_installation_method.md`.
