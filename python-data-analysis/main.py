"""显示课程入口和固定学习流程。"""


def main() -> None:
    """打印从第一节到综合项目的学习导航。"""
    print("IOM103 Python 数据分析课程：44 节 + 1 个综合项目")
    print("课程顺序：Python 9 → Pandas 14 → Matplotlib 6 → sklearn 15")
    print()
    print("从第一节开始：")
    print("1. 阅读 lessons/python/01_variables_and_types.md")
    print("2. 运行 python -m examples.python.example_01_variables_and_types")
    print("3. 编辑 practice/python/practice_01_variables_and_types.py")
    print('4. 运行 python -m pytest tests/python/test_python_practice.py -k "01"')
    print()
    print("完成 44 节后：")
    print("5. 阅读 lessons/projects/combined_customer_project.md")
    print("6. 编辑 practice/projects/combined_customer_project.py")
    print("未完成 TODO 时出现 XFAIL 属于预期结果。")


if __name__ == "__main__":
    main()
