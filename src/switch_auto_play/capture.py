from datetime import datetime
from pathlib import Path

import cv2

CAPTURE_DEVICE_INDEX = 0
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "captures"


def capture_screenshot() -> Path:
    cap = cv2.VideoCapture(CAPTURE_DEVICE_INDEX, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        raise RuntimeError(f"キャプチャデバイス(index={CAPTURE_DEVICE_INDEX})を開けませんでした")

    try:
        ok, frame = cap.read()
        if not ok:
            raise RuntimeError("フレームの取得に失敗しました")
    finally:
        cap.release()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    output_path = OUTPUT_DIR / filename
    cv2.imwrite(str(output_path), frame)
    return output_path


def main() -> None:
    path = capture_screenshot()
    print(f"保存しました: {path}")


if __name__ == "__main__":
    main()
