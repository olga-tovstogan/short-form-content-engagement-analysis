"""Reproduce the core product-engagement analysis and charts.

Run from the repository root:
    python src/analysis.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
IMAGES = ROOT / "images"
IMAGES.mkdir(exist_ok=True)


def load_events() -> pd.DataFrame:
    """Load and validate the synthetic event-level dataset."""
    events = pd.read_csv(
        DATA / "synthetic_user_events.csv", parse_dates=["event_date"]
    )
    required = {
        "event_id", "content_category", "video_length_seconds",
        "watch_time_seconds", "watch_ratio", "completed_video",
        "quick_swipe", "liked", "shared", "followed_creator",
        "rewatched", "negative_feedback", "continued_session",
    }
    missing = required.difference(events.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    return events


def category_scorecard(events: pd.DataFrame) -> pd.DataFrame:
    """Aggregate attention, intent, and satisfaction signals by category."""
    return (
        events.groupby("content_category")
        .agg(
            views=("event_id", "size"),
            avg_watch_seconds=("watch_time_seconds", "mean"),
            avg_watch_ratio=("watch_ratio", "mean"),
            completion_rate=("completed_video", "mean"),
            quick_swipe_rate=("quick_swipe", "mean"),
            like_rate=("liked", "mean"),
            share_rate=("shared", "mean"),
            follow_rate=("followed_creator", "mean"),
            rewatch_rate=("rewatched", "mean"),
            negative_feedback_rate=("negative_feedback", "mean"),
            session_continuation_rate=("continued_session", "mean"),
        )
        .sort_values("avg_watch_ratio", ascending=False)
    )


def signal_model(events: pd.DataFrame) -> pd.Series:
    """Estimate diagnostic associations with session continuation.

    Coefficients are descriptive and are not interpreted as causal effects.
    """
    features = [
        "watch_ratio", "completed_video", "quick_swipe", "liked", "shared",
        "followed_creator", "rewatched", "negative_feedback",
    ]
    model = make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=1000, random_state=2027)
    )
    model.fit(events[features], events["continued_session"])
    return pd.Series(
        model.named_steps["logisticregression"].coef_[0], index=features
    ).sort_values()


def create_charts(events: pd.DataFrame, metrics: pd.DataFrame) -> None:
    """Create portfolio-ready figures."""
    plt.style.use("seaborn-v0_8-whitegrid")
    cyan, pink = "#25F4EE", "#FE2C55"

    ordered = metrics.sort_values("avg_watch_ratio")
    fig, ax = plt.subplots(figsize=(9, 5.3))
    ax.barh(ordered.index, ordered["avg_watch_ratio"], color=cyan)
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set(
        title="Raw watch time can mislead; normalize by video length",
        xlabel="Average share of video watched", ylabel="",
    )
    fig.tight_layout()
    fig.savefig(IMAGES / "watch_ratio_by_category.png", dpi=180)
    plt.close(fig)

    signals = [
        "watch_ratio", "completed_video", "liked", "shared",
        "followed_creator", "rewatched", "negative_feedback",
    ]
    correlations = (
        events[signals + ["continued_session"]]
        .corr()["continued_session"]
        .drop("continued_session")
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(9, 5.3))
    ax.barh(
        correlations.index.str.replace("_", " ").str.title(),
        correlations.values,
        color=[pink if value < 0 else cyan for value in correlations],
    )
    ax.axvline(0, color="#161823", linewidth=0.8)
    ax.set(
        title="Different signals tell different product stories",
        xlabel="Correlation with session continuation", ylabel="",
    )
    fig.tight_layout()
    fig.savefig(IMAGES / "signals_vs_continuation.png", dpi=180)
    plt.close(fig)


def main() -> None:
    events = load_events()
    metrics = category_scorecard(events)
    coefficients = signal_model(events)

    metrics.to_csv(DATA / "category_metrics.csv")
    coefficients.rename("standardized_log_odds_coefficient").to_csv(
        DATA / "model_coefficients.csv", header=True
    )
    create_charts(events, metrics)

    print(f"Analyzed {len(events):,} events across {events.user_id.nunique():,} users.")
    print("\nCategory scorecard:\n", metrics.round(3))
    print("\nDiagnostic model coefficients:\n", coefficients.round(3))


if __name__ == "__main__":
    main()
