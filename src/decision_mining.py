"""
Decision mining: train classifiers on XOR gateway decisions.

For each XOR split in the Petri net we identify the *labeled* outgoing
transitions (silent / tau transitions are grouped together as the "skip"
branch). For each case we determine which branch was taken by checking
whether any of the labeled activities appears in the trace. We then train
a decision tree on case-level attributes to predict that choice.

This is a trace-level approximation of the alignment-based approach in
de Leoni and van der Aalst (2013). For the IMf model used here, every
XOR is "labeled activity vs. skip", so the decision is binary.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

from src.config import ACTIVITY_COL, CASE_COL, SEED

SKIP_LABEL = "__skip__"


def find_xor_splits(net) -> list:
    """Places in the Petri net with more than one outgoing arc."""
    return [p for p in net.places if len(p.out_arcs) > 1]


def prepare_case_features(log: pd.DataFrame) -> pd.DataFrame:
    """Build an encoded feature matrix at the case level."""
    case_features = log.groupby(CASE_COL).first()[
        ["case:LoanGoal", "case:ApplicationType", "case:RequestedAmount"]
    ]
    return pd.get_dummies(
        case_features,
        columns=["case:LoanGoal", "case:ApplicationType"],
        drop_first=True,
    )


def mine_decisions(
    log: pd.DataFrame,
    net,
    min_cases: int = 100,
    max_depth: int = 4,
) -> dict:
    """
    For each XOR split that has at least one labeled outgoing transition,
    train a decision tree on case attributes to predict which branch was
    taken (labeled activity vs. skip).
    """
    xor_places = find_xor_splits(net)
    case_features = prepare_case_features(log)
    case_activities = log.groupby(CASE_COL)[ACTIVITY_COL].apply(set)

    results = {}

    for i, place in enumerate(xor_places):
        out_transitions = [arc.target for arc in place.out_arcs]
        labels = {t.label for t in out_transitions if t.label is not None}
        has_skip = any(t.label is None for t in out_transitions)

        if not labels:
            continue

        decisions = {}
        for case_id, acts in case_activities.items():
            fired = acts & labels
            if fired:
                decisions[case_id] = next(iter(fired)) if len(fired) == 1 else "__multi__"
            elif has_skip:
                decisions[case_id] = SKIP_LABEL

        if len(decisions) < min_cases:
            continue

        df = case_features.join(
            pd.Series(decisions, name="decision"), how="inner"
        ).dropna()

        if df["decision"].nunique() < 2:
            continue

        X = df.drop(columns=["decision"])
        y = df["decision"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=SEED, stratify=y
        )

        clf = DecisionTreeClassifier(max_depth=max_depth, random_state=SEED)
        clf.fit(X_train, y_train)

        key = f"XOR_{i + 1}"
        results[key] = {
            "place": place.name,
            "labeled_branches": sorted(labels),
            "has_skip_branch": has_skip,
            "n_cases": len(df),
            "class_distribution": {k: int(v) for k, v in y.value_counts().items()},
            "train_accuracy": float(clf.score(X_train, y_train)),
            "test_accuracy": float(clf.score(X_test, y_test)),
            "tree_text": export_text(clf, feature_names=list(X.columns), max_depth=3),
            "classifier": clf,
            "features": list(X.columns),
        }

        print(
            f"{key} place={place.name} "
            f"labels={sorted(labels)} n={len(df)} "
            f"train={clf.score(X_train, y_train):.3f} "
            f"test={clf.score(X_test, y_test):.3f}"
        )

    return results
