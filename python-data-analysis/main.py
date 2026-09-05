"""打印课程学习导航。

重构后按“主题/章节”组织：每个章节目录内同时包含教材、示例、练习、
参考答案和测试，学习时无需在多个类型目录之间来回切换。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
COURSE_DIR = PROJECT_ROOT / "course"
PROJECT_CHAPTER = PROJECT_ROOT / "projects" / "combined_customer_project"

TOPICS = [
    ("python", "Python 基础"),
    ("pandas", "Pandas 数据处理"),
    ("matplotlib", "Matplotlib 图表"),
    ("sklearn", "scikit-learn 建模"),
]


def chapter_dirs(topic: str) -> list[Path]:
    return sorted((COURSE_DIR / topic).glob("[0-9][0-9]_*"))


def print_topic_plan(topic: str, title: str) -> None:
    print(f"\n{title}")
    print("=" * 72)
    for chapter_dir in chapter_dirs(topic):
        chapter = chapter_dir.name
        module = f"course.{topic}.{chapter}"
        print(f"\n{chapter}")
        print(f"  教材：{chapter_dir / 'lesson.md'}")
        print(f"  示例：python -m {module}.example")
        print(f"  练习：{chapter_dir / 'practice.py'}")
        print(f"  答案：{chapter_dir / 'answer.py'}")
        print(f"  测试：pytest {chapter_dir / 'test.py'}")


def print_project_plan() -> None:
    print("\n综合客户分析项目")
    print("=" * 72)
    print(f"  教材：{PROJECT_CHAPTER / 'lesson.md'}")
    print("  示例：python -m projects.combined_customer_project.example")
    print(f"  练习：{PROJECT_CHAPTER / 'practice.py'}")
    print(f"  答案：{PROJECT_CHAPTER / 'answer.py'}")
    print(f"  测试：pytest {PROJECT_CHAPTER / 'test.py'}")


def main() -> None:
    print("IOM103 Python 数据分析：章节学习顺序")
    print("所有命令都从 python-data-analysis 项目根目录运行。")
    for topic, title in TOPICS:
        print_topic_plan(topic, title)
    print_project_plan()
    print("\n全量测试：pytest")


if __name__ == "__main__":
    main()
