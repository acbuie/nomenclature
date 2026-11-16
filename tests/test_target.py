from typing import get_args

import pytest

from nomenclature.target import (
    Feature,
    Target,
    TargetFeatureMapping,
    get_target_features,
)


def test_target_feature_mapping():
    for target, features in TargetFeatureMapping.items():
        assert target in get_args(Target)

        for feature in features:
            assert feature in get_args(Feature)


def test_get_target_features_invalid():
    with pytest.raises(ValueError, match="Invalid target thing"):
        get_target_features("thing")

    with pytest.raises(ValueError, match="Invalid target Marsss"):
        get_target_features("Marsss")


def test_get_target_features_valid():

    bennu = ["Crater", "Regio", "Saxum"]
    europa = [
        "Cavus",
        "Chaos",
        "Crater",
        "Flexus",
        "Fossa",
        "Large ringed feature",
        "Linea",
        "Macula",
        "Mensa",
        "Regio",
    ]

    assert bennu == get_target_features("Bennu")
    assert europa == get_target_features("Europa")
