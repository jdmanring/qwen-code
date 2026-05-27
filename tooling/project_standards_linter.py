#!/usr/bin/env python3
"""
project_standards_linter: static analysis enforcing the project's engineering standards.

Rules enforced:
- DOC-02: Conversational tone in mandate/axiom documents
- CONFIG-01: Symmetry break between config/ and docs/
- CONFIG-02: Missing README.md in critical directory
- CONFIG-03: Executable logic in config/ directory
- CODE-01: Missing PEP 484 type hints
- CODE-02: Excessive nesting depth or function length
- CODE-03: Generic exception handling
- CODE-04: DEBUG print statements committed to source
- CODE-05: Primary class name does not match file name
"""

import argparse
import ast
import re
import sys
from collections.abc import Callable
from enum import Enum
from pathlib import Path
from typing import NamedTuple


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class Issue(NamedTuple):
    file: Path
    line: int | None
    rule_id: str
    severity: Severity
    message: str

    def __str__(self) -> str:
        line_str = f":{self.line}" if self.line else ""
        return f"[{self.severity.value}] {self.file}{line_str} {self.rule_id}: {self.message}"


class Rule:
    def __init__(
        self,
        rule_id: str,
        severity: Severity,
        check_func: Callable[[Path, str], list[Issue]],
        description: str,
    ) -> None:
        self.rule_id = rule_id
        self.severity = severity
        self.check_func = check_func
        self.description = description


