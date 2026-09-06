"""检查课程文件配对、接口隔离和可移植性（chapter-centric 结构）。"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = PROJECT_ROOT / "course"
PROJECT_CHAPTER = PROJECT_ROOT / "projects" / "combined_customer_project"
DOMAIN_COUNTS = {
    "python": 9,
    "pandas": 14,
    "matplotlib": 6,
    "sklearn": 15,
}
LEARNING_ROOTS = [
    COURSE_ROOT,
    PROJECT_ROOT / "projects",
    PROJECT_ROOT / "independent_readiness",
]
# 每章必备的四个文件；example.py 仅少数“值得单独运行的完整案例”保留
REQUIRED_CHAPTER_FILES = ("lesson.md", "practice.py", "answer.py", "test.py")
STANDALONE_EXAMPLES = {
    ("python", "06_modules_and_imports"),
    ("sklearn", "11_model_comparison"),
}


def _chapter_names(domain: str) -> list[str]:
    return sorted(
        path.parent.name
        for path in (COURSE_ROOT / domain).glob("*/lesson.md")
    )


def _chapter_file(domain: str, chapter: str, name: str) -> Path:
    return COURSE_ROOT / domain / chapter / name


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
        for name in REQUIRED_CHAPTER_FILES:
            assert _chapter_file(domain, chapter, name).is_file(), (
                f"{domain}/{chapter} 缺少 {name}"
            )
        has_example = _chapter_file(domain, chapter, "example.py").is_file()
        expect_example = (domain, chapter) in STANDALONE_EXAMPLES
        assert has_example == expect_example, (
            f"{domain}/{chapter} 的 example.py 保留状态不符合白名单约定"
        )
        lesson = _chapter_file(domain, chapter, "lesson.md").read_text(encoding="utf-8")
        if not expect_example:
            # 普通章不再保留 example.py，完整示例必须内联进 lesson，且提示折叠在末尾
            assert "本章完整示例" in lesson, f"{domain}/{chapter} 缺少内联完整示例"
            assert "```python" in lesson, f"{domain}/{chapter} 完整示例缺少代码块"
            assert "本节提示（卡住时再展开）" in lesson, f"{domain}/{chapter} 缺少折叠提示"


@pytest.mark.parametrize("domain", DOMAIN_COUNTS)
def test_practice_and_answer_interfaces_match(domain: str) -> None:
    for chapter in _chapter_names(domain):
        practice_nodes = _public_nodes(_chapter_file(domain, chapter, "practice.py"))
        answer_nodes = _public_nodes(_chapter_file(domain, chapter, "answer.py"))
        assert practice_nodes.keys() == answer_nodes.keys(), chapter
        for name in practice_nodes:
            assert type(practice_nodes[name]) is type(answer_nodes[name]), chapter
            assert _arguments(practice_nodes[name]) == _arguments(answer_nodes[name])


def test_examples_and_answers_do_not_contain_starter_code() -> None:
    for root in (COURSE_ROOT, PROJECT_CHAPTER.parent):
        for path in root.rglob("*.py"):
            if path.name in ("practice.py", "test.py", "conftest.py") or path.name.startswith("_"):
                continue
            source = path.read_text(encoding="utf-8")
            assert "TODO" not in source, path
            assert "NotImplementedError" not in source, path


def test_practice_functions_have_consistent_starter_state() -> None:
    """每个练习函数要么是可识别的模板，要么已经移除模板标记。"""
    paths = list(COURSE_ROOT.glob("*/[0-9][0-9]_*/practice.py"))
    paths.append(PROJECT_CHAPTER / "practice.py")
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
        for path in (COURSE_ROOT / domain).glob("*/lesson.md")
    ]
    assert len(paths) == 44
    for path in paths:
        source = path.read_text(encoding="utf-8")
        domain = path.parent.parent.name
        chapter = path.parent.name
        standalone = (domain, chapter) in STANDALONE_EXAMPLES
        assert "实际问题" in source, path
        assert "常见错误" in source, path
        if standalone:
            # 保留独立 example.py 的章节，用 python -m 运行完整案例
            assert f"python -m course.{domain}.{chapter}.example" in source, path
        else:
            # 普通章节把完整示例内联进 lesson
            assert "本章完整示例" in source, path
        assert "本节提示（卡住时再展开）" in source, path
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
    files = [
        PROJECT_CHAPTER / "lesson.md",
        PROJECT_CHAPTER / "example.py",
        PROJECT_CHAPTER / "practice.py",
        PROJECT_CHAPTER / "answer.py",
        PROJECT_CHAPTER / "test.py",
    ]
    assert all(path.is_file() for path in files)

    practice_nodes = _public_nodes(PROJECT_CHAPTER / "practice.py")
    answer_nodes = _public_nodes(PROJECT_CHAPTER / "answer.py")
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
        "py -3.12 -m venv .venv",
        "python -m course.python.06_modules_and_imports.example",
        "course/python/01_variables_and_types/test.py",
        "course/pandas",
        "course/matplotlib",
        "course/sklearn",
        "projects/combined_customer_project/test.py",
        "147 passed, 147 xfailed",
        "162 passed, 147 xfailed",
    ]
    for text in required:
        assert text in source, f"README 缺少 {text}"


def test_recent_clarity_fixes_remain_visible_without_revealing_answers() -> None:
    metrics_lesson = (
        COURSE_ROOT / "sklearn" / "09_classification_metrics" / "lesson.md"
    ).read_text(encoding="utf-8")
    assert "specificity" in metrics_lesson
    assert "TN / (TN + FP)" in metrics_lesson

    readiness = (
        PROJECT_ROOT / "independent_readiness" / "README.md"
    ).read_text(encoding="utf-8")
    assert "初次作答保存前不允许" in readiness
    assert "首次作答保存后才能打开 `rubric.md`" in readiness

    class_practice = COURSE_ROOT / "python" / "09_basic_classes" / "practice.py"
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
