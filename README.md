# Smart Fragrance BLE for Home Assistant

[Español](#español) · [English](#english)

> Community-maintained, experimental custom integration. Not affiliated with or endorsed by Felshare or Home Assistant.

## English

Local Bluetooth LE power control for a tested **Felshare SmartDiffuser 31-6**, controlled by the Android app `uni.glhxf`. It uses Home Assistant Bluetooth infrastructure, including ESPHome Bluetooth proxies. No vendor cloud credentials required.

### Features

- Power switch: ON (`03 01`) / OFF (`03 00`) over Nordic UART BLE.
- Power state query (`05`): the validated 40-byte response has ON/OFF at offset 9 (zero-based).
- 60-second polling (unchanged), including changes made using the Android app.
- Uses short-lived BLE connections and does not alter diffuser schedules, intensity or fan settings.

### Tested device

| Item | Value |
|---|---|
| Manufacturer | Felshare |
| Model | SmartDiffuser 31-6 (single tested unit) |
| App | Smart Fragrance (`uni.glhxf`) |
| Transport | Bluetooth Low Energy, Nordic UART Service |
| BLE UART write | `6e400002-b5a3-f393-e0a9-e50e24dcca9e` |
| BLE UART notify | `6e400003-b5a3-f393-e0a9-e50e24dcca9e` |

Other Felshare models have **not** been confirmed compatible. Your device's BLE address must be provided during setup; the address of the originally tested unit is intentionally not included in the public package.

### Install

1. Back up Home Assistant.
2. Copy `custom_components/smart_fragrance_ble/` into `/config/custom_components/smart_fragrance_ble/` or add the GitHub repository to **HACS → Custom repositories → Integration** after publishing it.
3. Restart Home Assistant Core.
4. **Settings → Devices & services → Add integration → Smart Fragrance BLE**. Enter your diffuser's BLE MAC address.
5. Verify manual ON/OFF and status synchronization before adding automations.

Do not place this integration inside the Terminal & SSH add-on Python environment. It belongs in Home Assistant Core's `custom_components` directory.

### Known limitations

- Confirmed only on a single diffuser; experimental protocol interpretation.
- Polling every 60 seconds, not instant push sync.
- BLE signal or proxy contention can cause transient unavailable states.
- The power state is the device's *logical enabled* state, not a guarantee it is currently nebulizing (scheduling may disable spraying).
- No firmware updates, fan, scent-program, or intensity controls.
- Existing Home Assistant entities are preserved when upgrading from v0.1.1. The MAC address is requested only for **new** configurations.

### Privacy

No credentials, device IDs, captured MQTT traffic, or private network addresses are committed. The integration operates locally.

### Contributions

Report compatibility findings and reproducible issues at [Issues](https://github.com/ctripodi/ha-smart-fragrance-ble/issues). Please redact MAC addresses, API keys, tokens, and private IPs from diagnostics.

## Español

Integración experimental de Home Assistant para controlar por **Bluetooth local** el encendido/apagado de un difusor Felshare SmartDiffuser 31-6, con lectura de estado cada **60 segundos**. No depende de la nube Felshare. Fue validada en una unidad; otros modelos todavía no están verificados.

**Instalación:** copiá `custom_components/smart_fragrance_ble` a `/config/custom_components/`, reiniciá Home Assistant y agregá **Smart Fragrance BLE** desde Dispositivos y servicios. También puede instalarse desde HACS como repositorio personalizado una vez publicado en GitHub.

**Precaución:** el interruptor habilita o deshabilita el equipo; la nebulización sigue respetando los horarios y ciclos del fabricante. No se modifican los ESPHome Bluetooth Proxy existentes.

**Licencia:** MIT. **Mantenimiento:** [@ctripodi](https://github.com/ctripodi).
