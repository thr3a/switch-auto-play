"""
BUNNY GARDEN2のギャンブルを自動ループする。
WINしたらセーブ、LOSEしたらロードして損失をなかったことにすることで実質的に負けなしで資金を増やし続ける。研究目的。

実行方法: uv run src/bunnygarden2/main.py
"""

import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, str(Path(__file__).resolve().parent))

import capture
import controller
import ocr

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M")
SESSION_DIR = REPO_ROOT / "captures" / "bunnygarden2" / RUN_ID

_shot_counter = 0


def shot(label: str) -> Path:
    """スクショを撮ってセッションディレクトリに連番付きで保存する"""
    global _shot_counter
    _shot_counter += 1
    filename = f"{_shot_counter:04d}_{label}.jpg"
    path = capture.capture_frame(SESSION_DIR, filename)
    print(f"  [capture] {path.name}")
    return path


def wait_for_text(label: str, keyword: str, timeout: float, interval: float = 1.0) -> dict:
    """指定キーワードを含む段落が現れるまでスクショ+OCRを繰り返す"""
    deadline = time.monotonic() + timeout
    while True:
        path = shot(label)
        try:
            result = ocr.analyze(path)
        except Exception as e:
            print(f"  [warn] OCR失敗: {e}")
            result = None

        if result is not None and ocr.contains_text(result, keyword):
            print(f"  [OK] 「{keyword}」を検出")
            return result

        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"{label}: 「{keyword}」を{timeout}秒待っても検出できませんでした。"
                f"画面がsizi.mdの想定と異なっている可能性があります。({path}を確認してください)"
            )
        time.sleep(interval)


def wait_for_amount(label: str, timeout: float, interval: float = 1.0) -> int:
    """WIN/LOSE画面の符号付き金額が現れるまでスクショ+OCRを繰り返す"""
    deadline = time.monotonic() + timeout
    while True:
        path = shot(label)
        try:
            result = ocr.analyze(path)
            amount = ocr.find_amount(result)
        except Exception as e:
            print(f"  [warn] OCR失敗: {e}")
            amount = None

        if amount is not None:
            print(f"  [OK] 金額 {amount:+,}円 を検出")
            return amount

        if time.monotonic() >= deadline:
            raise TimeoutError(f"{label}: 金額表示を{timeout}秒待っても検出できませんでした。({path}を確認してください)")
        time.sleep(interval)


def main() -> None:
    print(f"セッション開始: {RUN_ID} (保存先: {SESSION_DIR})")

    nx, idx = controller.connect()
    print("コントローラー接続完了")

    total_pnl = 0  # LOSE込みの損益(ロード前の見かけ上の値)
    real_pnl = 0  # LOSEはロードでなかったことになるのでWINのみ計上した実質損益
    round_count = 0
    win_count = 0
    WIN_LIMIT = 9

    try:
        # 最初の確認。「バニーガーデンへ入店します」が出ていなければsizi.mdの想定と違うので終了する
        wait_for_text("home_first", "ガーデンへ入店します", timeout=15)

        while True:
            round_count += 1
            print(f"=== ラウンド {round_count} (累計損益 {total_pnl:+,}円 / 実質損益 {real_pnl:+,}円) ===")

            # 右ボタン3回でギャンブルアイコンへ移動
            controller.press_n(nx, idx, controller.RIGHT, 3)
            # wait_for_text("home_gyanburu", "ギャンブルに挑戦します", timeout=10)

            controller.press(nx, idx, controller.A)
            wait_for_text("gyanburu_left", "安心して楽しく遊べるレートです", timeout=30)

            # 右に2回で一番高いレートへ
            controller.press_n(nx, idx, controller.RIGHT, 2)
            wait_for_text("gyanburu_right", "本気で勝負したいときのレートです", timeout=10)

            controller.press(nx, idx, controller.A)

            amount = wait_for_amount("gyanburu_result", timeout=60)
            total_pnl += amount

            controller.press(nx, idx, controller.B)

            # 下2回でセーブ/ロードへ
            # wait_for_text("home_gyanburu", "ギャンブルに挑戦します", timeout=10)
            controller.press_n(nx, idx, controller.DOWN, 2)

            if amount >= 0:
                real_pnl += amount
                win_count += 1
                print(f"WIN: {amount:+,}円 -> セーブして再挑戦 (WIN {win_count}/{WIN_LIMIT})")
                # セーブ選択 -> スロット選択 -> 上書き確認「はい」まで1秒間隔でAを4回
                controller.press_n(nx, idx, controller.A, 4, interval=1)
                # キャンセルでホームまで2回戻る
                controller.press_n(nx, idx, controller.B, 2, interval=1)
                controller.press_n(nx, idx, controller.UP, 2)
                controller.press_n(nx, idx, controller.LEFT, 3)

                if win_count >= WIN_LIMIT:
                    print(f"WINが{WIN_LIMIT}回たまったので終了します(日付変更対策)")
                    break
            else:
                print(f"LOSE: {amount:+,}円 -> ロードして損失をなかったことにする")
                # セーブ/ロードのサブメニューへ(デフォルトで「セーブ」がハイライトされている)
                controller.press(nx, idx, controller.A)
                # 「ロード」へカーソル移動してから選択->スロット選択->ロード確認「はい」まで1秒間隔でAを3回
                controller.press(nx, idx, controller.DOWN)
                controller.press_n(nx, idx, controller.A, 3, interval=1)
                wait_for_text("home_first_reload", "ガーデンへ入店します", timeout=30)

    except KeyboardInterrupt:
        print("ユーザー操作により中断しました")
    finally:
        print(f"終了。{round_count}ラウンド実施、累計損益 {total_pnl:+,}円 / 実質損益 {real_pnl:+,}円")


if __name__ == "__main__":
    main()
