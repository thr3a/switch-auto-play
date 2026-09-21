import time

import nuxbt
from nuxbt.bluez import find_devices_by_alias

nx = nuxbt.Nuxbt(debug=True)
print(nx.get_available_adapters)

controller_index = None
try:
    # 初回接続時は None(未ペアリング) 、2回目以降は前回のアドレスに再接続する
    reconnect_address = find_devices_by_alias("Nintendo Switch") or None
    print(f"reconnect_address: {reconnect_address}")

    controller_index = nx.create_controller(
        nuxbt.PRO_CONTROLLER,
        reconnect_address=reconnect_address,
    )
    nx.wait_for_connection(controller_index)

    print("Connected")
    print(controller_index)

    # 1秒に1回右ボタンを押す
    while True:
        nx.press_buttons(controller_index, [nuxbt.Buttons.DPAD_RIGHT])
        print("RIGHT")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n終了処理中...")
except OSError as e:
    # wait_for_connection がコントローラーのクラッシュを検知した場合
    print(f"接続エラー: {e}")
finally:
    if controller_index is not None:
        nx.remove_controller(controller_index)
        print("コントローラーを解放しました")
