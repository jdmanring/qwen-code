import os

LOCALES_DIR = "/home/james/projects/megalonyx-monorepo/packages/cli/src/i18n/locales/"


def fix_locale_quotes(file_path: str) -> None:
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    changed = False
    new_lines = []

    for line in lines:
        stripped = line.strip()

        # Case 1: Single-line entry 'key': 'value',
        if (
            ":" in stripped
            and stripped.startswith("'")
            and (stripped.endswith("',") or stripped.endswith("'"))
        ):
            first_quote_end = stripped.find("'", 1)
            if first_quote_end != -1:
                colon_pos = stripped.find(":", first_quote_end)
                if colon_pos != -1:
                    value_part = stripped[colon_pos + 1 :].strip()
                    if value_part.startswith("'") and (
                        value_part.endswith("',") or value_part.endswith("'")
                    ):
                        val_only = value_part[:-1] if value_part.endswith(",") else value_part
                        inner = val_only[1:-1]
                        if "'" in inner:
                            trailing = "," if value_part.endswith(",") else ""
                            indent = line[: line.find("'")]
                            inner_escaped = inner.replace('"', '\\"')
                            new_val = f'"{inner_escaped}"'
                            new_line = f"{indent}{stripped[: colon_pos + 1]} {new_val}{trailing}\n"
                            new_lines.append(new_line)
                            changed = True
                            continue

        # Case 2: Value on its own line
        if stripped.startswith("'") and (stripped.endswith("',") or stripped.endswith("'")):
            if ":" not in stripped:
                val_only = stripped[:-1] if stripped.endswith(",") else stripped
                if val_only.startswith("'") and val_only.endswith("'"):
                    inner = val_only[1:-1]
                    if "'" in inner:
                        trailing = "," if stripped.endswith(",") else ""
                        indent = line[: line.find("'")]
                        inner_escaped = inner.replace('"', '\\"')
                        new_val = f'"{inner_escaped}"'
                        new_line = f"{indent}{new_val}{trailing}\n"
                        new_lines.append(new_line)
                        changed = True
                        continue

        new_lines.append(line)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Fixed {file_path}")


def main() -> None:
    for filename in os.listdir(LOCALES_DIR):
        if filename.endswith(".js"):
            fix_locale_quotes(os.path.join(LOCALES_DIR, filename))


if __name__ == "__main__":
    main()
