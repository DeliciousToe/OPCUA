# NodeID_Browser - OPC UA NodeID Browse and Validation Tools

This branch contains a set of Python tools designed to browse the address space of OPC UA servers on Siemens SITOP UPS1600 24V/DC devices. These scripts are invaluable during the process of identifying and validating specific NodeIDs that correspond to telemetry data available from UPS systems.

## Purpose

The main goals of these scripts are:
* **`opcua_nodes_browse.py`**: Enables recursive Browse of all or part of the OPC UA server's address space, displaying node names, their NodeIDs, and classes. This is particularly useful for discovering the data structure on the UPS.
* **`opcua_specific_nodes.py`**: Allows direct reading of values from predefined NodeIDs. This serves for quick verification of whether specific NodeIDs provide the expected data and in what format.

These tools are crucial during the initial setup phase of monitoring when you need to determine which NodeIDs correspond to specific parameters (e.g., battery voltage, temperature, alarm statuses).

## Requirements

For the scripts to function correctly, the following components are essential:

1.  **Python 3:** The scripts are written in Python 3.
2.  **`opcua-client` library:** For communication with the OPC UA server.
    ```bash
    pip install opcua-client
    ```
3.  **Network access to the UPS:** The UPS device must be accessible at the specified IP address and have an active OPC UA server.

## Configuration

Before running the scripts, the following parameters must be configured:

* **UPS IP Address:** `UPS_IP_ADDRESS` variable.
* **OPC UA Port:** `OPCUA_PORT` variable (default is 4840).
* **OPC UA Credentials:** `OPCUA_USERNAME` and `OPCUA_PASSWORD` variables.

**Important: OPC UA Credential and IP Address Management**

**These scripts contain placeholders for the IP address and OPC UA server credentials. They SHOULD NOT be hardcoded in the version you commit to a public GitHub repository.**

**It is recommended that, before using these scripts, the values for `UPS_IP_ADDRESS`, `OPCUA_USERNAME`, and `OPCUA_PASSWORD` are provided in a secure manner:**

* **Edit before running:** Temporarily change the values in the file before running the script, and then **do not save and do not commit** these changes to Git.
* **Environment Variables:** You can modify the scripts to read these values from environment variables.
    ```python
    import os
    UPS_IP_ADDRESS = os.environ.get('UPS_IP_ADDRESS', '127.0.0.1') # Default value if variable not set
    OPCUA_USERNAME = os.environ.get('OPCUA_USERNAME')
    OPCUA_PASSWORD = os.environ.get('OPCUA_PASSWORD')
    ```
    Then set the variables before running:
    ```bash
    export UPS_IP_ADDRESS="10.201.5.12"
    export OPCUA_USERNAME="your_username"
    export OPCUA_PASSWORD="your_password"
    python3 opcua_nodes_browse.py
    ```
* **Command-line Arguments:** This is a very flexible method for diagnostic tools. You can use the `argparse` module to add support for arguments like `--ip`, `--user`, `--password`.

## Running the Scripts

### `opcua_nodes_browse.py`

This script browses the entire OPC UA address space, which can take some time and generate a lot of output. By default, the maximum Browse depth is set to (`max_depth=5`), which can be changed within the code.

```bash
# Ensure you have configured the IP and credentials in the script or via environment variables
python3 opcua_nodes_browse.py
