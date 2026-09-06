"""第六章练习：模块、导入与项目路径常量。"""

from pathlib import Path

from utils.paths import DATA_DIR, FIGURE_DIR, PROCESSED_DATA_DIR, PROJECT_ROOT


def build_data_path(file_name: str) -> Path:
    """为 data 目录中的 CSV 文件构造路径。

    题目背景：
        项目在不同电脑上的绝对位置不同，代码应从统一的 DATA_DIR 开始拼接路径。

    学生需要完成什么：
        验证 file_name 是简单的 .csv 文件名，再返回 DATA_DIR / file_name。

    参数：
        file_name：不包含文件夹的 CSV 文件名。

    返回值：
        指向项目 data 目录中该文件的 Path。

    输入输出示例：
        build_data_path("sample_customers.csv").name -> "sample_customers.csv"
        build_data_path("orders.csv").parent.name -> "data"

    特殊情况：
        空文件名、绝对路径、包含文件夹或不是 .csv 后缀时产生 ValueError。
        不要求文件已经存在。
    """
    # TODO: 验证文件名并从 DATA_DIR 构造路径。
    raise NotImplementedError("TODO: 实现 build_data_path")


def build_processed_path(file_name: str) -> Path:
    """为处理后的 CSV 构造输出路径。

    题目背景：
        原始数据和处理结果应放在不同目录，避免覆盖原始文件。

    学生需要完成什么：
        验证简单 CSV 文件名并返回 PROCESSED_DATA_DIR / file_name。

    参数：
        file_name：不包含文件夹的 CSV 输出文件名。

    返回值：
        data/processed 目录中的 Path。

    输入输出示例：
        build_processed_path("clean.csv").name -> "clean.csv"
        build_processed_path("result.csv").parent.name -> "processed"

    特殊情况：
        文件名为空、包含路径部分或后缀不是 .csv 时产生 ValueError。
        本函数只构造路径，不写入文件。
    """
    # TODO: 验证文件名并从 PROCESSED_DATA_DIR 构造路径。
    raise NotImplementedError("TODO: 实现 build_processed_path")


def build_figure_path(file_name: str) -> Path:
    """为分析图片构造输出路径。

    题目背景：
        所有图表统一保存到 figures 目录，便于报告引用。

    学生需要完成什么：
        验证文件名以 .png 结尾，并返回 FIGURE_DIR / file_name。

    参数：
        file_name：不包含文件夹的 PNG 文件名。

    返回值：
        figures 目录中的 Path。

    输入输出示例：
        build_figure_path("sales.png").name -> "sales.png"
        build_figure_path("churn.png").parent.name -> "figures"

    特殊情况：
        文件名为空、包含路径部分或不是 .png 后缀时产生 ValueError。
    """
    # TODO: 验证 PNG 文件名并构造图片路径。
    raise NotImplementedError("TODO: 实现 build_figure_path")


def get_project_directories() -> dict[str, Path]:
    """汇总项目中常用的目录常量。

    题目背景：
        导入模块后，可以把分散的路径常量整理成字典供导航程序显示。

    学生需要完成什么：
        返回包含 root、data、processed、figures 四个键的字典。

    参数：
        本函数没有参数。

    返回值：
        值分别为 PROJECT_ROOT、DATA_DIR、PROCESSED_DATA_DIR、FIGURE_DIR 的字典。

    输入输出示例：
        get_project_directories()["data"].name -> "data"
        get_project_directories()["root"] == PROJECT_ROOT -> True

    特殊情况：
        必须直接使用已导入的常量，不要写死本机绝对路径。
    """
    # TODO: 把四个导入的目录常量组织成字典。
    raise NotImplementedError("TODO: 实现 get_project_directories")
