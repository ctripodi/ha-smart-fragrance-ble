"""Constants for the Smart Fragrance BLE integration."""
DOMAIN = "smart_fragrance_ble"
DEFAULT_NAME = "Smart Fragrance"
NUS_WRITE = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
NUS_NOTIFY = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
COMMAND_ON = bytes.fromhex("0301")
COMMAND_OFF = bytes.fromhex("0300")
COMMAND_STATUS = bytes.fromhex("05")
STATUS_LENGTH = 40
STATUS_ON_OFFSET = 9
POLL_SECONDS = 60
