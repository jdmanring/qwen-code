from pathlib import Path

# Comprehensive ASCII mapping for technical documentation and source code.
# These mappings preserve the semantic meaning of Unicode symbols while
# converting them to the most common ASCII approximations.
REPLACEMENTS = {
    # Punctuation and Dashes
    "\u2014": "--",  # Em dash
    "\u2013": "-",  # En dash
    "\u201c": '"',  # Left double quotation mark
    "\u201d": '"',  # Right double quotation mark
    "\u2018": "'",  # Left single quotation mark
    "\u2019": "'",  # Right single quotation mark
    "\u2026": "...",  # Ellipsis
    # Logic and Math Symbols
    "\u2192": "->",  # Right arrow
    "\u2190": "<-",  # Left arrow
    "\u2194": "<->",  # Left-right arrow
    "\u2264": "<=",  # Less-than or equal
    "\u2265": ">=",  # Greater-than or equal
    "\u00d7": "*",  # Multiplication
    "\u00b5": "u",  # Micro
    "\u2200": "FORALL",  # Universal quantifier
    "\u2201": "EXISTS",  # Existential quantifier
    "\u2202": "del",  # Partial differential
    "\u2203": "NOT EXISTS",  # Negated existential quantifier
    # Box Drawing (Critical for Tree Maps)
    "\u2502": "|",  # Vertical
    "\u2500": "-",  # Horizontal
    "\u251c": "|--",  # Vertical and Right
    "\u2514": "\\_",  # Vertical and Right-Down
    "\u2518": "---",  # Right-down (alternative)
    "\u250c": "+--",  # Corner
    "\u2510": "+--",  # Corner
    "\u253c": "---",  # Horizontal line
    # Typography and Symbols
    "\uff1a": ":",  # Full-width colon
    "\u00a0": " ",  # Non-breaking space
    "\u200b": "",  # Zero-width space (Remove)
    "\u200c": "",  # Zero-width non-joiner (Remove)
    "\u200d": "",  # Zero-width joiner (Remove)
    # Decorative/Emoji (Remove entirely as per mandate)
    "\u2699": "",  # Gear
    "\u2705": "",  # Check mark
    "\u1f680": "",  # Rocket
    "\u26a0": "",  # Warning
    "\u2728": "",  # Sparkles
    "\u1f3dB": "",  # Classical building
    "\u1f4b3": "",  # Credit card
    "\ufe0f": "",  # Variation Selector-16
}


def clean_ascii(root_dir: Path) -> int:
    """
    Recursively scans the project directory and converts all non-ASCII characters
    to their ASCII equivalents based on a predefined mapping, or removes them if
    no mapping exists. This ensures token efficiency and uniform context for LLMs.
    """
    count = 0
    for path in root_dir.rglob("*"):
        # Skip hidden directories (like .git)
        if path.is_file() and not any(part.startswith(".") for part in path.parts):
            try:
                content = path.read_text(encoding="utf-8")
                new_content = content
                changed = False

                # 1. Apply systematic replacements
                for old, new in REPLACEMENTS.items():
                    if old in new_content:
                        new_content = new_content.replace(old, new)
                        changed = True

                # 2. Aggressive fallback: remove any remaining non-ASCII characters (ord > 127)
                final_content = "".join(c if ord(c) <= 127 else "" for c in new_content)
                if final_content != new_content:
                    new_content = final_content
                    changed = True

                if changed:
                    path.write_text(new_content, encoding="utf-8")
                    count += 1
                    print(f"Cleaned: {path}")
            except (UnicodeDecodeError, PermissionError):
                continue
    return count


if __name__ == "__main__":
    target = Path(".").resolve()
    cleaned = clean_ascii(target)
    print(f"\nTotal files cleaned: {cleaned}")
