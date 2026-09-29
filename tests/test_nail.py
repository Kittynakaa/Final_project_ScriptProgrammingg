"""
ชุดทดสอบอัตโนมัติ (Automated Tests) — pytest
รันด้วย:  pytest   หรือ   python -m pytest
ครอบคลุม: การจำแนก undertone (ITA), การแปลงสี, และเครื่องมือแนะนำ (suggest/search/filter/sort)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.skin_analyzer import SkinAnalyzer
from src.palette_renderer import PaletteRenderer
from src.recommender import NailRecommender
from src.data_store import DataStore
from src.models import Suggestion
from src.api_client import ColorApiClient, FALLBACK_COLOR_NAMES


# ---------- SkinAnalyzer: จำแนก undertone จาก ITA ----------
def test_classify_ita_cool():
    assert SkinAnalyzer.classify_ita(40) == "cool"      # >= 28

def test_classify_ita_warm():
    assert SkinAnalyzer.classify_ita(5) == "warm"       # <= 10

def test_classify_ita_neutral():
    assert SkinAnalyzer.classify_ita(20) == "neutral"   # 10 < ita < 28

def test_undertone_unknown_when_no_skin():
    import numpy as np
    analyzer = SkinAnalyzer()
    black = np.zeros((50, 50, 3), dtype=np.uint8)       # ไม่มีพิกเซลผิว
    empty_mask = np.zeros((50, 50), dtype=np.uint8)
    tone, ita = analyzer.estimate_undertone(black, empty_mask)
    assert tone == "unknown"


# ---------- PaletteRenderer: แปลงสี ----------
def test_hex_to_bgr_white():
    assert PaletteRenderer.hex_to_bgr("#FFFFFF") == (255, 255, 255)

def test_hex_to_bgr_pure_red():
    # #FF0000 (แดง) -> BGR = (0, 0, 255)
    assert PaletteRenderer.hex_to_bgr("#FF0000") == (0, 0, 255)

def test_hex_to_bgr_without_hash():
    assert PaletteRenderer.hex_to_bgr("000000") == (0, 0, 0)


# ---------- NailRecommender: แนะนำ / ค้นหา / กรอง / เรียง ----------
def _recommender():
    ds = DataStore(data_dir="data")
    return NailRecommender(ds.load_rules())

def test_suggest_returns_at_most_max():
    rec = _recommender()
    sugs = rec.suggest("cool", "almond", "long")
    assert len(sugs) <= rec.max_results
    assert all(isinstance(s, Suggestion) for s in sugs)

def test_suggest_oval_prepends_ombre():
    rec = _recommender()
    sugs = rec.suggest("warm", "oval", "medium")
    assert "ombre" in sugs[0].tags        # ทรง oval -> ombré ขึ้นก่อน

def test_suggest_short_length_appends_micro_french():
    rec = _recommender()
    sugs = rec.suggest("neutral", "square", "short")
    notes = [s.note for s in sugs]
    assert any("micro-French" in n for n in notes)

def test_unknown_undertone_falls_back_to_neutral():
    rec = _recommender()
    sugs = rec.suggest("unknown", "stiletto", "long")
    assert len(sugs) > 0                   # ไม่ crash และมีคำแนะนำ

def test_search_finds_keyword():
    rec = _recommender()
    sugs = rec.suggest("cool", "round", "short")
    results = rec.search(sugs, "pastel")
    assert all(s.has_tag("pastel") for s in results)

def test_filter_by_tag():
    rec = _recommender()
    sugs = rec.suggest("cool", "round", "short")
    cools = rec.filter_by_tag(sugs, "cool")
    assert all("cool" in [t.lower() for t in s.tags] for s in cools)

def test_sort_by_palette_size_descending():
    rec = _recommender()
    sugs = rec.suggest("warm", "oval", "long")
    sizes = [len(s.palette) for s in rec.sort_by_palette_size(sugs)]
    assert sizes == sorted(sizes, reverse=True)

def test_dedupe_removes_duplicates():
    dup = [Suggestion(["#FFF"], ["a"], "x"), Suggestion(["#FFF"], ["a"], "x")]
    assert len(NailRecommender._dedupe(dup)) == 1


# ---------- ColorApiClient (External API + Defensive Fallback) ----------
def test_fallback_color_names_exist():
    assert FALLBACK_COLOR_NAMES["#FFFFFF"] == "White"
    assert FALLBACK_COLOR_NAMES["#C3C7FF"] == "Periwinkle"

def test_enrich_palette_structure():
    # ทำงานได้ทั้งกรณี API ออนไลน์และกรณี fallback (ไม่ขึ้นกับเน็ต)
    client = ColorApiClient(timeout=3)
    out = client.enrich_palette(["#C3C7FF", "#FFB3D1"])
    assert len(out) == 2
    for hx, name in out:
        assert hx.startswith("#")
        assert isinstance(name, str) and name != ""
    assert client.last_source in ("api", "fallback")
