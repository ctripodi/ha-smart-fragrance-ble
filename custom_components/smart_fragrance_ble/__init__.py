"""Smart Fragrance BLE integration setup."""
from __future__ import annotations

from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .coordinator import SmartFragranceCoordinator

PLATFORMS = ["switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = SmartFragranceCoordinator(hass, entry.data[CONF_ADDRESS])
    entry.runtime_data = coordinator
    # Do not fail setup when the diffuser is out of range; state stays unavailable.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await coordinator.async_refresh()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
