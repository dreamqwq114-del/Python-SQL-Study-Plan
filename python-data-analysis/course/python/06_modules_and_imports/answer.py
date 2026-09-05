"""第六章四道练习的参考答案。"""

from pathlib import Path

from utils.paths import DATA_DIR, FIGURE_DIR, PROCESSED_DATA_DIR, PROJECT_ROOT


def _validate_file_name(file_name: str, suffix: str) -> None:
    """验证简单文件名和扩展名。"""
    path = Path(file_name)
    if file_name == "" or path.is_absolute() or path.name != file_name:
        raise ValueError("必须提供不含文件夹的文件名")
    if path.suffix.lower() != suffix:
        raise ValueError(f"文件扩展名必须是 {suffix}")


def build_data_path(file_name: str) -> Path:
    """构造 data 目录中的 CSV 路径。"""
    _validate_file_name(file_name, ".csv")
    return DATA_DIR / file_name


def build_processed_path(file_name: str) -> Path:
    """构造 data/processed 目录中的 CSV 路径。"""
    _validate_file_name(file_name, ".csv")
    return PROCESSED_DATA_DIR / file_name


def build_figure_path(file_name: str) -> Path:
    """构造 figures 目录中的 PNG 路径。"""
    _validate_file_name(file_name, ".png")
    return FIGURE_DIR / file_name


def get_project_directories() -> dict[str, Path]:
    """返回项目常用目录。"""
    return {
        "root": PROJECT_ROOT,
        "data": DATA_DIR,
        "processed": PROCESSED_DATA_DIR,
        "figures": FIGURE_DIR,
    }
