"""运行完整客户分析流程。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from answers.projects.answer_combined_customer_project import (
    clean_customers,
    create_customer_figure,
    load_datasets,
    merge_customer_summary,
    summarize_orders,
    train_churn_classifier,
)
from utils.paths import DATA_DIR


def main() -> None:
    customers, orders = load_datasets(
        DATA_DIR / "sample_customers.csv",
        DATA_DIR / "sample_orders.csv",
    )
    cleaned_customers = clean_customers(customers)
    order_summary = summarize_orders(orders)
    analysis_data = merge_customer_summary(
        cleaned_customers,
        order_summary,
    )

    with TemporaryDirectory() as temporary_directory:
        figure_path = Path(temporary_directory) / "customer_report.png"
        create_customer_figure(analysis_data, figure_path)
        model, metrics = train_churn_classifier(analysis_data)

        print(
            {
                "raw_customers": len(customers),
                "clean_customers": len(cleaned_customers),
                "analysis_rows": len(analysis_data),
            }
        )
        print(figure_path.exists() and figure_path.stat().st_size > 0)
        print(list(metrics))
        print(all(0.0 <= value <= 1.0 for value in metrics.values()))
        print(list(model.named_steps))


if __name__ == "__main__":
    main()
