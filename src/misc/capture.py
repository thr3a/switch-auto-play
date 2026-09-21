import time
from datetime import datetime
from pathlib import Path

import cv2

CAPTURE_DEVICE_INDEX = 0
# CAPTURE_WIDTH = 1280
# CAPTURE_HEIGHT = 720
CAPTURE_WIDTH = 1920
CAPTURE_HEIGHT = 1080
# MiraBoxのキャプチャチップはストリーム開始直後、実映像が出るまで数秒間黒フレームを吐き続けるため
# その間のフレームを読み捨てて実映像が安定するのを待つ
WARMUP_SECONDS = 4.0
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "captures"


def capture_screenshot() -> Path:
    cap = cv2.VideoCapture(CAPTURE_DEVICE_INDEX, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise RuntimeError(f"キャプチャデバイス(index={CAPTURE_DEVICE_INDEX})を開けませんでした")

    # デフォルトのYUYVだと真っ黒なフレームしか取得できないため明示的にMJPGへ切り替える
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

    try:
        deadline = time.monotonic() + WARMUP_SECONDS
        ok, frame = cap.read()
        if not ok:
            raise RuntimeError("フレームの取得に失敗しました")
        while time.monotonic() < deadline:
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
