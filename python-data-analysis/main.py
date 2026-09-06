"""打印课程学习导航。

按“主题/章节”组织，且尽量减少学习时需要打开的文件：
正常只看 lesson.md（讲解、完整示例、练习要求、折叠提示都在里面），
做题时打开 practice.py，做完或卡住再看 answer.py；
test.py 只负责自动检查，不需要阅读。
只有少数“值得单独运行的完整案例”才额外保留 example.py。
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


def print_chapter(chapter_dir: Path, module: str | None = None) -> None:
    print(f"\n{chapter_dir.name}")
    print(f"  1. 先读教材：{chapter_dir / 'lesson.md'}（含完整示例与折叠提示）")
    print(f"  2. 做练习：{chapter_dir / 'practice.py'}")
    print(f"  3. 对答案：{chapter_dir / 'answer.py'}")
    example = chapter_dir / "example.py"
    if example.exists():
        target = f"{module}.example" if module else "projects.combined_customer_project.example"
        print(f"  完整案例可单独运行：python -m {target}")
    print(f"  自动检查（无需阅读）：pytest {chapter_dir / 'test.py'}")


def print_topic_plan(topic: str, title: str) -> None:
    print(f"\n{title}")
    print("=" * 72)
    for chapter_dir in chapter_dirs(topic):
        print_chapter(chapter_dir, module=f"course.{topic}.{chapter_dir.name}")


def print_project_plan() -> None:
    print("\n综合客户分析项目")
    print("=" * 72)
    print_chapter(PROJECT_CHAPTER)


def main() -> None:
    print("IOM103 Python 数据分析：章节学习顺序")
    print("学习节奏：lesson.md 通读 → practice.py 做题 → answer.py 对答案；test.py 自动检查。")
    print("所有命令都从 python-data-analysis 项目根目录运行。")
    for topic, title in TOPICS:
        print_topic_plan(topic, title)
    print_project_plan()
    print("\n全量测试：pytest")


if __name__ == "__main__":
    main()
