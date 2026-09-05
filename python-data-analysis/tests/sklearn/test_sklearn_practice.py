"""scikit-learn 15 节、45 道练习与答案的契约测试。"""

from types import ModuleType
from typing import Callable

import numpy as np
import pandas as pd
import pytest
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_classification
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from answers.sklearn import answer_01_features_and_labels as answer_01
from answers.sklearn import answer_02_train_test_split as answer_02
from answers.sklearn import answer_03_categorical_encoding as answer_03
from answers.sklearn import answer_04_standard_scaler as answer_04
from answers.sklearn import answer_05_logistic_regression as answer_05
from answers.sklearn import answer_06_decision_tree as answer_06
from answers.sklearn import answer_07_random_forest as answer_07
from answers.sklearn import answer_08_predict_and_probability as answer_08
from answers.sklearn import answer_09_classification_metrics as answer_09
from answers.sklearn import answer_10_confusion_matrix as answer_10
from answers.sklearn import answer_11_model_comparison as answer_11
from answers.sklearn import answer_12_overfitting_and_leakage as answer_12
from answers.sklearn import answer_13_kmeans as answer_13
from answers.sklearn import answer_14_elbow_method as answer_14
from answers.sklearn import answer_15_silhouette_score as answer_15
from practice.sklearn import practice_01_features_and_labels as practice_01
from practice.sklearn import practice_02_train_test_split as practice_02
from practice.sklearn import practice_03_categorical_encoding as practice_03
from practice.sklearn import practice_04_standard_scaler as practice_04
from practice.sklearn import practice_05_logistic_regression as practice_05
from practice.sklearn import practice_06_decision_tree as practice_06
from practice.sklearn import practice_07_random_forest as practice_07
from practice.sklearn import practice_08_predict_and_probability as practice_08
from practice.sklearn import practice_09_classification_metrics as practice_09
from practice.sklearn import practice_10_confusion_matrix as practice_10
from practice.sklearn import practice_11_model_comparison as practice_11
from practice.sklearn import practice_12_overfitting_and_leakage as practice_12
from practice.sklearn import practice_13_kmeans as practice_13
from practice.sklearn import practice_14_elbow_method as practice_14
from practice.sklearn import practice_15_silhouette_score as practice_15


Check = Callable[[ModuleType], None]


@pytest.fixture(scope="module")
def classification_data() -> tuple[np.ndarray, np.ndarray]:
    return make_classification(
        n_samples=100,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )


@pytest.fixture(scope="module")
def split_classification_data(
    classification_data: tuple[np.ndarray, np.ndarray],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X, y = classification_data
    return train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )


@pytest.fixture(scope="module")
def cluster_data() -> np.ndarray:
    X, _ = make_blobs(
        n_samples=60,
        centers=3,
        cluster_std=0.45,
        random_state=42,
    )
    return X


def tiny_classification() -> tuple[np.ndarray, np.ndarray]:
    return make_classification(
        n_samples=40,
        n_features=3,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )


def check_01_select_features_and_label(module: ModuleType) -> None:
    source = pd.DataFrame(
        {
            "city": ["A", "B"],
            "churn": [0, 1],
            "monthly_spending": [100.0, 150.0],
            "age": [20, 30],
        }
    )
    original = source.copy()
    X, y = module.select_features_and_label(source)
    assert X.columns.tolist() == ["age", "monthly_spending"]
    assert y.tolist() == [0, 1]
    X.loc[0, "age"] = 99
    y.loc[0] = 1
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.select_features_and_label(source.drop(columns="age"))


def check_01_select_mixed_features(module: ModuleType) -> None:
    source = pd.DataFrame(
        {
            "age": [20, 30],
            "monthly_spending": [100.0, 150.0],
            "city": ["A", "B"],
            "churn": [0, 1],
        }
    )
    X, y = module.select_mixed_features(source)
    assert X.columns.tolist() == ["age", "monthly_spending", "city"]
    assert X["city"].tolist() == ["A", "B"]
    assert y.name == "churn"


