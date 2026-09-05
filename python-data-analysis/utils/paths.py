"""集中管理项目相对路径，避免写死本机绝对路径。"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# 所有代码从项目根目录拼接相对路径，不依赖具体电脑用户名或盘符。
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FIGURE_DIR = PROJECT_ROOT / "figures"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
