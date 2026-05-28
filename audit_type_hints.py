import ast
import sys


class TypeHintAuditor(ast.NodeVisitor):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.issues: list[tuple[int, str]] = []
        self.context_stack: list[str] = []  # To track if we are in a class

    def is_public(self, name: str) -> bool:
        return not name.startswith("_")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.context_stack.append(node.name)
        self.generic_visit(node)
        self.context_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def _check_function(self, node: ast.FunctionDef) -> None:
        if not self.is_public(node.name):
            return

        # Check arguments
        all_args = []
        if hasattr(node.args, "posonlyargs"):
            all_args.extend(node.args.posonlyargs)
        all_args.extend(node.args.args)
        all_args.extend(node.args.kwonlyargs)

        is_method = len(self.context_stack) > 0

        for arg in all_args:
            if is_method and arg.arg in ("self", "cls"):
                continue

            if arg.annotation is None:
                self.issues.append(
                    (
                        arg.lineno,
                        f"Public function '{node.name}' argument '{arg.arg}' lacks type hint",
                    )
                )
            else:
                self._check_for_any(
                    arg.annotation, f"argument '{arg.arg}' in function '{node.name}'", arg.lineno
                )

        # Check return type
        if node.returns is None:
            self.issues.append(
                (node.lineno, f"Public function '{node.name}' lacks return type hint")
            )
        else:
            self._check_for_any(node.returns, f"return type of function '{node.name}'", node.lineno)

    def _check_for_any(self, annotation: ast.AST, context_msg: str, line: int) -> None:
        if isinstance(annotation, ast.Name) and annotation.id == "Any":
            self.issues.append(
                (line, f"Use of 'Any' in {context_msg} (consider more specific type)")
            )
        elif isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name) and annotation.value.id == "Any":
                self.issues.append(
                    (line, f"Use of 'Any' in {context_msg} (consider more specific type)")
                )

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            if self.is_public(node.target.id):
                if node.annotation:
                    self._check_for_any(
                        node.annotation,
                        f"annotation of public variable '{node.target.id}'",
                        node.lineno,
                    )
        self.generic_visit(node)


def run_audit(file_path: str) -> list[str]:
    with open(file_path, encoding="utf-8") as f:
        try:
            content = f.read()
            tree = ast.parse(content)
        except SyntaxError as e:
            return [f"{file_path}:{e.lineno}: Syntax Error: {e.msg}"]
        except Exception as e:
            return [f"{file_path}:0: Error reading file: {str(e)}"]

    auditor = TypeHintAuditor(file_path)
    auditor.visit(tree)

    results = []
    for line, msg in auditor.issues:
        results.append(f"{file_path}:{line}: {msg}")
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audit_type_hints.py <file_path>")
        sys.exit(1)

    file_to_audit = sys.argv[1]
    issues = run_audit(file_to_audit)
    for issue in issues:
        print(issue)