def check_01_count_target_classes(module: ModuleType) -> None:
    assert module.count_target_classes(pd.Series([0, 1, 0])) == {0: 2, 1: 1}
    assert module.count_target_classes(pd.Series([0, 0])) == {0: 2, 1: 0}
    assert module.count_target_classes(pd.Series([], dtype=int)) == {0: 0, 1: 0}
    with pytest.raises(ValueError):
        module.count_target_classes(pd.Series([0, 2]))
    with pytest.raises(ValueError):
        module.count_target_classes(pd.Series([0, None]))


def check_02_split_data(module: ModuleType) -> None:
    X = pd.DataFrame({"x": range(40)})
    y = pd.Series([0, 1] * 20)
    result = module.split_data(X, y)
    X_train, X_test, y_train, y_test = result
    assert (len(X_train), len(X_test)) == (30, 10)
    assert y_train.mean() == pytest.approx(0.5)
    assert y_test.mean() == pytest.approx(0.5)
    repeated = module.split_data(X, y)
    pd.testing.assert_frame_equal(X_train, repeated[0])
    pd.testing.assert_frame_equal(X_test, repeated[1])


def check_02_split_with_test_size(module: ModuleType) -> None:
    X = pd.DataFrame({"x": range(20)})
    y = pd.Series([0, 1] * 10)
    assert len(module.split_with_test_size(X, y, 0.2)[1]) == 4
    assert len(module.split_with_test_size(X, y, 0.5)[1]) == 10
    with pytest.raises(ValueError):
        module.split_with_test_size(X, y, 0)
    with pytest.raises(ValueError):
        module.split_with_test_size(X, y, 1)


def check_02_summarize_split_balance(module: ModuleType) -> None:
    result = module.summarize_split_balance(
        pd.Series([0, 1]),
        pd.Series([0, 1, 1, 0]),
    )
    assert result == {
        "train_positive_rate": 0.5,
        "test_positive_rate": 0.5,
    }
    with pytest.raises(ValueError):
        module.summarize_split_balance(
            pd.Series([], dtype=int),
            pd.Series([0, 1]),
        )


def check_03_encode_city_feature(module: ModuleType) -> None:
    train = pd.DataFrame({"city": ["A", "B", "A"]})
    test = pd.DataFrame({"city": ["B", "C"]})
    train_encoded, test_encoded = module.encode_city_feature(train, test)
    assert train_encoded.shape == (3, 2)
    assert test_encoded.shape == (2, 2)
    assert np.array_equal(test_encoded[0], np.array([0.0, 1.0]))
    assert np.array_equal(test_encoded[1], np.array([0.0, 0.0]))


def check_03_encode_categorical_features(module: ModuleType) -> None:
    train = pd.DataFrame(
        {
            "city": ["A", "B"],
            "contract": ["Monthly", "Yearly"],
        }
    )
    test = pd.DataFrame(
        {"city": ["C"], "contract": ["Monthly"]}
    )
    train_encoded, test_encoded = module.encode_categorical_features(
        train,
        test,
        ["city", "contract"],
    )
    assert train_encoded.shape == (2, 4)
    assert test_encoded.shape == (1, 4)
    with pytest.raises(ValueError):
        module.encode_categorical_features(train, test, [])
    with pytest.raises(KeyError):
        module.encode_categorical_features(train, test, ["unknown"])


def check_03_get_encoded_feature_names(module: ModuleType) -> None:
    train = pd.DataFrame(
        {
            "city": ["A", "B"],
            "contract": ["Monthly", "Yearly"],
        }
    )
    names = module.get_encoded_feature_names(
        train,
        ["city", "contract"],
    )
    assert names == [
        "city_A",
        "city_B",
        "contract_Monthly",
        "contract_Yearly",
    ]
    with pytest.raises(ValueError):
        module.get_encoded_feature_names(train, [])


def check_04_scale_features(module: ModuleType) -> None:
    train = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
    test = np.array([[4.0, 40.0]])
    train_scaled, test_scaled = module.scale_features(train, test)
    assert np.allclose(train_scaled.mean(axis=0), 0.0)
    assert np.allclose(train_scaled.std(axis=0), 1.0)
    assert test_scaled.shape == (1, 2)
    assert not np.allclose(test_scaled, 0.0)


