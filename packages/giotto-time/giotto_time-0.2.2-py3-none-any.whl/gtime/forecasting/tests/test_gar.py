import itertools
import random
from typing import List

import numpy as np
import pandas as pd
from hypothesis.strategies import data, integers, lists, text
import hypothesis.strategies as st
from numpy.testing import assert_array_equal

from gtime.explainability import _ShapExplainer
from gtime.explainability.tests.test_explainer import models
from gtime.forecasting.gar import MultiFeatureGAR, initialize_estimator
from gtime.regressors import ExplainableRegressor

if pd.__version__ >= "1.0.0":
    import pandas._testing as testing
else:
    import pandas.util.testing as testing

import pytest
from hypothesis import given, assume
from sklearn.compose import make_column_selector
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression

from gtime.compose import FeatureCreation
from gtime.feature_extraction import MovingAverage, Shift
from gtime.feature_generation import Constant
from gtime.forecasting import GAR, GARFF
from gtime.model_selection import FeatureSplitter
from gtime.utils.hypothesis.feature_matrices import (
    X_y_matrices,
    X_matrices,
)
from gtime.utils.fixtures import estimator

df_transformer = FeatureCreation(
    [
        ("shift_0", Shift(0), make_column_selector(dtype_include=np.number)),
        ("shift_1", Shift(1), make_column_selector(dtype_include=np.number)),
        (
            "moving_average_3",
            MovingAverage(window_size=3),
            make_column_selector(dtype_include=np.number),
        ),
    ]
)


forecasters = [GAR, GARFF, MultiFeatureGAR]
explainers = [
    "shap",
]  # "lime"] for speed reason


@pytest.fixture
def time_series():
    testing.N, testing.K = 200, 1
    return testing.makeTimeDataFrame(freq="MS")


def arbitrary_features(feature_length):
    possible_features = [MovingAverage, Constant, Shift]
    random_features = []
    random_params = random.sample(range(1, 100), feature_length)

    feature_names = []
    for random_param in random_params:
        random_feature = random.sample(possible_features, 1)[0]
        output_name = f"{random_feature}_{random_params}"
        if output_name in feature_names:
            continue
        feature_names.append(output_name)
        feature = random_feature(random_param)
        random_features.append(feature)

    return random_features, feature_names


@st.composite
def str_target_to_feature_dicts(
    draw,
    targets: List[str],
    features: List[str],
    min_features_per_target: int = 1,
    max_features_per_target: int = None,
):
    if max_features_per_target is None:
        max_features_per_target = len(features)
    target_to_feature_dict = {}
    for target in targets:
        n_target_features = draw(
            integers(min_features_per_target, max_features_per_target)
        )
        target_features = sorted(
            np.random.choice(len(features), n_target_features, replace=False)
        )
        target_features = [features[i] for i in target_features]
        target_to_feature_dict[target] = target_features
    return target_to_feature_dict


def feature_names():
    return text(min_size=1, max_size=12)


@given(
    data=data(),
    targets=lists(feature_names(), unique=True, min_size=1, max_size=10),
    features=lists(feature_names(), unique=True, min_size=1, max_size=10),
    min_features_per_target=integers(1, 4),
    max_features_per_target=integers(5, 10),
)
def test_str_target_to_feature_dicts(
    data, targets, features, min_features_per_target, max_features_per_target
):
    assume(min_features_per_target <= len(targets))
    assume(max_features_per_target <= len(features))
    target_to_feature_dict = data.draw(
        str_target_to_feature_dicts(
            targets, features, min_features_per_target, max_features_per_target
        )
    )
    assert len(target_to_feature_dict) == len(targets)
    for target, target_features in target_to_feature_dict.items():
        assert all([feature in features for feature in target_features])
        assert len(set(target_features)) == len(target_features)
        assert (
            min_features_per_target <= len(target_features) <= max_features_per_target
        )


@given(models())
def test_initialize_estimator(estimator):
    assert estimator == initialize_estimator(estimator, explainer_type=None)


@given(models())
def test_initialize_estimator_explainable(estimator):
    explainable_estimator = initialize_estimator(estimator, explainer_type="shap")
    assert isinstance(explainable_estimator, ExplainableRegressor)
    assert isinstance(explainable_estimator.explainer, _ShapExplainer)


