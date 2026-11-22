from typing import get_args

import pytest

from nomenclature.target import (
    Feature,
    Target,
    TargetFeatureMapping,
    get_target_features,
    validate_target_features,
)


def test_target_feature_mapping():
    for target, features in TargetFeatureMapping.items():
        assert target in get_args(Target)

        for feature in features:
            assert feature in get_args(Feature)


def test_get_target_features_invalid():
    with pytest.raises(ValueError, match="Invalid target thing"):
        get_target_features("thing")

    with pytest.raises(ValueError, match="Invalid target marsss"):
        get_target_features("marsss")

    # lowercase message
    with pytest.raises(ValueError, match="Invalid target europe"):
        get_target_features("Europe")


def test_get_target_features_valid():

    bennu = ["crater", "regio", "saxum"]
    europa = [
        "cavus",
        "chaos",
        "crater",
        "flexus",
        "fossa",
        "large ringed feature",
        "linea",
        "macula",
        "mensa",
        "regio",
    ]

    assert bennu == get_target_features("bennu")
    assert europa == get_target_features("europa")


def test_get_target_features_code():

    miranda = ["CR", "AA", "RE", "RU", "SU"]

    assert miranda == get_target_features("miranda", code=True)


def test_get_target_features_convert_str():
    titania = ["chasma", "crater", "rupes"]

    assert titania == get_target_features("titania")
    assert titania == get_target_features("tiTanIa")
    assert titania == get_target_features("TITANIA")
    assert titania == get_target_features("Titania")


def test_validate_target_features():

    mars_error = validate_target_features(
        "mars", ["chaos", "crater", "sinus", "satellite feature"]
    )

    mars_valid = validate_target_features("mars", ["chasma", "crater", "chaos"])

    assert set(mars_error) == {
        "sinus",
        "satellite feature",
    }  # set to solve testing sorting issues

    assert mars_valid == []  # empty if valid