def check_04_scale_dataframe_columns(module: ModuleType) -> None:
    train = pd.DataFrame(
        {"age": [10.0, 20.0, 30.0], "city": ["A", "B", "C"]}
    )
    test = pd.DataFrame({"age": [40.0], "city": ["D"]})
    original = train.copy()
    train_scaled, test_scaled = module.scale_dataframe_columns(
        train,
        test,
        ["age"],
    )
    assert train_scaled["age"].mean() == pytest.approx(0.0)
    assert train_scaled["city"].tolist() == ["A", "B", "C"]
    assert test_scaled["city"].tolist() == ["D"]
    pd.testing.assert_frame_equal(train, original)
    empty_train, empty_test = module.scale_dataframe_columns(train, test, [])
    pd.testing.assert_frame_equal(empty_train, train)
    pd.testing.assert_frame_equal(empty_test, test)


def check_04_summarize_scaled_training(module: ModuleType) -> None:
    data = np.array([[-1.0, -1.0], [1.0, 1.0]])
    result = module.summarize_scaled_training(data)
    assert np.allclose(result["mean"], [0.0, 0.0])
    assert np.allclose(result["std"], [1.0, 1.0])
    with pytest.raises(ValueError):
        module.summarize_scaled_training(np.array([]))
    with pytest.raises(ValueError):
        module.summarize_scaled_training(np.array([1.0, 2.0]))


