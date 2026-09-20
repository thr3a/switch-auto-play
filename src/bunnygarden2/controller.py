import time

import nuxbt
from nuxbt.bluez import find_devices_by_alias

A = nuxbt.Buttons.A
B = nuxbt.Buttons.B
UP = nuxbt.Buttons.DPAD_UP
DOWN = nuxbt.Buttons.DPAD_DOWN
LEFT = nuxbt.Buttons.DPAD_LEFT
RIGHT = nuxbt.Buttons.DPAD_RIGHT


def connect() -> tuple[nuxbt.Nuxbt, int]:
    # nx = nuxbt.Nuxbt(debug=True)
    nx = nuxbt.Nuxbt()
    reconnect_address = find_devices_by_alias("Nintendo Switch")
    print(f"reconnect_address: {reconnect_address}")

    controller_index = nx.create_controller(
        nuxbt.PRO_CONTROLLER,
        reconnect_address=reconnect_address,
    )
    nx.wait_for_connection(controller_index)
    return nx, controller_index


def press(nx: nuxbt.Nuxbt, controller_index: int, button: str, down: float = 0.1, up: float = 0.3) -> None:
    nx.press_buttons(controller_index, [button], down=down, up=up)
    time.sleep(0.5)


def press_n(
    nx: nuxbt.Nuxbt,
    controller_index: int,
    button: str,
    times: int,
    interval: float = 0.4,
    down: float = 0.1,
) -> None:
    """同じボタンをinterval秒間隔でtimes回押す"""
    for i in range(times):
        press(nx, controller_index, button, down=down, up=0.1)
        if i < times - 1:
            time.sleep(interval)
    time.sleep(0.5)
