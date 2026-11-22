"""Process target requests."""

import csv
from collections import defaultdict
from pathlib import Path
from typing import Literal, get_args

Target = Literal[
    "amalthea",
    "ariel",
    "arrokoth",
    "bennu",
    "callisto",
    "ceres",
    "charon",
    "dactyl",
    "deimos",
    "didymos",
    "dimorphos",
    "dinkinesh",
    "dione",
    "donaldjohanson",
    "enceladus",
    "eros",
    "epimetheus",
    "europa",
    "ganymede",
    "gaspra",
    "hyperion",
    "iapetus",
    "ida",
    "io",
    "itokawa",
    "janus",
    "lutetia",
    "mars",
    "mathilde",
    "mercury",
    "mimas",
    "miranda",
    "moon",
    "nix",
    "oberon",
    "phobos",
    "phoebe",
    "pluto",
    "proteus",
    "puck",
    "rhea",
    "ryugu",
    "selam",
    "steins",
    "tethys",
    "thebe",
    "titan",
    "titania",
    "triton",
    "umbriel",
    "venus",
    "vesta",
]

Feature = Literal[
    "albedo feature",
    "arcus",
    "astronaut-named features",
    "astrum",
    "catena",
    "cavus",
    "chaos",
    "chasma",
    "collis",
    "collum",
    "corona",
    "crater",
    "dorsum",
    "eruptive center",
    "facula",
    "farrum",
    "flexus",
    "fluctus",
    "flumen",
    "fossa",
    "fretum",
    "insula",
    "labes",
    "labyrinthius",
    "lacuna",
    "lacus",
    "large ringed feature",
    "linea",
    "lingula",
    "lobus",
    "macula",
    "mare",
    "mensa",
    "mons",
    "oceanus",
    "palus",
    "patera",
    "planitia",
    "planum",
    "plume",
    "promontorium",
    "regio",
    "reticulum",
    "rima",
    "rupes",
    "satellite feature",
    "saxum",
    "scopulus",
    "serpens",
    "sinus",
    "statio",
    "sulcus",
    "terra",
    "tessera",
    "tholus",
    "unda",
    "vallis",
    "vastitas",
    "virga",
]

FeatureCode = Literal[
    "AL",
    "AR",
    "LF",
    "AS",
    "CA",
    "CB",
    "CH",
    "CM",
    "CO",
    "CL",
    "CR",
    "AA",
    "DO",
    "ER",
    "FA",
    "FR",
    "FE",
    "FL",
    "FM",
    "FO",
    "FT",
    "IN",
    "LA",
    "LB",
    "LU",
    "LC",
    "LG",
    "LI",
    "LN",
    "LO",
    "MA",
    "ME",
    "MN",
    "MO",
    "OC",
    "PA",
    "PE",
    "PL",
    "PM",
    "PU",
    "PR",
    "RE",
    "RT",
    "RI",
    "RU",
    "SF",
    "SA",
    "SC",
    "SE",
    "SI",
    "ST",
    "SU",
    "TA",
    "TE",
    "TH",
    "UN",
    "VA",
    "VS",
    "VI",
]

FeatureCodeMapping: dict[Feature, FeatureCode] = {
    "albedo feature": "AL",
    "arcus": "AR",
    "astronaut-named features": "LF",
    "astrum": "AS",
    "catena": "CA",
    "cavus": "CB",
    "chaos": "CH",
    "chasma": "CM",
    "collis": "CO",
    "collum": "CL",
    "corona": "CR",
    "crater": "AA",
    "dorsum": "DO",
    "eruptive center": "ER",
    "facula": "FA",
    "farrum": "FR",
    "flexus": "FE",
    "fluctus": "FL",
    "flumen": "FM",
    "fossa": "FO",
    "fretum": "FT",
    "insula": "IN",
    "labes": "LA",
    "labyrinthius": "LB",
    "lacuna": "LU",
    "lacus": "LC",
    "large ringed feature": "LG",
    "linea": "LI",
    "lingula": "LN",
    "lobus": "LO",
    "macula": "MA",
    "mare": "ME",
    "mensa": "MN",
    "mons": "MO",
    "oceanus": "OC",
    "palus": "PA",
    "patera": "PE",
    "planitia": "PL",
    "planum": "PM",
    "plume": "PU",
    "promontorium": "PR",
    "regio": "RE",
    "reticulum": "RT",
    "rima": "RI",
    "rupes": "RU",
    "satellite feature": "SF",
    "saxum": "SA",
    "scopulus": "SC",
    "serpens": "SE",
    "sinus": "SI",
    "statio": "ST",
    "sulcus": "SU",
    "terra": "TA",
    "tessera": "TE",
    "tholus": "TH",
    "unda": "UN",
    "vallis": "VA",
    "vastitas": "VS",
    "virga": "VI",
}


