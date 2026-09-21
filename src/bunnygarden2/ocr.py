import re
import unicodedata
from pathlib import Path
from typing import Any

import requests

OCR_API_URL = "http://deep01.local:3200"
# WIN/LOSE画面の勝敗金額 (例: +54,400円 / -6,900円)
AMOUNT_PATTERN = re.compile(r"[+-][\d,]+円")


def analyze(image_path: Path) -> dict[str, Any]:
    """Yomitoku APIに画像を投げて解析結果のJSONを返す"""
    with open(image_path, "rb") as f:
        response = requests.post(
            f"{OCR_API_URL}/analyze",
            params={"format": "json"},
            files={"file": (image_path.name, f, "image/jpeg")},
            timeout=30,
        )
    response.raise_for_status()
    return response.json()


def normalize(text: str) -> str:
    """濁点/半濁点の誤認識(バ/パ等)を吸収するため、清音に正規化する"""
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def get_paragraph_texts(result: dict[str, Any]) -> list[str]:
    content = result["content"][0]
    return [p["contents"] for p in content.get("paragraphs", [])]


def contains_text(result: dict[str, Any], keyword: str) -> bool:
    """トップレベルのparagraphsにkeywordが部分一致で含まれるか判定する"""
    normalized_keyword = normalize(keyword)
    return any(normalized_keyword in normalize(text) for text in get_paragraph_texts(result))


def find_amount(result: dict[str, Any]) -> int | None:
    """WIN/LOSE画面の符号付き金額(例: +16,100円)を探す。見つからなければNone。
    金額はグラフィカルな領域(figure)として分類される場合とトップレベルのparagraphとして
    分類される場合の両方があるため、両方を検索する。
    """
    content = result["content"][0]
    texts = list(get_paragraph_texts(result))
    for figure in content.get("figures", []):
        for paragraph in figure.get("paragraphs", []):
            texts.append(paragraph.get("contents", ""))

    for text in texts:
        match = AMOUNT_PATTERN.search(text)
        if match:
            amount_str = match.group()
            sign = 1 if amount_str[0] == "+" else -1
            digits = amount_str[1:-1].replace(",", "")
            return sign * int(digits)
    return None
