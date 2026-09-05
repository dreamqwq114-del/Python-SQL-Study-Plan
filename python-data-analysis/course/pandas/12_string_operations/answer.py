"""第 12 节答案：字符串操作。"""

import pandas as pd


def clean_text_fields(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["city"] = result["city"].str.strip().str.lower()
    result["contract_type"] = result["contract_type"].str.strip()
    return result


def filter_products_by_keyword(
    dataframe: pd.DataFrame, keyword: str
) -> pd.DataFrame:
    mask = dataframe["product_name"].str.contains(
        keyword,
        case=False,
        na=False,
        regex=False,
    )
    return dataframe.loc[mask].copy()


def add_product_key(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result["product_key"] = (
        result["product_name"]
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )
    return result
