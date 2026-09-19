AF_BLUETOOTHの有無を各Pythonで直接確認したコマンドです。

uv管理のvenv (python3.11, python-build-standalone)
.venv/bin/python3 -c "import socket; print(socket.AF_BLUETOOTH)"
→ AttributeError: module 'socket' has no attribute 'AF_BLUETOOTH'

miseで入っているpython3.13 (which python3が指すもの)
python3 -c "import socket; print(socket.AF_BLUETOOTH)"
→ 同じく AttributeError

システムのapt標準python3(3.14)
/usr/bin/python3 -c "import socket; print(socket.AF_BLUETOOTH)"
→ 31 (定数が存在＝Bluetoothソケット対応あり)

つまり単純に3つのPythonインタプリタで同じ1行のimportコードを実行して、属性が存在するかどうかを比較しただけです。uv/miseの「ビルド済みポータブルPython」(python-build-standalone系)は移植性重視でLinux固有のBluetoothヘッダに依存する機能を無効化してビルドされているため、AF_BLUETOOTHが存在しません。apt標準のpython3はUbuntuのビルドサーバでフルビルドされているため対応しています。


または、miseでpython-build-standaloneではなくpyenv経由でソースからビルドする（libbluetooth-devをインストール済みの状態でビルドすればAF_BLUETOOTHは有効になります）。

==========================
# 事前にBluetoothヘッダーを入れておく(既にインストール済みでした)
sudo apt install -y libbluetooth-dev

# ソースビルドを有効化(グローバル設定として永続化)
mise settings set python.compile 1

# python3.13をソースからビルド
mise install python@3.13

一時的に今回だけソースビルドしたい場合は、設定を永続化せず環境変数で:

MISE_PYTHON_COMPILE=1 mise install python@3.13

ビルド後、確認は:

mise use -g python@3.13
python3 -c "import socket; print(socket.AF_BLUETOOTH, socket.BTPROTO_L2CAP)"

AF_BLUETOOTHとBTPROTO_L2CAPが出力されればOKです。その後 .venvを作り直して(uv venv --python $(mise which python3) など) uv sync し直す必要があります。ビルド自体は数分かかります。実行してよければ言ってください。