def check_05_train_logistic(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_logistic(X, y)
    assert model.random_state == 42
    assert model.max_iter == 1000
    assert hasattr(model, "coef_")


def check_05_train_logistic_with_strength(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_logistic_with_strength(X, y, 0.5)
    assert model.C == 0.5
    assert model.random_state == 42
    with pytest.raises(ValueError):
        module.train_logistic_with_strength(X, y, 0)


def check_05_logistic_coefficient_table(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = LogisticRegression(max_iter=1000, random_state=42).fit(X, y)
    result = module.logistic_coefficient_table(
        model,
        ["age", "spending", "orders"],
    )
    assert result.columns.tolist() == [
        "feature",
        "coefficient",
        "absolute_coefficient",
    ]
    assert result["absolute_coefficient"].is_monotonic_decreasing
    with pytest.raises(ValueError):
        module.logistic_coefficient_table(model, ["age"])
    with pytest.raises(NotFittedError):
        module.logistic_coefficient_table(
            LogisticRegression(),
            ["a", "b", "c"],
        )


def check_06_train_tree(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_tree(X, y)
    assert model.max_depth == 3
    assert model.random_state == 42
    assert hasattr(model, "tree_")


def check_06_train_tree_with_depth(module: ModuleType) -> None:
    X, y = tiny_classification()
    assert module.train_tree_with_depth(X, y, 1).max_depth == 1
    assert module.train_tree_with_depth(X, y, 5).max_depth == 5
    with pytest.raises(ValueError):
        module.train_tree_with_depth(X, y, 0)


def check_06_tree_importance_table(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
    ).fit(X, y)
    result = module.tree_importance_table(model, ["a", "b", "c"])
    assert result.shape == (3, 2)
    assert result["importance"].is_monotonic_decreasing
    assert result["importance"].sum() == pytest.approx(1.0)
    with pytest.raises(ValueError):
        module.tree_importance_table(model, ["a"])
    with pytest.raises(NotFittedError):
        module.tree_importance_table(DecisionTreeClassifier(), ["a", "b", "c"])


def check_07_train_forest(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_forest(X, y)
    assert model.n_estimators == 50
    assert model.random_state == 42
    assert len(model.estimators_) == 50


def check_07_train_forest_with_estimators(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_forest_with_estimators(X, y, 10)
    assert model.n_estimators == 10
    assert len(model.estimators_) == 10
    with pytest.raises(ValueError):
        module.train_forest_with_estimators(X, y, 0)


def check_07_forest_importance_table(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_forest(X, y)
    result = module.forest_importance_table(model, ["a", "b", "c"])
    assert result.shape == (3, 2)
    assert result["importance"].is_monotonic_decreasing
    assert result["importance"].sum() == pytest.approx(1.0)
    with pytest.raises(ValueError):
        module.forest_importance_table(model, ["a"])


def fitted_logistic() -> tuple[LogisticRegression, np.ndarray, np.ndarray]:
    X, y = tiny_classification()
    model = LogisticRegression(max_iter=1000, random_state=42).fit(X, y)
    return model, X, y


def check_08_predict_labels_and_probabilities(module: ModuleType) -> None:
    model, X, _ = fitted_logistic()
    labels, probabilities = module.predict_labels_and_probabilities(
        model,
        X[:5],
    )
    assert labels.shape == (5,)
    assert probabilities.shape == (5,)
    assert np.all((probabilities >= 0) & (probabilities <= 1))


def check_08_predict_with_threshold(module: ModuleType) -> None:
    model, X, _ = fitted_logistic()
    probabilities = model.predict_proba(X[:5])[:, 1]
    result = module.predict_with_threshold(model, X[:5], 0.5)
    assert np.array_equal(result, (probabilities >= 0.5).astype(int))
    assert set(result).issubset({0, 1})
    with pytest.raises(ValueError):
        module.predict_with_threshold(model, X[:2], -0.1)
    with pytest.raises(ValueError):
        module.predict_with_threshold(model, X[:2], 1.1)


def check_08_build_prediction_table(module: ModuleType) -> None:
    result = module.build_prediction_table(
        ["C1", "C2"],
        np.array([0, 1]),
        np.array([0.2, 0.8]),
    )
    assert result.columns.tolist() == [
        "customer_id",
        "predicted_churn",
        "churn_probability",
    ]
    assert result.to_dict("records")[1] == {
        "customer_id": "C2",
        "predicted_churn": 1,
        "churn_probability": 0.8,
    }
    with pytest.raises(ValueError):
        module.build_prediction_table(
            ["C1"],
            np.array([0, 1]),
            np.array([0.2, 0.8]),
        )


def check_09_calculate_metrics(module: ModuleType) -> None:
    result = module.calculate_metrics(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 1, 1]),
        np.array([0.1, 0.6, 0.7, 0.9]),
    )
    assert set(result) == {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    }
    assert result["accuracy"] == pytest.approx(0.75)
    assert result["recall"] == pytest.approx(1.0)
    with pytest.raises(ValueError):
        module.calculate_metrics(
            np.array([0, 0]),
            np.array([0, 0]),
            np.array([0.1, 0.2]),
        )


def check_09_calculate_threshold_metrics(module: ModuleType) -> None:
    result = module.calculate_threshold_metrics(
        np.array([0, 1, 1]),
        np.array([0.1, 0.4, 0.9]),
        0.5,
    )
    assert result["precision"] == pytest.approx(1.0)
    assert result["recall"] == pytest.approx(0.5)
    zero_result = module.calculate_threshold_metrics(
        np.array([0, 1]),
        np.array([0.1, 0.2]),
        1.0,
    )
    assert zero_result["precision"] == 0.0
    with pytest.raises(ValueError):
        module.calculate_threshold_metrics(
            np.array([0]),
            np.array([0.1]),
            2,
        )


def check_09_calculate_specificity(module: ModuleType) -> None:
    assert module.calculate_specificity(
        np.array([0, 0, 1]),
        np.array([0, 1, 1]),
    ) == pytest.approx(0.5)
    assert module.calculate_specificity(
        np.array([1, 1]),
        np.array([1, 0]),
    ) == 0.0


def check_10_build_confusion_matrix(module: ModuleType) -> None:
    result = module.build_confusion_matrix(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 0, 1]),
    )
    assert np.array_equal(result, np.array([[1, 1], [1, 1]]))
    one_class = module.build_confusion_matrix(
        np.array([0, 0]),
        np.array([0, 0]),
    )
    assert one_class.shape == (2, 2)


def check_10_confusion_counts(module: ModuleType) -> None:
    result = module.confusion_counts(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 0, 1]),
    )
    assert result == {"tn": 1, "fp": 1, "fn": 1, "tp": 1}
    assert module.confusion_counts(
        np.array([0, 1]),
        np.array([0, 1]),
    ) == {"tn": 1, "fp": 0, "fn": 0, "tp": 1}


def check_10_normalized_confusion_matrix(module: ModuleType) -> None:
    result = module.normalized_confusion_matrix(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 1, 1]),
    )
    assert np.allclose(result, [[0.5, 0.5], [0.0, 1.0]])
    one_class = module.normalized_confusion_matrix(
        np.array([0, 0]),
        np.array([0, 0]),
    )
    assert np.allclose(one_class, [[1.0, 0.0], [0.0, 0.0]])


