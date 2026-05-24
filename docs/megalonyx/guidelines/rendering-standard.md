# Rendering Standard

## 1. Visual Philosophy
The goal is a clean, professional look that renders perfectly in a monospace CLI environment without relying on external rendering engines (like LaTeX).

## 2. Prohibited Patterns
- **No LaTeX Delimiters**: NEVER use `$...$` or `$$...$$`.
- **No Complex Math Symbols**: Avoid symbols that require specialized font rendering.

## 3. Mandatory Substitutions
Replace LaTeX symbols with standard Unicode characters:
- Instead of `$\rightarrow$`, use `=>`
- Instead of `$\Rightarrow$`, use `=>`
- Instead of `$\approx$`, use `≈`
- Instead of `$\text{Text}$`, use plain text.

## 4. Approved Layouts
- **ASCII Boxes**: Use `┌`, `┐`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `─`, `│` for structural diagrams.
- **Markdown Tables**: Use standard GFM tables for matrices and comparisons.
- **Bold Identifiers**: Use `**Bold**` for key components and `code` for paths/files.

## 5. Enforcement
Any documentation or architectural output that uses LaTeX delimiters is considered "broken" and must be rewritten to follow this standard.
