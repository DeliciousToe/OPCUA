# Siemens SITOP UPS1600 24V/DC OPC UA Information Script

## `ups_opcua_info.py` Script

**THIS SCRIPT CONTAINS SENSITIVE INFORMATION AND SHOULD NEVER BE SHARED PUBLICLY OR COMMITTED TO A PUBLIC GITHUB REPOSITORY.**

This Bash script serves as a central configuration file for managing UPS device credentials and other critical information, which is then passed to the main `opcua_automated.py` monitoring script. Its primary purpose is to decouple sensitive data from the main automation logic, enhancing security.

### Purpose

The script's main responsibilities include:
* **Storing UPS Device Details:** It holds a list of UPS devices, each entry containing the UPS's IP address, its corresponding Zabbix host name, and the OPC UA password required for connection.
* **Orchestrating Monitoring:** It iterates through the list of UPS devices and calls the `opcua_automated.py` script for each one, passing the necessary connection details as command-line arguments.
* **Centralized Configuration:** Provides a single point of truth for managing multiple UPS units within the monitoring setup.

### Sensitive Data Disclosure Warning

**The `UPS_LIST` array within this script directly contains OPC UA passwords.** Hardcoding credentials, even in a seemingly private script, carries inherent risks.

**CRITICAL SECURITY CONSIDERATIONS:**

* **NEVER push this file or this branch to a public GitHub repository.**
* **Store this script ONLY in a private, access-controlled repository or directly on the server where it will be executed.**
* **For enhanced security, consider replacing hardcoded passwords with:**
    * **Environment Variables:** Pass passwords to `opcua_automated.py` via environment variables.
    * **Secure Secret Management Systems:** Utilize solutions like HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or similar tools to fetch credentials at runtime without storing them in files.

### Configuration

Before using this script, you must configure the `UPS_LIST` array:

* Each entry in `UPS_LIST` should be a string containing three space-separated values:
    1.  The **IP address** of the UPS device.
    2.  The **Zabbix Hostname** associated with this UPS (as configured in Zabbix).
    3.  The **OPC UA Password** for this UPS device.

    Example (replace placeholders with actual values):
    ```bash
    UPS_LIST=(
            "10.201.5.10 ups-host-a secretpassword1"
            "10.201.5.11 ups-host-b anothersecret"
            "10.201.5.12 ups-host-c finalpassword"
    )
    ```
* Ensure `PYTHON_SCRIPT` points to the correct path of your `opcua_automated.py` script.
* `ZABBIX_SERVER` variable also needs to be correctly set.

### Running the Script

This script is typically executed periodically (e.g., via `cron`) on the server responsible for collecting UPS data.

Example `crontab` entry:

```bash
# Runs the script every 5 minutes (adjust as needed)
*/5 * * * * /bin/bash /path/to/your/ups_opcua_info.py >> /var/log/ups_opcua_info_cron.log 2>&1
