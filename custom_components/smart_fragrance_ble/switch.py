"""Smart Fragrance power switch."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import CoordinatorEntity, UpdateFailed


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([SmartFragranceSwitch(entry.runtime_data, entry)])


class SmartFragranceSwitch(CoordinatorEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = "Power"
    _attr_icon = "mdi:air-filter"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.address}_power"
        self._attr_device_info = {
            "identifiers": {("smart_fragrance_ble", coordinator.address)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Felshare",
            "model": "SmartDiffuser 31-6",
        }

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data

    async def async_turn_on(self, **kwargs):
        try:
            await self.coordinator.async_set_power(True)
        except UpdateFailed as err:
            raise HomeAssistantError(str(err)) from err

    async def async_turn_off(self, **kwargs):
        try:
            await self.coordinator.async_set_power(False)
        except UpdateFailed as err:
            raise HomeAssistantError(str(err)) from err
