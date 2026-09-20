import nuxbt
from nuxbt.bluez import find_devices_by_alias

nx = nuxbt.Nuxbt(debug=True)

reconnect_address = find_devices_by_alias("Nintendo Switch")
print(f"reconnect_address: {reconnect_address}")

controller_index = nx.create_controller(
    nuxbt.PRO_CONTROLLER,
    reconnect_address=reconnect_address,
)
nx.wait_for_connection(controller_index)

print("Connected")
print(controller_index)
