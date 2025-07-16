# Zabbix Template: Siemens SITOP UPS1600 24V/DC by OPC UA

This branch contains the Zabbix XML template (`UPS by OPC-UA.xml`) designed for monitoring Siemens SITOP UPS1600 24V/DC units via the OPC UA protocol. This template defines all the necessary items, triggers, graphs, and value maps to effectively collect and visualize data, as well as alert on critical conditions of your UPS devices.

## Purpose

The primary goal of this template is to seamlessly integrate OPC UA data collected by external scripts (like `opcua_automated.py`) into Zabbix. It provides a comprehensive monitoring solution by defining:

* **Items:** Specifies what data to collect from each UPS, using `Zabbix Trapper` item types to receive data pushed by the `opcua_automated.py` script.
* **Triggers:** Defines conditions for generating alerts based on the collected data, with various severity levels.
* **Graphs:** Provides visual representations of key UPS parameters over time, facilitating trend analysis and quick status checks.
* **Value Maps:** Ensures human-readable interpretations for binary (0/1) status indicators.

## Monitored Parameters

The template is configured to monitor a wide range of UPS parameters, including but not limited to:

### Connection Status
* `ups.connection.status`: Indicates the success of the OPC UA connection to the UPS (0 = No Connection, 1 = Connected).

### Battery Health
* `ups.battery.charge_level`: Percentage of battery charge.
* `ups.battery.voltage`: Current battery voltage.
* `ups.buffer.remaining_time`: Estimated remaining backup time on battery (in seconds).
* `ups.battery.change_recommended`: Indicator if battery replacement is recommended (0/1).

### Device Status and Environment
* `ups.device.temperature`: Internal temperature of the UPS unit.

### Input Power
* `ups.input.voltage`: Input voltage supplied to the UPS.
* `ups.input.frequency`: Input power frequency. **Note: For some UPS models, this item might return non-numeric text values (e.g., `LocalizedText(...)`) instead of a numerical frequency. Triggers and graphs may be limited or require preprocessing for such cases.**

### Output Power and Load
* `ups.output.voltage`: Output voltage provided by the UPS to connected devices.
* `ups.output.frequency`: Output power frequency. **Note: Similar to input frequency, this might return non-numeric text values for some models.**
* `ups.load.current`: Current load drawn from the UPS.

### Alarm States (Binary Indicators: 0 = OK, 1 = Alarm)
* `ups.alarm.battery_deep_discharge`: Alarm for deep battery discharge.
* `ups.alarm.battery_low`: Alarm for low battery level. **Note: For some UPS models, this item might return non-numeric text values (e.g., `EUInformation(...)`). Triggers for this item might not be functional in such cases.**
* `ups.alarm.battery_temperature_high`: Alarm for high battery temperature.
* `ups.alarm.device_overtemperature`: Alarm for device overheating.
* `ups.alarm.input_voltage_high`: Alarm for high input voltage.
* `ups.alarm.input_voltage_low`: Alarm for low input voltage. **Note: For some UPS models, this item might be unsupported (`BadAttributeIdInvalid`) and will not provide data.**
* `ups.alarm.mains_failure`: Alarm for mains power failure.
* `ups.alarm.output_overload`: Alarm for output overload.
* `ups.alarm.ups_fault`: General UPS internal fault alarm.

## Import into Zabbix

To use this template, import the `UPS by OPC-UA.xml` file into your Zabbix server:

1.  Log in to your Zabbix web interface.
2.  Navigate to **Configuration > Templates**.
3.  Click the **Import** button in the top right corner.
4.  Click **Browse** and select the `UPS by OPC-UA.xml` file.
5.  Ensure that `Update existing` is checked if you are updating an existing template, or leave it unchecked if this is a new import.
6.  Click **Import**.

## Linking to Hosts

After importing, link this template to your UPS host(s) in Zabbix:

1.  Navigate to **Configuration > Hosts**.
2.  Select the host you want to monitor (or create a new host).
3.  Go to the **Templates** tab.
4.  In the "Link new templates" field, start typing "UPS by OPC-UA" and select it from the dropdown.
5.  Click **Add**.
6.  Click **Update** to save the host configuration.

Once the template is linked and the `opcua_automated.py` script starts sending data, Zabbix will begin collecting, visualizing, and alerting on your UPS performance.

---
