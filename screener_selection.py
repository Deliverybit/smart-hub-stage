"""Shared proximity selection for Top 10 screeners."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

INTERNAL_THRESHOLD_PCT = 15
MAX_PAD_CAP_PCT = 30
TARGET_COUNT = 10

MARKET_MOOD_TIP = (
    "Proximity to the 52-week low: BELOW LOW = trading under the recorded low, "
    "AT LOW = within 2%, NEAR LOW = above 2% and within 30% of the 52-week low."
)


@dataclass(frozen=True)
class ProximitySelection:
    results: list[dict[str, Any]]
    mode: str
    strict_count: int
    padded_count: int
    eligible_count: int


def select_proximity_results(
    all_results: list[dict[str, Any]],
    *,
    target: int = TARGET_COUNT,
    internal_threshold: float = INTERNAL_THRESHOLD_PCT,
    max_pad_cap: float = MAX_PAD_CAP_PCT,
) -> ProximitySelection:
    """Select up to ``target`` rows using 15% strict / 30% cap proximity rules."""
    if not all_results:
        return ProximitySelection([], "empty", 0, 0, 0)

    def pct(row: dict[str, Any]) -> float:
        return float(row["% Above Low"])

    eligible = [row for row in all_results if pct(row) <= max_pad_cap]
    strict = sorted(
        [row for row in eligible if pct(row) <= internal_threshold],
        key=pct,
    )

    if len(strict) >= target:
        final = strict[:target]
        return ProximitySelection(
            final,
            "all_strict",
            len(final),
            0,
            len(eligible),
        )

    if strict:
        strict_tickers = {row["Ticker"] for row in strict}
        padded_pool = sorted(
            [row for row in eligible if row["Ticker"] not in strict_tickers],
            key=pct,
        )
        need = target - len(strict)
        padded = padded_pool[:need]
        final = strict + padded
        return ProximitySelection(
            final,
            "padded",
            len(strict),
            len(padded),
            len(eligible),
        )

    if eligible:
        final = sorted(eligible, key=pct)[:target]
        return ProximitySelection(
            final,
            "closest_only",
            0,
            len(final),
            len(eligible),
        )

    return ProximitySelection([], "empty", 0, 0, 0)


def selection_status_message(
    selection: ProximitySelection,
    *,
    asset_noun: str,
    scanned_count: int,
    universe_size: int,
) -> tuple[str, str]:
    """Return a Streamlit status helper name and markdown message."""
    count = len(selection.results)
    shortfall = ""
    if count < TARGET_COUNT:
        shortfall = f" (only **{count}** within **{MAX_PAD_CAP_PCT}%** right now)"

    if selection.mode == "all_strict":
        return (
            "success",
            f"Found **{count}** candidates{shortfall} from {scanned_count} of "
            f"{universe_size} {asset_noun} scanned.",
        )

    if selection.mode == "padded":
        return (
            "info",
            f"**{selection.strict_count}** {asset_noun} within "
            f"**{INTERNAL_THRESHOLD_PCT}%** of their 52-week low; "
            f"**{selection.padded_count}** additional closest names shown "
            f"(up to **{MAX_PAD_CAP_PCT}%**).{shortfall}",
        )

    if selection.mode == "closest_only":
        return (
            "info",
            f"No {asset_noun} within **{INTERNAL_THRESHOLD_PCT}%** of their 52-week low; "
            f"showing the **{count}** closest available (within "
            f"**{MAX_PAD_CAP_PCT}%**).{shortfall}",
        )

    return (
        "warning",
        f"No {asset_noun} within **{MAX_PAD_CAP_PCT}%** of their 52-week low right now.",
    )


def proximity_how_it_works(asset_label: str = "asset") -> str:
    """Standard info-box copy for proximity screeners."""
    return (
        f"**How it works:** Each {asset_label} is checked for proximity to its 52-week low, "
        f"ranked by closeness, and filtered to within **{MAX_PAD_CAP_PCT}%** of the low. "
        f"Names within **{INTERNAL_THRESHOLD_PCT}%** are preferred; if fewer than 10 qualify, "
        f"the closest names up to **{MAX_PAD_CAP_PCT}%** fill the table."
    )
