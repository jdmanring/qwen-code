#  Project Scripts: Utility & Automation

This document catalogs the scripts available in the `scripts/` directory and their functions.

##  Script Registry

| Script | Purpose | Usage |
| :--- | :--- | :--- |
| `create-standalone-package.js` | Scaffolds a new standalone package within the monorepo. | `node scripts/create-standalone-package.js <name>` |
| `unused-keys-only-in-locales.json` | (Data File) Tracks unused localization keys for cleanup. | N/A |

---

##  Automation Patterns

The project uses these scripts to maintain the monorepo's structural integrity:
1. **Package Scaffolding**: Ensures new packages follow the same directory structure and configuration as existing ones.
2. **Localization Cleanup**: Periodically identifies and removes unused translation keys to reduce bundle size.
