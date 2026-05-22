 # Git Strategy: The Sovereign Flow

## 🗺️ Branching Architecture
To ensure stability and protect our sovereign innovations, we use a tiered branching strategy:

| Branch | Source | Purpose | Authority |
| :--- | :--- | :--- | :--- |
| `upstream-main` | `upstream/main` | Raw mirror of official QwenL code. | Read-Only |
| `integration` | `upstream-main` | Refactoring and 'Sovereignizing' upstream changes. | Integration Lead |
| `develop` | `integration` | Active development of Mega Code features. | Developer |
| `main` | `develop` | Stable, production-ready Sovereign Blueprint. | Architect |

## 🔄 The Integration Loop
1. **Sourcing**: Pull latest from `upstream/main` $\to$ `upstream-main`.
2. **Refining**: Merge `upstream-main` $\to$ `integration`. Resolve conflicts and adapt to Mega Code architecture.
3. **Building**: Merge `integration` $\to$ `develop`. Implement new features on top of the stable base.
4. **Releasing**: Merge `develop` $\to$ `main` after successful verification.

## 🤝 The Dual-Track Contribution Flow
When contributing back to the official project:
1. Fix bug/feature in `develop`.
2. Extract change $\to$ Public Fork of QwenL.
3. Submit Pull Request from Public Fork $\to$ Official Upstream.