def comparison_split() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X, y = make_classification(
        n_samples=80,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )
    return train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )


def check_11_compare_models(module: ModuleType) -> None:
    result = module.compare_models(*comparison_split())
    assert result.columns.tolist() == ["model", "accuracy", "roc_auc"]
    assert result["model"].tolist() == ["Logistic", "Tree"]
    assert result[["accuracy", "roc_auc"]].apply(
        lambda column: column.between(0, 1).all()
    ).all()


def check_11_rank_models(module: ModuleType) -> None:
    source = pd.DataFrame(
        {
            "model": ["A", "B", "C"],
            "accuracy": [0.7, 0.9, 0.9],
        }
    )
    original = source.copy()
    result = module.rank_models(source, "accuracy")
    assert result["model"].tolist() == ["B", "C", "A"]
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.rank_models(source, "roc_auc")


def check_11_select_best_model_name(module: ModuleType) -> None:
    results = pd.DataFrame(
        {
            "model": ["Logistic", "Tree"],
            "roc_auc": [0.8, 0.7],
        }
    )
    assert module.select_best_model_name(results, "roc_auc") == "Logistic"
    tied = results.assign(roc_auc=[0.8, 0.8])
    assert module.select_best_model_name(tied, "roc_auc") == "Logistic"
    with pytest.raises(ValueError):
        module.select_best_model_name(results.iloc[:0], "roc_auc")


def check_12_compare_train_test_accuracy(module: ModuleType) -> None:
    X_train, X_test, y_train, y_test = comparison_split()
    model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    train_score, test_score = module.compare_train_test_accuracy(
        model,
        X_train,
        X_test,
        y_train,
        y_test,
    )
    assert 0 <= train_score <= 1
    assert 0 <= test_score <= 1


def check_12_detect_overfitting(module: ModuleType) -> None:
    assert module.detect_overfitting(0.95, 0.75, 0.1) is True
    assert module.detect_overfitting(0.85, 0.80, 0.1) is False
    assert module.detect_overfitting(0.9, 0.8, 0.1) is False
    with pytest.raises(ValueError):
        module.detect_overfitting(1.1, 0.8, 0.1)


def check_12_scale_without_leakage(module: ModuleType) -> None:
    train = np.array([[1.0], [2.0], [3.0]])
    test = np.array([[100.0]])
    train_scaled, test_scaled = module.scale_without_leakage(train, test)
    assert train_scaled.mean() == pytest.approx(0.0)
    assert train_scaled.std() == pytest.approx(1.0)
    assert test_scaled[0, 0] > 10


def small_clusters() -> np.ndarray:
    X, _ = make_blobs(
        n_samples=30,
        centers=3,
        cluster_std=0.4,
        random_state=42,
    )
    return X


def check_13_fit_kmeans(module: ModuleType) -> None:
    X = small_clusters()
    model = module.fit_kmeans(X, 3)
    assert model.n_clusters == 3
    assert model.random_state == 42
    assert model.n_init == 10
    assert model.labels_.shape == (30,)
    with pytest.raises(ValueError):
        module.fit_kmeans(X, 0)


def check_13_cluster_customers(module: ModuleType) -> None:
    X = small_clusters()
    labels = module.cluster_customers(X, 3)
    assert labels.shape == (30,)
    assert len(np.unique(labels)) == 3
    repeated = module.cluster_customers(X, 3)
    assert np.array_equal(labels, repeated)


def check_13_cluster_centers_table(module: ModuleType) -> None:
    X = small_clusters()
    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10,
    ).fit(X)
    result = module.cluster_centers_table(
        model,
        ["income", "spending"],
    )
    assert result.shape == (3, 3)
    assert result.columns.tolist() == ["cluster", "income", "spending"]
    assert result["cluster"].tolist() == [0, 1, 2]
    with pytest.raises(ValueError):
        module.cluster_centers_table(model, ["income"])
    with pytest.raises(AttributeError):
        module.cluster_centers_table(
            KMeans(n_clusters=2),
            ["income", "spending"],
        )