# uses Feature for readability rather than FeatureCode
TargetFeatureMapping: dict[Target, list[Feature]] = {
    "mercury": [
        "albedo feature",
        "catena",
        "crater",
        "dorsum",
        "facula",
        "fossa",
        "mons",
        "planitia",
        "planum",
        "rupes",
        "vallis",
    ],  # interactive
    "venus": [
        "chasma",
        "collis",
        "corona",
        "crater",
        "dorsum",
        "farrum",
        "fluctus",
        "fossa",
        "labyrinthius",
        "linea",
        "mons",
        "patera",
        "planitia",
        "planum",
        "regio",
        "rupes",
        "terra",
        "tessera",
        "tholus",
        "unda",
        "vallis",
    ],  # interactive
    "moon": [
        "albedo feature",
        "astronaut-named features",
        "catena",
        "crater",
        "dorsum",
        "fossa",
        "lacus",
        "mare",
        "mons",
        "oceanus",
        "palus",
        "planitia",
        "promontorium",
        "rima",
        "rupes",
        "satellite feature",
        "sinus",
        "statio",
        "vallis",
    ],  # interactive
    # mars
    "mars": [
        "albedo feature",
        "catena",
        "cavus",
        "chaos",
        "chasma",
        "collis",
        "crater",
        "dorsum",
        "fluctus",
        "fossa",
        "labes",
        "labyrinthius",
        "lingula",
        "macula",
        "mensa",
        "mons",
        "palus",
        "patera",
        "planitia",
        "planum",
        "rupes",
        "scopulus",
        "serpens",
        "sulcus",
        "terra",
        "tholus",
        "unda",
        "vallis",
        "vastitas",
    ],  # interactive
    "phobos": ["crater", "dorsum", "planitia", "regio"],
    "deimos": ["crater"],
    # asteroid belt
    "arrokoth": ["arcus", "collum", "crater", "linea", "lobus"],
    "bennu": ["crater", "regio", "saxum"],
    "ceres": [
        "catena",
        "crater",
        "facula",
        "fossa",
        "labes",
        "labyrinthius",
        "mons",
        "planitia",
        "planum",
        "regio",
        "rupes",
        "sulcus",
        "tholus",
    ],  # interactive
    "dinkinesh": ["dorsum", "fossa", "saxum"],
    "selam": ["dorsum", "lobus"],
    "didymos": ["saxum"],
    "dimorphos": ["crater", "saxum"],
    "donaldjohanson": ["collum", "crater", "dorsum", "lobus", "regio", "saxum"],
    "eros": ["crater", "dorsum", "regio"],
    "gaspra": ["crater", "regio"],
    "ida": ["crater", "dorsum", "regio"],
    "dactyl": ["crater"],
    "itokawa": ["crater", "regio"],
    "lutetia": ["crater", "dorsum", "fossa", "labes", "regio", "rima", "rupes"],
    "mathilde": ["crater"],
    "ryugu": ["crater", "dorsum", "fossa", "saxum"],  # interactive
    "steins": ["crater", "regio"],
    "vesta": [
        "catena",
        "crater",
        "dorsum",
        "fossa",
        "planitia",
        "rupes",
        "terra",
        "tholus",
    ],  # interactive
    # jupiter
    "amalthea": ["crater", "facula"],
    "thebe": ["crater"],
    "io": [
        "eruptive center",
        "fluctus",
        "mensa",
        "mons",
        "patera",
        "planum",
        "regio",
        "tholus",
        "vallis",
    ],  # interactive
    "europa": [
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
    ],
    "ganymede": [
        "catena",
        "crater",
        "facula",
        "fossa",
        "patera",
        "regio",
        "sulcus",
    ],  # interactive
    "callisto": ["catena", "crater", "facula", "large ringed feature"],
    # saturn
    "epimetheus": ["crater"],
    "janus": ["crater"],
    "mimas": ["catena", "chasma", "crater"],
    "enceladus": [
        "crater",
        "dorsum",
        "fossa",
        "planitia",
        "rupes",
        "sulcus",
    ],  # interactive
    "tethys": ["chasma", "crater", "mons"],
    "dione": ["catena", "chasma", "crater", "dorsum", "fossa", "linea"],
    "rhea": ["catena", "chasma", "crater", "fossa", "linea"],
    "titan": [
        "albedo feature",
        "arcus",
        "collis",
        "crater",
        "facula",
        "fluctus",
        "flumen",
        "fretum",
        "insula",
        "labyrinthius",
        "lacuna",
        "lacus",
        "large ringed feature",
        "macula",
        "mare",
        "mons",
        "patera",
        "planitia",
        "regio",
        "sinus",
        "terra",
        "unda",
        "virga",
    ],  # interactive
    "hyperion": ["crater", "dorsum"],
    "iapetus": ["crater", "mons", "regio", "terra"],
    "phoebe": ["crater", "regio"],
    # uranus
    "puck": ["crater"],
    "miranda": ["corona", "crater", "regio", "rupes", "sulcus"],
    "ariel": ["chasma", "crater", "vallis"],
    "umbriel": ["crater"],
    "titania": ["chasma", "crater", "rupes"],
    "oberon": ["chasma", "crater"],
    # neptune
    "proteus": ["crater"],
    "triton": [
        "catena",
        "cavus",
        "crater",
        "dorsum",
        "fossa",
        "macula",
        "patera",
        "planitia",
        "planum",
        "plume",
        "regio",
        "sulcus",
    ],
    # pluto
    "pluto": [
        "cavus",
        "collis",
        "crater",
        "dorsum",
        "fossa",
        "lacus",
        "linea",
        "mons",
        "palus",
        "planitia",
        "regio",
        "rupes",
        "terra",
        "vallis",
    ],  # interactive
    "charon": ["chasma", "crater", "dorsum", "mons", "regio"],  # interactive
    "nix": ["crater"],
}


