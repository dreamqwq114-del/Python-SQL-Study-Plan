"""检查课程文件配对、接口隔离和可移植性。"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOMAIN_COUNTS = {
    "python": 9,
    "pandas": 14,
    "matplotlib": 6,
    "sklearn": 15,
}
LEARNING_ROOTS = [
    PROJECT_ROOT / "lessons",
    PROJECT_ROOT / "examples",
    PROJECT_ROOT / "practice",
    PROJECT_ROOT / "answers",
    PROJECT_ROOT / "independent_readiness",
]


def _chapter_names(domain: str) -> list[str]:
    lesson_directory = PROJECT_ROOT / "lessons" / domain
    return sorted(path.stem for path in lesson_directory.glob("[0-9][0-9]_*.md"))


def _public_nodes(path: Path) -> dict[str, ast.AST]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    }


def _arguments(node: ast.AST) -> str:
    if isinstance(node, ast.FunctionDef):
        return ast.dump(node.args, include_attributes=False)
    if isinstance(node, ast.ClassDef):
        methods = [
            child
            for child in node.body
            if isinstance(child, ast.FunctionDef)
            and not child.name.startswith("_")
        ]
        return "|".join(
            f"{method.name}:{ast.dump(method.args, include_attributes=False)}"
            for method in methods
        )
    raise TypeError("只比较函数或类")


@pytest.mark.parametrize(
    ("domain", "expected_count"),
    DOMAIN_COUNTS.items(),
)
def test_chapter_files_are_paired(domain: str, expected_count: int) -> None:
    chapters = _chapter_names(domain)
    assert len(chapters) == expected_count

    for chapter in chapters:
        assert (
            PROJECT_ROOT / "examples" / domain / f"example_{chapter}.py"
        ).is_file()
        assert (
            PROJECT_ROOT / "practice" / domain / f"practice_{chapter}.py"
        ).is_file()
        assert (
            PROJECT_ROOT / "answers" / domain / f"answer_{chapter}.py"
        ).is_file()


@pytest.mark.parametrize("domain", DOMAIN_COUNTS)
def test_practice_and_answer_interfaces_match(domain: str) -> None:
    for chapter in _chapter_names(domain):
        practice_path = (
            PROJECT_ROOT / "practice" / domain / f"practice_{chapter}.py"
        )
        answer_path = (
            PROJECT_ROOT / "answers" / domain / f"answer_{chapter}.py"
        )
        practice_nodes = _public_nodes(practice_path)
        answer_nodes = _public_nodes(answer_path)
        assert practice_nodes.keys() == answer_nodes.keys()
        for name in practice_nodes:
            assert type(practice_nodes[name]) is type(answer_nodes[name])
            assert _arguments(practice_nodes[name]) == _arguments(answer_nodes[name])


def test_examples_and_answers_do_not_contain_starter_code() -> None:
    for root_name in ("examples", "answers"):
        for path in (PROJECT_ROOT / root_name).rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            assert "TODO" not in source, path
            assert "NotImplementedError" not in source, path


def test_practice_functions_have_consistent_starter_state() -> None:
    """每个练习函数要么是可识别的模板，要么已经移除模板标记。"""
    paths = [
        path
        for path in (PROJECT_ROOT / "practice").rglob("*.py")
        if path.name != "__init__.py"
    ]
    assert len(paths) == 45
    for path in paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        functions = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not node.name.startswith("_")
        ]
        assert functions, path
        for function in functions:
            function_source = ast.get_source_segment(source, function) or ""
            has_todo = "TODO" in function_source
            has_not_implemented = "NotImplementedError" in function_source
            if has_not_implemented:
                assert has_todo, f"模板函数缺少 TODO 标记: {path}:{function.lineno}"
            else:
                assert not has_todo, f"已完成函数仍含 TODO 标记: {path}:{function.lineno}"


def test_lessons_have_learning_support_sections() -> None:
    paths = [
        path
        for domain in DOMAIN_COUNTS
        for path in (PROJECT_ROOT / "lessons" / domain).glob("*.md")
    ]
    assert len(paths) == 44
    for path in paths:
        source = path.read_text(encoding="utf-8")
        assert "实际问题" in source, path
        assert "常见错误" in source, path
        assert "python -m examples" in source, path
        assert "pytest" in source, path
        assert "检查清单" in source, path
        assert "ORIGINAL_PROJECT_ANALYSIS.md" in source, path


def test_learning_sources_are_portable_and_use_allowed_dependencies() -> None:
    forbidden = [
        "C:\\\\Users\\\\",
        "C:/Users/",
        "import seaborn",
        "from seaborn",
        "get_ipython(",
        "jupyter notebook",
    ]
    files = [
        path
        for root in LEARNING_ROOTS
        for path in root.rglob("*")
        if path.suffix in {".py", ".md"}
    ]
    files.extend([PROJECT_ROOT / "README.md", PROJECT_ROOT / "main.py"])
    for path in files:
        source = path.read_text(encoding="utf-8").lower()
        for text in forbidden:
            assert text.lower() not in source, f"{path}: {text}"


def test_integrated_project_files_and_interfaces_exist() -> None:
    lesson = PROJECT_ROOT / "lessons/projects/combined_customer_project.md"
    example = (
        PROJECT_ROOT
        / "examples/projects/example_combined_customer_project.py"
    )
    practice = (
        PROJECT_ROOT / "practice/projects/combined_customer_project.py"
    )
    answer = (
        PROJECT_ROOT
        / "answers/projects/answer_combined_customer_project.py"
    )
    test = (
        PROJECT_ROOT
        / "tests/projects/test_combined_customer_project.py"
    )
    assert all(path.is_file() for path in [lesson, example, practice, answer, test])

    practice_nodes = _public_nodes(practice)
    answer_nodes = _public_nodes(answer)
    expected = {
        "load_datasets",
        "clean_customers",
        "summarize_orders",
        "merge_customer_summary",
        "create_customer_figure",
        "train_churn_classifier",
    }
    assert practice_nodes.keys() == answer_nodes.keys() == expected
    for name in expected:
        assert _arguments(practice_nodes[name]) == _arguments(answer_nodes[name])

    readiness_root = PROJECT_ROOT / "independent_readiness"
    readiness_files = {
        "README.md",
        "assessment.py",
        "rubric.md",
        "bridge_contract.md",
        "bridge_analysis.py",
    }
    assert readiness_files <= {
        path.name for path in readiness_root.iterdir() if path.is_file()
    }
    assert not list(readiness_root.glob("*answer*"))
    assert not list(readiness_root.glob("*hint*"))

    assessment_nodes = _public_nodes(readiness_root / "assessment.py")
    assert assessment_nodes.keys() == {
        "load_sources",
        "build_customer_report",
        "summarize_quality",
        "save_analysis_figure",
        "main",
    }
    bridge_nodes = _public_nodes(readiness_root / "bridge_analysis.py")
    assert bridge_nodes.keys() == {
        "load_project_export",
        "compare_python_summary",
        "main",
    }


def test_readme_contains_runnable_learning_commands() -> None:
    source = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    required = [
        "IOM103_Python_Data_Analysis\\.venv\\Scripts\\python.exe",
        "py -3.12 -m venv .venv",
        "python -m examples.python.example_01_variables_and_types",
        "tests/python/test_python_practice.py",
        "tests/pandas/test_pandas_practice.py",
        "tests/matplotlib/test_matplotlib_practice.py",
        "tests/sklearn/test_sklearn_practice.py",
        "tests/projects/test_combined_customer_project.py",
        "147 passed, 147 xfailed",
        "161 passed, 147 xfailed",
    ]
    for text in required:
        assert text in source


def test_recent_clarity_fixes_remain_visible_without_revealing_answers() -> None:
    metrics_lesson = (
        PROJECT_ROOT / "lessons/sklearn/09_classification_metrics.md"
    ).read_text(encoding="utf-8")
    assert "specificity" in metrics_lesson
    assert "TN / (TN + FP)" in metrics_lesson

    readiness = (PROJECT_ROOT / "independent_readiness/README.md").read_text(
        encoding="utf-8"
    )
    assert "初次作答保存前不允许" in readiness
    assert "首次作答保存后才能打开 `rubric.md`" in readiness

    class_practice = (
        PROJECT_ROOT / "practice/python/practice_09_basic_classes.py"
    )
    tree = ast.parse(class_practice.read_text(encoding="utf-8"))
    methods = [
        child
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        for child in node.body
        if isinstance(child, ast.FunctionDef)
    ]
    assert len(methods) == 9
    assert all(ast.get_docstring(method) for method in methods)
