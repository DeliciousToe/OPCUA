# Siemens SITOP UPS1600 24V/DC OPC UA Monitoring Project

## `opcua_automated.py` Script

This Python script is responsible for automatically collecting telemetry data from Siemens SITOP UPS1600 24V/DC devices via the OPC UA protocol and sending it to a Zabbix server. It is a key component of the monitoring solution, enabling continuous supervision of UPS status and operating parameters.

### Purpose

The main goals of the script are:
* Establish a secure connection to the OPC UA server on UPS devices.
* Read defined parameters (e.g., battery level, voltage, current, alarm statuses) using their NodeIDs.
* Format the collected data and send it to the Zabbix server using `zabbix_sender`.
* Handle connection and read errors to ensure robust operation.

### Requirements

For the script to function correctly, the following components are essential:

1.  **Python 3:** The script is written in Python 3.
2.  **`opcua-client` library:** For communication with the OPC UA server.
    ```bash
    pip install opcua-client
    ```
3.  **`zabbix_sender`:** A Zabbix client tool used to send data to the server. It must be installed and accessible in the system's PATH (e.g., `/usr/bin/zabbix_sender` or other specified in configuration).
    * Installation instructions for various operating systems can be found in Zabbix documentation.
4.  **Access to OPC UA servers on UPS devices:** The UPS devices must be network accessible at the specified IP addresses and have an active OPC UA server with appropriate permissions.
5.  **Zabbix Server:** Data will be sent to a running Zabbix server.

### Configuration

Before running the script, the following parameters must be configured:

* **UPS IP Addresses:** Define the mapping of Zabbix host names to UPS IP addresses in the `UPS_MAPPING` dictionary.
* **Zabbix Server IP and Port:** `ZABBIX_SERVER` and `ZABBIX_PORT` variables.
* **Path to `zabbix_sender`:** `ZABBIX_SENDER_PATH` variable.
* **NodeIDs of monitored parameters:** The `MONITOR_PARAMS_COMMON` and `MONITOR_PARAMS_DEV1_5` dictionaries contain mappings of Zabbix keys to OPC UA NodeIDs. **These must be adjusted to the specific characteristics of your UPS devices.** Verify that the specified NodeIDs correspond to the actual values on your UPS units.

**Important: OPC UA Credential Management**

This script requires a username and password to connect to the OPC UA server. **The version of the script in this repository (`main` branch) deliberately DOES NOT contain hardcoded credentials (`OPCUA_USERNAME`, `OPCUA_PASSWORD`).**

To ensure secure operation, it is recommended to provide these credentials in one of the following ways:

* **Environment Variables:** Set `OPCUA_USERNAME` and `OPCUA_PASSWORD` as environment variables on the system where the script is run.
    ```bash
    export OPCUA_USERNAME="your_username"
    export OPCUA_PASSWORD="your_password"
    ```
    The script can then read them using, for example, `os.environ.get('OPCUA_USERNAME')`.
* **Separate Configuration File (e.g., `.env` or `.ini`):** Create a file (e.g., `.env`) outside the Git repository to store credentials. Ensure this file is added to `.gitignore` so it never gets committed to a public repository.
* **Secure Secret Management:** In production environments, consider using dedicated secret management solutions (e.g., HashiCorp Vault, Kubernetes Secrets).

**If you are using a dedicated script for credential storage (e.g., `ups_opcua_info.py` in a separate, private branch), ensure it is correctly imported and its content never reaches a public repository.**

### Running the Script

The script should be run cyclically (e.g., every 60 seconds) using system tools like `cron` on Linux systems.

Example `crontab` entry (for the `root` user):

```bash
# Runs the script every minute
* * * * * /usr/bin/python3 /path/to/your/opcua_automated.py >> /var/log/opcua_automated_cron.log 2>&1
