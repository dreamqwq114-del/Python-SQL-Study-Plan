"""综合客户项目参考答案。"""

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


CUSTOMER_COLUMNS = [
    "customer_id",
    "age",
    "gender",
    "city",
    "monthly_spending",
    "contract_type",
    "join_date",
    "churn",
    "satisfaction_score",
]
ORDER_COLUMNS = [
    "order_id",
    "customer_id",
    "quantity",
    "unit_price",
    "order_status",
]
ORDER_SUMMARY_COLUMNS = [
    "customer_id",
    "order_count",
    "total_order_spending",
    "average_order_value",
]
NUMERIC_FEATURES = [
    "age",
    "monthly_spending",
    "satisfaction_score",
    "order_count",
    "total_order_spending",
    "average_order_value",
]
CATEGORICAL_FEATURES = ["gender", "city", "contract_type"]


def _require_columns(dataframe: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in dataframe.columns]
    if missing:
        raise KeyError(f"缺少必需列: {missing}")


def load_datasets(
    customer_path: Path,
    order_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """读取并返回客户与订单 CSV。"""
    customers = pd.read_csv(customer_path)
    orders = pd.read_csv(order_path)
    return customers, orders


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """按项目契约清理客户表。"""
    _require_columns(customers, CUSTOMER_COLUMNS)
    cleaned = customers.copy()
    cleaned["customer_id"] = cleaned["customer_id"].astype("string").str.strip()
    invalid_ids = cleaned["customer_id"].isna() | cleaned["customer_id"].eq("")
    if invalid_ids.any():
        raise ValueError("customer_id 不能缺失或为空")
    cleaned = (
        cleaned.drop_duplicates(subset="customer_id", keep="first")
        .reset_index(drop=True)
    )

    cleaned["gender"] = cleaned["gender"].astype("string").str.strip().str.lower()
    cleaned["city"] = cleaned["city"].astype("string").str.strip().str.title()
    cleaned["contract_type"] = (
        cleaned["contract_type"].astype("string").str.strip().str.lower()
    )

    numeric_columns = ["age", "monthly_spending", "satisfaction_score"]
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
        if not cleaned[column].notna().any():
            raise ValueError(f"{column} 没有有效数字")

    cleaned["join_date"] = pd.to_datetime(
        cleaned["join_date"],
        format="mixed",
        errors="coerce",
        dayfirst=True,
    )
    normalized_churn = (
        cleaned["churn"].astype("string").str.strip().str.lower()
    )
    cleaned["churn"] = normalized_churn.map({"no": 0, "yes": 1})
    if cleaned["churn"].isna().any():
        raise ValueError("churn 只能包含 Yes/No，且不能缺失")
    cleaned["churn"] = cleaned["churn"].astype(int)
    return cleaned


def summarize_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """汇总每位客户的已完成订单。"""
    _require_columns(orders, ORDER_COLUMNS)
    prepared = orders.copy()
    try:
        prepared["quantity"] = pd.to_numeric(prepared["quantity"], errors="raise")
        prepared["unit_price"] = pd.to_numeric(
            prepared["unit_price"],
            errors="raise",
        )
    except (TypeError, ValueError) as error:
        raise ValueError("quantity 和 unit_price 必须是数字") from error

    numeric_values = prepared[["quantity", "unit_price"]]
    if numeric_values.isna().any().any() or not np.isfinite(
        numeric_values.to_numpy(dtype=float)
    ).all():
        raise ValueError("quantity 和 unit_price 不能缺失或为无穷值")
    if (prepared["quantity"] < 0).any() or (
        prepared["quantity"] % 1 != 0
    ).any():
        raise ValueError("quantity 必须是非负整数")
    if (prepared["unit_price"] < 0).any():
        raise ValueError("unit_price 不能为负数")

    completed = prepared.loc[
        prepared["order_status"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("completed")
    ].copy()
    if completed.empty:
        return pd.DataFrame(columns=ORDER_SUMMARY_COLUMNS)

    completed["order_total"] = (
        completed["quantity"] * completed["unit_price"]
    )
    summary = (
        completed.groupby("customer_id", as_index=False, sort=True)
        .agg(
            order_count=("order_id", "nunique"),
            total_order_spending=("order_total", "sum"),
            average_order_value=("order_total", "mean"),
        )
        .loc[:, ORDER_SUMMARY_COLUMNS]
    )
    summary["order_count"] = summary["order_count"].astype(int)
    return summary


def merge_customer_summary(
    customers: pd.DataFrame,
    order_summary: pd.DataFrame,
) -> pd.DataFrame:
    """左连接客户表与订单统计，并填充无订单客户。"""
    _require_columns(customers, ["customer_id"])
    _require_columns(order_summary, ORDER_SUMMARY_COLUMNS)
    merged = customers.merge(
        order_summary,
        on="customer_id",
        how="left",
        validate="one_to_one",
        sort=False,
    )
    fill_columns = [
        "order_count",
        "total_order_spending",
        "average_order_value",
    ]
    merged[fill_columns] = merged[fill_columns].fillna(0)
    merged["order_count"] = merged["order_count"].astype(int)
    return merged


def create_customer_figure(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """保存城市消费和流失人数双子图。"""
    _require_columns(dataframe, ["city", "monthly_spending", "churn"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    try:
        city_spending = (
            dataframe.groupby("city")["monthly_spending"]
            .mean()
            .sort_values(ascending=False)
        )
        axes[0].bar(city_spending.index, city_spending.values)
        axes[0].set_title("Average Monthly Spending by City")
        axes[0].set_xlabel("City")
        axes[0].set_ylabel("Average Monthly Spending")
        axes[0].tick_params(axis="x", rotation=30)

        churn_counts = (
            dataframe["churn"].value_counts().reindex([0, 1], fill_value=0)
        )
        axes[1].bar(["No Churn", "Churn"], churn_counts.values)
        axes[1].set_title("Customer Churn Counts")
        axes[1].set_xlabel("Churn Status")
        axes[1].set_ylabel("Customers")

        figure.tight_layout()
        figure.savefig(output_path, dpi=150)
    finally:
        plt.close(figure)


def train_churn_classifier(
    dataframe: pd.DataFrame,
) -> tuple[Any, dict[str, float]]:
    """训练无泄漏的逻辑回归管道并返回测试指标。"""
    required = NUMERIC_FEATURES + CATEGORICAL_FEATURES + ["churn"]
    _require_columns(dataframe, required)
    features = dataframe[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    target = dataframe["churn"].copy()

    if target.isna().any() or not target.isin([0, 1]).all():
        raise ValueError("churn 必须是没有缺失的 0/1 标签")
    class_counts = target.value_counts()
    if len(class_counts) != 2 or int(class_counts.min()) < 2:
        raise ValueError("churn 的两个类别都至少需要 2 个样本")

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.25,
        stratify=target,
        random_state=42,
    )

    numeric_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore"),
            ),
        ]
    )
    preprocessor = ColumnTransformer(
        [
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )
    model = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(max_iter=1000, random_state=42),
            ),
        ]
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
    }
    return model, metrics