class TestAll:
    @pytest.mark.parametrize(
        "forecaster,explainer", itertools.product(forecasters, explainers)
    )
    @given(
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        )
    )
    def test_predict_has_explainers(self, forecaster, explainer, X_y):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        model = forecaster(LinearRegression(), explainer_type=explainer)
        model.fit(X_train, y_train)
        model.predict(X_test.iloc[:1, :])
        assert len(model.estimators_) == y_test.shape[1]
        for estimator in model.estimators_:
            assert len(estimator.explainer_.explanations_) == 1

    @pytest.mark.parametrize(
        "forecaster,explainer", itertools.product(forecasters, explainers)
    )
    @given(
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        )
    )
    def test_explanations_columns(self, forecaster, explainer, X_y):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        model = forecaster(LinearRegression(), explainer_type=explainer)
        model.fit(X_train, y_train)
        model.predict(X_test.iloc[:1, :])
        for target_column, explanation in model.explanations_.items():
            assert set(explanation.columns).issuperset(set(X_train.columns))

        assert set(model.explanations_.keys()) == set(y_train.columns)


class TestMultiFeatureGAR:
    def test_constructor(self, estimator):
        multi_feature_gar = MultiFeatureGAR(estimator)
        assert multi_feature_gar.n_jobs == 1

    @pytest.mark.parametrize(
        "X_columns, y_columns, target_to_feature_dict, expected",
        [
            (
                ["a", "b", "c"],
                ["d", "e"],
                {"d": ["a", "b"], "e": ["b", "c"]},
                {0: [0, 1], 1: [1, 2]},
            ),
            (
                ["a", "b", "c"],
                ["d", "e"],
                {"d": ["a", "b"], "e": ["a"]},
                {0: [0, 1], 1: [0]},
            ),
        ],
    )
    def test_feature_name_to_index(
        self, X_columns, y_columns, target_to_feature_dict, expected
    ):
        computed = MultiFeatureGAR._feature_name_to_index(
            target_to_feature_dict, X_columns, y_columns
        )
        for key, value in computed.items():
            assert_array_equal(value, expected[key])

    @pytest.mark.parametrize(
        "X_columns, y_columns, target_to_feature_dict, expected",
        [
            (
                ["a", "b", "c"],
                ["d", "e"],
                {"d": ["a", "b"], "e": ["b", "d"]},
                {0: [0, 1], 1: [1, 2]},
            ),
        ],
    )
    def test_key_error_feature_name_to_index(
        self, X_columns, y_columns, target_to_feature_dict, expected
    ):
        with pytest.raises(KeyError):
            MultiFeatureGAR._feature_name_to_index(
                target_to_feature_dict, X_columns, y_columns
            )

    @given(
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        )
    )
    def test_fit_as_multi_output_regressor_if_target_to_feature_none(
        self, estimator, X_y
    ):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        multi_feature_gar = MultiFeatureGAR(estimator)
        multi_feature_gar.fit(X_train, y_train)

        gar = GAR(estimator)
        gar.fit(X_train, y_train)

        pd.testing.assert_frame_equal(
            multi_feature_gar.predict(X_test), gar.predict(X_test),
        )

    @given(X=X_matrices(df_transformer=df_transformer))
    def test_error_predict_with_no_fit(self, estimator, X):
        regressor = MultiFeatureGAR(estimator)
        with pytest.raises(NotFittedError):
            regressor.predict(X)

    @given(
        data=data(),
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        ),
    )
    def test_fit_target_to_feature_dict_working(self, data, X_y, estimator):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        target_to_feature_dict = data.draw(
            str_target_to_feature_dicts(targets=y.columns, features=X.columns)
        )
        multi_feature_gar = MultiFeatureGAR(
            estimator, target_to_features_dict=target_to_feature_dict
        )
        multi_feature_gar.fit(X_train, y_train)

    @given(
        data=data(),
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        ),
    )
    def test_fit_target_to_feature_dict_consistent(self, data, X_y, estimator):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        target_to_feature_dict = data.draw(
            str_target_to_feature_dicts(targets=y.columns, features=X.columns)
        )
        multi_feature_gar = MultiFeatureGAR(
            estimator, target_to_features_dict=target_to_feature_dict
        )
        multi_feature_gar.fit(X_train, y_train)
        for i, estimator_ in enumerate(multi_feature_gar.estimators_):
            expected_n_features = len(target_to_feature_dict[y.columns[i]])
            assert len(estimator_.coef_) == expected_n_features

    @given(
        data=data(),
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        ),
    )
    def test_fit_target_to_feature_dict_set_after_consistent(
        self, data, X_y, estimator
    ):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        target_to_feature_dict = data.draw(
            str_target_to_feature_dicts(targets=y.columns, features=X.columns)
        )
        multi_feature_gar = MultiFeatureGAR(
            estimator, target_to_features_dict=target_to_feature_dict
        )
        multi_feature_gar.target_to_features_dict = target_to_feature_dict
        multi_feature_gar.fit(X_train, y_train)
        for i, estimator_ in enumerate(multi_feature_gar.estimators_):
            expected_n_features = len(target_to_feature_dict[y.columns[i]])
            assert len(estimator_.coef_) == expected_n_features

    @given(
        data=data(),
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        ),
    )
    def test_predict_target_to_feature_dict(self, data, X_y, estimator):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        target_to_feature_dict = data.draw(
            str_target_to_feature_dicts(targets=y.columns, features=X.columns)
        )
        multi_feature_gar = MultiFeatureGAR(estimator)
        multi_feature_gar.target_to_features_dict = target_to_feature_dict
        multi_feature_gar.fit(X_train, y_train)
        multi_feature_gar.predict(X_test)

    @given(
        data=data(),
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        ),
    )
    def test_predict_target_to_feature_dict_explainable(self, data, X_y, estimator):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        target_to_feature_dict = data.draw(
            str_target_to_feature_dicts(targets=y.columns, features=X.columns)
        )
        multi_feature_gar = MultiFeatureGAR(estimator, explainer_type="shap")
        multi_feature_gar.target_to_features_dict = target_to_feature_dict
        multi_feature_gar.fit(X_train, y_train)
        multi_feature_gar.predict(X_test)

    @given(
        data=data(),
        X_y=X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            min_length=10,
            allow_nan_infinity=False,
        ),
    )
    def test_error_predict_target_to_feature_dict_wrong_X_shape(
        self, data, X_y, estimator
    ):
        X, y = X_y
        X_train, y_train, X_test, y_test = FeatureSplitter().transform(X, y)
        target_to_feature_dict = data.draw(
            str_target_to_feature_dicts(targets=y.columns, features=X.columns)
        )
        multi_feature_gar = MultiFeatureGAR(
            estimator, target_to_features_dict=target_to_feature_dict
        )
        multi_feature_gar.fit(X_train, y_train)
        X_test = X_test.iloc[:, :2]
        with pytest.raises(ValueError):
            multi_feature_gar.predict(X_test)


class TestFitPredict:
    def test_predict_with_no_fit(self, time_series):
        base_model = LinearRegression()

        gar_no_feedforward = GAR(estimator=base_model)

        with pytest.raises(NotFittedError):
            gar_no_feedforward.predict(time_series)

    @given(
        X_y_matrices(
            horizon=4,
            df_transformer=df_transformer,
            allow_nan_infinity=False,
            min_length=10,
        )
    )
    def test_correct_fit_date(self, X_y):
        base_model = LinearRegression()
        feature_splitter = FeatureSplitter()
        x, y = X_y[0], X_y[1]
        x_train, y_train, x_test, y_test = feature_splitter.transform(x, y)

        gar_no_feedforward = GAR(estimator=base_model)

        gar_no_feedforward.fit(x_train, y_train)

        predictions = gar_no_feedforward.predict(x_test)

        assert len(predictions) == len(x_test)
        np.testing.assert_array_equal(predictions.index, x_test.index)

        gar_with_feedforward = GARFF(estimator=base_model)

        gar_with_feedforward.fit(x_train, y_train)

        predictions = gar_with_feedforward.predict(x_test)

        assert len(predictions) == len(x_test)
        np.testing.assert_array_equal(predictions.index, x_test.index)
