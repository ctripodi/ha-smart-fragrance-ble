"""BLE GATT transport and state polling for Smart Fragrance."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from bleak_retry_connector import BleakClientWithServiceCache, establish_connection
from homeassistant.components import bluetooth
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    COMMAND_OFF, COMMAND_ON, COMMAND_STATUS, DOMAIN, NUS_NOTIFY, NUS_WRITE,
    POLL_SECONDS, STATUS_LENGTH, STATUS_ON_OFFSET,
)

_LOGGER = logging.getLogger(__name__)


def decode_power_status(data: bytes) -> bool | None:
    """Parse a validated 40-byte status frame; reject unknown formats."""
    if len(data) != STATUS_LENGTH or data[0] != 0x05:
        return None
    value = data[STATUS_ON_OFFSET]
    if value not in (0, 1):
        return None
    return bool(value)


class SmartFragranceCoordinator(DataUpdateCoordinator[bool]):
    """Short-lived BLE sessions, serialized to avoid overlapping GATT calls."""

    def __init__(self, hass, address: str):
        super().__init__(
            hass, _LOGGER, name=f"{DOMAIN}_{address}",
            update_interval=timedelta(seconds=POLL_SECONDS),
        )
        self.address = address
        self._lock = asyncio.Lock()

    async def _exchange(self, command: bytes) -> bool:
        async with self._lock:
            device = bluetooth.async_ble_device_from_address(
                self.hass, self.address, connectable=True
            )
            if device is None:
                raise UpdateFailed(f"No connectable Bluetooth proxy sees {self.address}")
            client = None
            notifications: asyncio.Queue[bytes] = asyncio.Queue()

            def on_notification(_sender, payload: bytearray) -> None:
                notifications.put_nowait(bytes(payload))

            try:
                client = await establish_connection(
                    BleakClientWithServiceCache, device,
                    name="Smart Fragrance", max_attempts=2, timeout=20.0,
                )
                await client.start_notify(NUS_NOTIFY, on_notification)
                if command != COMMAND_STATUS:
                    # Device has been observed to accept NUS writes with response=True.
                    await client.write_gatt_char(NUS_WRITE, command, response=True)
                    await asyncio.sleep(0.25)
                await client.write_gatt_char(NUS_WRITE, COMMAND_STATUS, response=True)
                # Ignore unrelated initial identification notifications.
                loop = asyncio.get_running_loop()
                deadline = loop.time() + 8.0
                while (remaining := deadline - loop.time()) > 0:
                    payload = await asyncio.wait_for(notifications.get(), remaining)
                    status = decode_power_status(payload)
                    if status is not None:
                        return status
                raise UpdateFailed("No valid BLE status response")
            except Exception as err:
                # UpdateFailed is left intact, all other transport errors mapped.
                if isinstance(err, UpdateFailed):
                    raise
                raise UpdateFailed(f"BLE transaction failed: {err}") from err
            finally:
                if client is not None:
                    try:
                        await asyncio.wait_for(client.disconnect(), timeout=8)
                    except Exception as err:
                        _LOGGER.debug("BLE disconnect failed: %s", err)

    async def _async_update_data(self) -> bool:
        return await self._exchange(COMMAND_STATUS)

    async def async_set_power(self, enabled: bool) -> None:
        result = await self._exchange(COMMAND_ON if enabled else COMMAND_OFF)
        if result != enabled:
            raise UpdateFailed("Device reported an unexpected power state")
        self.async_set_updated_data(result)