def check_14_calculate_inertias(module: ModuleType) -> None:
    X = small_clusters()
    inertias = module.calculate_inertias(X, [2, 3, 4])
    assert len(inertias) == 3
    assert inertias[0] > inertias[1] > inertias[2]
    assert module.calculate_inertias(X, []) == []


def check_14_calculate_inertia_drops(module: ModuleType) -> None:
    assert module.calculate_inertia_drops([100.0, 60.0, 45.0]) == [
        40.0,
        15.0,
    ]
    assert module.calculate_inertia_drops([]) == []
    assert module.calculate_inertia_drops([100.0]) == []
    with pytest.raises(ValueError):
        module.calculate_inertia_drops([10.0, 20.0])
    with pytest.raises(ValueError):
        module.calculate_inertia_drops([10.0, -1.0])


def check_14_build_elbow_table(module: ModuleType) -> None:
    X = small_clusters()
    result = module.build_elbow_table(X, [2, 3])
    assert result.columns.tolist() == ["k", "inertia"]
    assert result["k"].tolist() == [2, 3]
    empty = module.build_elbow_table(X, [])
    assert empty.empty
    assert empty.columns.tolist() == ["k", "inertia"]


def check_15_calculate_silhouette_scores(module: ModuleType) -> None:
    X = small_clusters()
    scores = module.calculate_silhouette_scores(X, [2, 3, 4])
    assert set(scores) == {2, 3, 4}
    assert all(-1 <= score <= 1 for score in scores.values())
    assert scores[3] > scores[2]
    assert module.calculate_silhouette_scores(X, []) == {}


def check_15_select_best_silhouette_k(module: ModuleType) -> None:
    assert module.select_best_silhouette_k({2: 0.4, 3: 0.6}) == 3
    assert module.select_best_silhouette_k({3: 0.5, 2: 0.5}) == 2
    with pytest.raises(ValueError):
        module.select_best_silhouette_k({})