def get_target_features(target: Target) -> list[Feature]:
    """
    Get a list of features by target.

    Args:
        target: A nomenclature target.

    Returns:
        List of feature types.

    Raises:
        ValueError: Raised if `target` is not a valid Gazetteer target.

    """
    if target.lower() not in get_args(Target):
        msg = f"Invalid target {target.lower()}"
        raise ValueError(msg)

    features = TargetFeatureMapping.get(target.lower())

    if not features:
        msg = f"Invalid target {target.lower()}"
        raise ValueError(msg)

    return features


def get_target_features_code(target: Target) -> list[FeatureCode]:
    """
    Get a list of feature codes by target.

    Args:
        target: A nomenclature target.

    Returns:
        List of feature type codes.

    Raises:
        ValueError: Raised if `target` is not a valid Gazetteer target.

    """
    if target.lower() not in get_args(Target):
        msg = f"Invalid target {target.lower()}"
        raise ValueError(msg)

    features = TargetFeatureMapping.get(target.lower())

    if not features:
        msg = f"Invalid target {target.lower()}"
        raise ValueError(msg)

    return [FeatureCodeMapping[feature] for feature in features]


def validate_target_features(target: Target, features: list[Feature]) -> list[str]:
    """
    Validate that supplied features are available on a target.

    Args:
        target: Target to validate.
        features: List of features to check on a target.

    Returns:
        List of non-validated features if found or an empty list otherwise.

    """
    target_features = get_target_features(target)

    return list(set(features) - set(target_features))


def lookup_feature_id(
    target: Target, features: list[Feature]
) -> dict[Feature, dict[str, int]]:
    """
    Parse the CSV lookup table to find the GPN ID for a target's requested features.

    Args:
        target: Target.
        features: Features to parse for their ID.

    Returns:
        Lookup table containing the features, names, and IDs,
        e.g. {"unda": {"abalos undae": 5, ...}, "chaos": {...}, ...}

    """
    feature_codes = [FeatureCodeMapping[feature] for feature in features]

    # invert to convert code back to full name
    code_feature_lookup = {v: k for k, v in FeatureCodeMapping.items()}

    root_dir = Path(Path(Path(__file__).resolve()).parent)
    lookup_file = root_dir / Path("./lookup_tables/lookup.csv")

    # tell ty what we expect the dict to look like
    requested_features: dict[Feature, dict[str, int]] = defaultdict(dict)
    with lookup_file.open(encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)

        for row in csv_reader:
            # skip row if not on target or desired feature type
            if row["t_name"].lower() != target or row["f_code"] not in set(
                feature_codes
            ):
                continue

            requested_features[code_feature_lookup[row["f_code"]]].update(
                {row["f_name"].lower(): int(row["f_id"])}
            )

    return requested_features
