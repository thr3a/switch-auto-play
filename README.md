# 準備

```
sudo usermod -aG video thr3a
```

## Python

Pythonのビルド miseでは通常ビルド済みのバイナリをインストールするがBluetooth非対応なのでセルフビルドする必要がある。

[pyenvのWIKI](https://github.com/pyenv/pyenv/wiki)の参考にインストール

```bash
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libzstd-dev
```

事前にBluetoothヘッダーを入れておく必要がある

```bash
sudo apt install -y libbluetooth-dev

```bash
MISE_PYTHON_COMPILE=1 mise install python@3.13
```

確認

```bash
python3 -c "import socket; print(socket.AF_BLUETOOTH, socket.BTPROTO_L2CAP)"
```

## ライブラリ

nuxbt用に必要なライブラリのインストール

```bash
sudo apt-get install libdbus-glib-1-dev libdbus-1-dev libcairo2-dev libgirepository-2.0-dev pkg-config
```

```
uv sync
```

最初は `uv run src/misc/nuxbt-init.py` 実行する。

# そのた

```bash
sudo apt install v4l-utils ffmpeg
```

```bash
ffmpeg -f v4l2 -input_format mjpeg -video_size 1280x720 -i /dev/video0 -f mpegts -listen 1 tcp://0.0.0.0:8554
# VLCとかでtcp://ubuntu06.local:8554
```
