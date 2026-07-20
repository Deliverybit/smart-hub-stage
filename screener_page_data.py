"""Load screener results from Supabase snapshots with live-scan fallback."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from app_config import get_screener_symbol_limit
from screener_engine import selection_from_payload
from screener_selection import ProximitySelection, select_proximity_results
from screener_snapshots import fetch_snapshot, snapshot_is_fresh


@dataclass(frozen=True)
class ScreenerPageLoad:
    all_results: list[dict]
    display_results: list[dict]
    selection: ProximitySelection
    last_updated: str
    scanned_count: int
    universe_size: int
    asset_noun: str
    from_snapshot: bool
    headlines_enriched: bool


def load_screener_page_data(
    screener_key: str,
    *,
    universe_size: int,
    asset_noun: str,
    run_live: Callable[[], tuple[list[dict], str]],
) -> ScreenerPageLoad:
    """Return precomputed snapshot data when fresh, otherwise run the live screener."""
    payload = fetch_snapshot(screener_key)
    if payload and snapshot_is_fresh(payload):
        selection = selection_from_payload(payload)
        return ScreenerPageLoad(
            all_results=list(payload.get("all_results") or []),
            display_results=list(payload.get("display_results") or []),
            selection=selection,
            last_updated=str(payload.get("last_updated_display") or ""),
            scanned_count=int(payload.get("scanned_count") or 0),
            universe_size=int(payload.get("universe_size") or universe_size),
            asset_noun=str(payload.get("asset_noun") or asset_noun),
            from_snapshot=True,
            headlines_enriched=bool(payload.get("headlines_enriched")),
        )

    all_results, last_updated = run_live()
    selection = select_proximity_results(all_results)
    symbol_limit = get_screener_symbol_limit()
    return ScreenerPageLoad(
        all_results=all_results,
        display_results=selection.results,
        selection=selection,
        last_updated=last_updated,
        scanned_count=min(symbol_limit, universe_size),
        universe_size=universe_size,
        asset_noun=asset_noun,
        from_snapshot=False,
        headlines_enriched=False,
    )
