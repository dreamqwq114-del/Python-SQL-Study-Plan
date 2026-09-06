"""模块导入与项目路径常量演示。"""

from utils.paths import DATA_DIR, FIGURE_DIR, PROJECT_ROOT


def demo_data_path(file_name: str):
    """演示如何从统一的数据目录常量拼接出路径（不做文件名校验）。"""
    return DATA_DIR / file_name


def main() -> None:
    customer_path = demo_data_path("sample_customers.csv")
    figure_path = FIGURE_DIR / "customer_summary.png"

    print("项目目录：", PROJECT_ROOT.name)
    print("客户数据：", customer_path.relative_to(PROJECT_ROOT).as_posix())
    print("图片输出：", figure_path.relative_to(PROJECT_ROOT).as_posix())
    print("数据存在：", customer_path.exists())


if __name__ == "__main__":
    main()