class ProjectStandardsLinter:
    def __init__(self, root_dir: Path, strict: bool = False) -> None:
        self.root_dir = root_dir
        self.strict = strict
        self.rules: list[Rule] = []
        self._setup_rules()

    def _setup_rules(self) -> None:
        self.rules.append(
            Rule(
                "DOC-01",
                Severity.CRITICAL,
                self._check_ascii_compliance,
                "Non-ASCII character detected. Use ASCII only for efficiency.",
            )
        )
        self.rules.append(
            Rule(
                "DOC-02",
                Severity.CRITICAL,
                self._check_conversational_language,
                "Conversational tone in mandate/axiom document. Use imperative language.",
            )
        )
        self.rules.append(
            Rule(
                "CONFIG-01",
                Severity.CRITICAL,
                self._check_config_docs_symmetry,
                "Symmetry break between config/ and docs/.",
            )
        )
        self.rules.append(
            Rule(
                "CONFIG-02",
                Severity.WARNING,
                self._check_qwen_context_files,
                "Missing README.md in critical directory.",
            )
        )
        self.rules.append(
            Rule(
                "CONFIG-03",
                Severity.WARNING,
                self._check_config_has_no_logic,
                "Executable logic found in config/ directory. Config must be static.",
            )
        )
        self.rules.append(
            Rule(
                "CODE-01",
                Severity.WARNING,
                self._check_type_hints,
                "Missing PEP 484 type hints.",
            )
        )
        self.rules.append(
            Rule(
                "CODE-02",
                Severity.INFO,
                self._check_complexity,
                "Nesting depth or function length exceeds limit.",
            )
        )
        self.rules.append(
            Rule(
                "CODE-03",
                Severity.CRITICAL,
                self._check_exception_specificity,
                "Generic exception handler. Use specific exception types.",
            )
        )
        self.rules.append(
            Rule(
                "CODE-04",
                Severity.CRITICAL,
                self._check_debug_prints,
                "DEBUG print statement in committed source.",
            )
        )
        self.rules.append(
            Rule(
                "CODE-05",
                Severity.WARNING,
                self._check_file_class_name_match,
                "Single-class file: class name does not match file name.",
            )
        )

    # --- DOC domain ---

    def _check_ascii_compliance(self, path: Path, content: str) -> list[Issue]:
        # Skip binary files or specific exclusions if needed
        if path.suffix in (".png", ".jpg", ".gif", ".ico"):
            return []

        violations = []
        for i, line in enumerate(content.splitlines(), 1):
            # Find first non-ASCII character
            for char in line:
                if ord(char) > 127:
                    violations.append(
                        Issue(
                            path,
                            i,
                            "DOC-01",
                            Severity.CRITICAL,
                            f"Non-ASCII char '{char}' (U+{ord(char):04X}) "
                            f"detected. Use ASCII only.",
                        )
                    )
                    break  # Only report one violation per line to avoid spam
        return violations

    def _check_conversational_language(self, path: Path, content: str) -> list[Issue]:
        if path.suffix == ".py":
            return []
        is_target_name = path.name in ("QWEN.md", "agent-system.md")
        is_target_content = "Mandate" in content or "Axiom" in content
        if not (is_target_name or is_target_content):
            return []

        pattern = re.compile(
            r"(?i)\b(I think|Please try to|It would be a good idea|I suggest|maybe|possibly)\b"
        )
        violations = []
        for i, line in enumerate(content.splitlines(), 1):
            if pattern.search(line):
                violations.append(
                    Issue(
                        path,
                        i,
                        "DOC-02",
                        Severity.CRITICAL,
                        "Conversational tone detected. Use imperative, precise language.",
                    )
                )
        return violations

    # --- CONFIG domain ---

    def _check_config_docs_symmetry(self, path: Path, content: str) -> list[Issue]:
        if path != self.root_dir:
            return []

        config_dir = self.root_dir / "config"
        docs_dir = self.root_dir / "docs"
        if not config_dir.exists() or not docs_dir.exists():
            return [
                Issue(
                    self.root_dir,
                    None,
                    "CONFIG-01",
                    Severity.CRITICAL,
                    "Missing config/ or docs/ directory.",
                )
            ]

        violations = []
        for item in sorted(config_dir.rglob("*")):
            relative_path = item.relative_to(config_dir)
            if item.is_dir():
                if not (docs_dir / relative_path).exists():
                    violations.append(
                        Issue(
                            item,
                            None,
                            "CONFIG-01",
                            Severity.CRITICAL,
                            f"Symmetry break: {relative_path} missing in docs/",
                        )
                    )
            elif item.is_file():
                if item.suffix in (".lock", ".template"):
                    continue
                if item.name.startswith("."):
                    continue
                if not (docs_dir / relative_path.with_suffix(".md")).exists():
                    violations.append(
                        Issue(
                            item,
                            None,
                            "CONFIG-01",
                            Severity.CRITICAL,
                            f"Symmetry break: {relative_path} missing in docs/",
                        )
                    )

        for item in sorted(docs_dir.rglob("*")):
            if item.is_file() and item.suffix == ".md":
                relative_path = item.relative_to(docs_dir)
                config_parent = config_dir / relative_path.parent
                if config_parent.exists():
                    found = any(
                        f.is_file()
                        and f.stem == item.stem
                        and f.suffix not in (".lock", ".template")
                        for f in config_parent.iterdir()
                    )
                    if not found:
                        violations.append(
                            Issue(
                                item,
                                None,
                                "CONFIG-01",
                                Severity.WARNING,
                                f"Symmetry break: {relative_path} missing in config/",
                            )
                        )
        return violations

    def _check_qwen_context_files(self, path: Path, content: str) -> list[Issue]:
        if path != self.root_dir:
            return []

        critical_dirs = ["packages", "scripts", "config", "docs"]
        violations = []
        for d_name in critical_dirs:
            d_path = self.root_dir / d_name
            if d_path.exists() and d_path.is_dir() and not (d_path / "README.md").exists():
                violations.append(
                    Issue(
                        d_path,
                        None,
                        "CONFIG-02",
                        Severity.WARNING,
                        f"Missing README.md in critical directory: {d_name}",
                    )
                )
        return violations

    def _check_config_has_no_logic(self, path: Path, content: str) -> list[Issue]:
        if path.suffix != ".py":
            return []
        try:
            rel_path = path.relative_to(self.root_dir)
        except ValueError:
            return []

        if str(rel_path).startswith("config/") and not any(
            x in path.name for x in ("schema", "constants")
        ):
            return [
                Issue(
                    path,
                    None,
                    "CONFIG-03",
                    Severity.WARNING,
                    "Executable logic in config/. Config must be static schemas or constants.",
                )
            ]
        return []

    # --- CODE domain ---

    def _check_type_hints(self, path: Path, content: str) -> list[Issue]:
        if path.suffix != ".py":
            return []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.arg in ("self", "cls") or arg.annotation:
                        continue
                    violations.append(
                        Issue(
                            path,
                            node.lineno,
                            "CODE-01",
                            Severity.WARNING,
                            f"Missing type hint for argument '{arg.arg}' in '{node.name}'",
                        )
                    )
                if node.returns is None:
                    violations.append(
                        Issue(
                            path,
                            node.lineno,
                            "CODE-01",
                            Severity.WARNING,
                            f"Missing return type hint for '{node.name}'",
                        )
                    )
        return violations

    def _check_complexity(self, path: Path, content: str) -> list[Issue]:
        if path.suffix != ".py":
            return []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        violations: list[Issue] = []

        class NestingVisitor(ast.NodeVisitor):
            def __init__(self, file_path: Path) -> None:
                self.file_path = file_path
                self.depth = 0
                self.max_depth = 3

            def visit_block(self, node: ast.AST) -> None:
                self.depth += 1
                if self.depth > self.max_depth:
                    violations.append(
                        Issue(
                            self.file_path,
                            node.lineno,  # type: ignore[attr-defined]
                            "CODE-02",
                            Severity.INFO,
                            f"Nesting depth {self.depth} exceeds limit of {self.max_depth}",
                        )
                    )
                self.generic_visit(node)
                self.depth -= 1

            def visit_If(self, node: ast.If) -> None:
                self.visit_block(node)

            def visit_For(self, node: ast.For) -> None:
                self.visit_block(node)

            def visit_While(self, node: ast.While) -> None:
                self.visit_block(node)

            def visit_With(self, node: ast.With) -> None:
                self.visit_block(node)

            def visit_Try(self, node: ast.Try) -> None:
                self.visit_block(node)

        visitor = NestingVisitor(path)
        visitor.visit(tree)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start = node.lineno
                end = getattr(node, "end_lineno", start)
                if (end - start) > 50:
                    violations.append(
                        Issue(
                            path,
                            start,
                            "CODE-02",
                            Severity.INFO,
                            f"Function '{node.name}' is {end - start} lines (limit: 50).",
                        )
                    )

        return violations

    def _check_exception_specificity(self, path: Path, content: str) -> list[Issue]:
        if path.suffix != ".py":
            return []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        lines = content.splitlines()
        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None or (
                    isinstance(node.type, ast.Name) and node.type.id == "Exception"
                ):
                    line_idx = node.lineno - 1
                    if line_idx < len(lines) and "# noqa" in lines[line_idx]:
                        continue
                    violations.append(
                        Issue(
                            path,
                            node.lineno,
                            "CODE-03",
                            Severity.CRITICAL,
                            "Generic exception handler. Use specific exception types.",
                        )
                    )
        return violations

    def _check_debug_prints(self, path: Path, content: str) -> list[Issue]:
        if path.suffix != ".py":
            return []

        pattern = re.compile(r'print\s*\(\s*[f"\']*\[?DEBUG', re.IGNORECASE)
        violations = []
        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue
            if pattern.search(line):
                violations.append(
                    Issue(
                        path,
                        i,
                        "CODE-04",
                        Severity.CRITICAL,
                        "DEBUG print statement in committed source. Use a logger.",
                    )
                )
        return violations

    def _check_file_class_name_match(self, path: Path, content: str) -> list[Issue]:
        if path.suffix != ".py":
            return []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        # Only check pure class files -- skip scripts that have module-level functions
        module_level_funcs = [
            node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        if module_level_funcs:
            return []

        public_classes = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
        ]

        if len(public_classes) != 1:
            return []

        class_name = public_classes[0]
        # Convert PascalCase to snake_case, handling acronyms correctly
        # e.g. LSPManager -> lsp_manager, RAGTool -> rag_tool
        snake = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", class_name)
        snake = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", snake).lower()
        snake = re.sub(r"_+", "_", snake).strip("_")

        if path.stem != snake:
            return [
                Issue(
                    path,
                    None,
                    "CODE-05",
                    Severity.WARNING,
                    f"Class '{class_name}' expects file name '{snake}.py', got '{path.name}'",
                )
            ]
        return []

    def lint(self, target_paths: list[Path]) -> list[Issue]:
        all_issues: list[Issue] = []

        for rule in self.rules:
            if rule.rule_id.startswith("CONFIG"):
                all_issues.extend(rule.check_func(self.root_dir, ""))

        for target in target_paths:
            files = [target] if target.is_file() else list(target.rglob("*"))

            for file_path in files:
                if not file_path.is_file() or any(part.startswith(".") for part in file_path.parts):
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, PermissionError):
                    continue

                for rule in self.rules:
                    if rule.rule_id.startswith("CONFIG"):
                        continue
                    all_issues.extend(rule.check_func(file_path, content))

        return all_issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Project standards linter")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Paths to lint. Defaults to current directory.",
    )
    parser.add_argument(
        "--strict", action="store_true", help="Exit with error on any CRITICAL issue."
    )
    args = parser.parse_args()

    root = Path(".").resolve()
    linter = ProjectStandardsLinter(root, strict=args.strict)
    target_paths = [Path(p).resolve() for p in args.paths]

    issues = linter.lint(target_paths)

    if not issues:
        print("\nNo issues found.")
        sys.exit(0)

    print(f"\n{'SEVERITY':<12} {'RULE':<12} {'FILE:LINE':<40} {'MESSAGE'}")
    print("-" * 100)

    severity_map = {Severity.CRITICAL: 0, Severity.WARNING: 1, Severity.INFO: 2}
    sorted_issues = sorted(issues, key=lambda x: (severity_map[x.severity], x.file))

    for issue in sorted_issues:
        file_line = f"{issue.file.name}:{issue.line}" if issue.line else issue.file.name
        print(
            f"{issue.severity.value:<12} {issue.rule_id:<12} {file_line[:39]:<40} {issue.message}"
        )

    print(f"\nFound {len(issues)} issues.")

    if args.strict and any(i.severity == Severity.CRITICAL for i in issues):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
