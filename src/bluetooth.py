from bleak import BleakScanner

class Bluetooth:
    def __init__(self):
        pass

    async def get_beacon_data(self):
        devices = await BleakScanner.discover()
        beacon_data = []
        for device in devices:
            beacon_data.append({
                "name": device.name,
                "address": device.address,
                "rssi": device.rssi
            })
        return beacon_data
