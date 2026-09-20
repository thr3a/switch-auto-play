import time
from pathlib import Path

import cv2

CAPTURE_DEVICE_INDEX = 0
CAPTURE_WIDTH = 1920
CAPTURE_HEIGHT = 1080
# MiraBoxのキャプチャチップはストリーム開始直後、実映像が出るまで数秒間黒フレームを吐き続けるため
# その間のフレームを読み捨てて実映像が安定するのを待つ
WARMUP_SECONDS = 4.0


def capture_frame(output_dir: Path, filename: str) -> Path:
    """画面を1枚キャプチャし output_dir/filename に保存してパスを返す"""
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

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    cv2.imwrite(str(output_path), frame)
    return output_path