def check_15_build_cluster_evaluation(module: ModuleType) -> None:
    X = small_clusters()
    result = module.build_cluster_evaluation(X, [2, 3, 4])
    assert result.columns.tolist() == ["k", "inertia", "silhouette"]
    assert result["k"].tolist() == [2, 3, 4]
    assert result["silhouette"].between(-1, 1).all()
    empty = module.build_cluster_evaluation(X, [])
    assert empty.empty
    assert empty.columns.tolist() == ["k", "inertia", "silhouette"]


ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_01_select_features_and_label", answer_01, check_01_select_features_and_label),
    ("answer_01_select_mixed_features", answer_01, check_01_select_mixed_features),
    ("answer_01_count_target_classes", answer_01, check_01_count_target_classes),
    ("answer_02_split_data", answer_02, check_02_split_data),
    ("answer_02_split_with_test_size", answer_02, check_02_split_with_test_size),
    ("answer_02_summarize_split_balance", answer_02, check_02_summarize_split_balance),
    ("answer_03_encode_city_feature", answer_03, check_03_encode_city_feature),
    (
        "answer_03_encode_categorical_features",
        answer_03,
        check_03_encode_categorical_features,
    ),
    (
        "answer_03_get_encoded_feature_names",
        answer_03,
        check_03_get_encoded_feature_names,
    ),
    ("answer_04_scale_features", answer_04, check_04_scale_features),
    (
        "answer_04_scale_dataframe_columns",
        answer_04,
        check_04_scale_dataframe_columns,
    ),
    (
        "answer_04_summarize_scaled_training",
        answer_04,
        check_04_summarize_scaled_training,
    ),
    ("answer_05_train_logistic", answer_05, check_05_train_logistic),
    (
        "answer_05_train_logistic_with_strength",
        answer_05,
        check_05_train_logistic_with_strength,
    ),
    (
        "answer_05_logistic_coefficient_table",
        answer_05,
        check_05_logistic_coefficient_table,
    ),
    ("answer_06_train_tree", answer_06, check_06_train_tree),
    ("answer_06_train_tree_with_depth", answer_06, check_06_train_tree_with_depth),
    (
        "answer_06_tree_importance_table",
        answer_06,
        check_06_tree_importance_table,
    ),
    ("answer_07_train_forest", answer_07, check_07_train_forest),
    (
        "answer_07_train_forest_with_estimators",
        answer_07,
        check_07_train_forest_with_estimators,
    ),
    (
        "answer_07_forest_importance_table",
        answer_07,
        check_07_forest_importance_table,
    ),
    (
        "answer_08_predict_labels_and_probabilities",
        answer_08,
        check_08_predict_labels_and_probabilities,
    ),
    ("answer_08_predict_with_threshold", answer_08, check_08_predict_with_threshold),
    (
        "answer_08_build_prediction_table",
        answer_08,
        check_08_build_prediction_table,
    ),
    ("answer_09_calculate_metrics", answer_09, check_09_calculate_metrics),
    (
        "answer_09_calculate_threshold_metrics",
        answer_09,
        check_09_calculate_threshold_metrics,
    ),
    (
        "answer_09_calculate_specificity",
        answer_09,
        check_09_calculate_specificity,
    ),
    ("answer_10_build_confusion_matrix", answer_10, check_10_build_confusion_matrix),
    ("answer_10_confusion_counts", answer_10, check_10_confusion_counts),
    (
        "answer_10_normalized_confusion_matrix",
        answer_10,
        check_10_normalized_confusion_matrix,
    ),
    ("answer_11_compare_models", answer_11, check_11_compare_models),
    ("answer_11_rank_models", answer_11, check_11_rank_models),
    (
        "answer_11_select_best_model_name",
        answer_11,
        check_11_select_best_model_name,
    ),
    (
        "answer_12_compare_train_test_accuracy",
        answer_12,
        check_12_compare_train_test_accuracy,
    ),
    ("answer_12_detect_overfitting", answer_12, check_12_detect_overfitting),
    (
        "answer_12_scale_without_leakage",
        answer_12,
        check_12_scale_without_leakage,
    ),
    ("answer_13_fit_kmeans", answer_13, check_13_fit_kmeans),
    ("answer_13_cluster_customers", answer_13, check_13_cluster_customers),
    (
        "answer_13_cluster_centers_table",
        answer_13,
        check_13_cluster_centers_table,
    ),
    ("answer_14_calculate_inertias", answer_14, check_14_calculate_inertias),
    (
        "answer_14_calculate_inertia_drops",
        answer_14,
        check_14_calculate_inertia_drops,
    ),
    ("answer_14_build_elbow_table", answer_14, check_14_build_elbow_table),
    (
        "answer_15_calculate_silhouette_scores",
        answer_15,
        check_15_calculate_silhouette_scores,
    ),
    (
        "answer_15_select_best_silhouette_k",
        answer_15,
        check_15_select_best_silhouette_k,
    ),
    (
        "answer_15_build_cluster_evaluation",
        answer_15,
        check_15_build_cluster_evaluation,
    ),
]


practice_modules = [
    module
    for module in [
        practice_01,
        practice_02,
        practice_03,
        practice_04,
        practice_05,
        practice_06,
        practice_07,
        practice_08,
        practice_09,
        practice_10,
        practice_11,
        practice_12,
        practice_13,
        practice_14,
        practice_15,
    ]
    for _ in range(3)
]

PRACTICE_CASES: list[tuple[str, ModuleType, Check]] = [
    (name.replace("answer_", "practice_"), practice, check)
    for (name, _, check), practice in zip(ANSWER_CASES, practice_modules)
]


@pytest.mark.parametrize(
    ("name", "module", "check"),
    ANSWER_CASES,
    ids=[case[0] for case in ANSWER_CASES],
)
def test_answer_contract(
    name: str,
    module: ModuleType,
    check: Check,
) -> None:
    check(module)


@pytest.mark.parametrize(
    ("name", "module", "check"),
    PRACTICE_CASES,
    ids=[case[0] for case in PRACTICE_CASES],
)
def test_practice_contract(
    name: str,
    module: ModuleType,
    check: Check,
) -> None:
    try:
        check(module)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
