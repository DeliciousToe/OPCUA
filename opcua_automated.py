from opcua import Client, ua
import sys
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='/var/log/opcua_automated.log')

OPCUA_PORT = 4840

OPCUA_USERNAME = "<USERNAME>"

ZABBIX_SERVER="127.0.0.1"
ZABBIX_PORT=10051
ZABBIX_SENDER_PATH="/usr/bin/zabbix_sender"

# Dla ups-br5 i ups-sclr5
MONITOR_PARAMS_COMMON={
        "ups.battery.voltage": "ns=3;i=100083",
        "ups.battery.charge_level": "ns=3;i=100075",
        "ups.buffer.remaining_time": "ns=3;i=100090",
        "ups.device.temperature": "ns=3;i=100165",
        "ups.input.voltage": "ns=3;i=100123",
        "ups.output.voltage": "ns=3;i=100136",
        "ups.load.current": "ns=3;i=100127",
        "ups.input.frequency": "ns=3;i=100161",
        "ups.output.frequency": "ns=3;i=100162",
        "ups.alarm.mains_failure": "ns=3;i=100041",
        "ups.alarm.battery_low": "ns=3;i=100042",
        "ups.battery.change_recommended": "ns=3;i=100074",
        "ups.alarm.battery_deep_discharge": "ns=3;i=100178",
        "ups.alarm.battery_temperature_high": "ns=3;i=100187",
        "ups.alarm.device_overtemperature": "ns=3;i=100184",
        "ups.alarm.input_voltage_high": "ns=3;i=100192",
        "ups.alarm.input_voltage_low": "ns=3;i=100047",
        "ups.alarm.output_overload": "ns=3;i=100196",
        "ups.alarm.ups_fault": "ns=3;i=100183"
        }

MONITOR_PARAMS_DEV1_5 = {
        'ups.connection.status': "ns=3;i=100000",
        'ups.battery.voltage': "ns=3;i=100215",
        'ups.battery.charge_level': "ns=3;i=100191",
        'ups.buffer.remaining_time': "ns=3;i=100194",
        'ups.device.temperature': "ns=3;i=100197",
        'ups.input.voltage': "ns=3;i=100200",
        'ups.output.voltage': "ns=3;i=100203",
        'ups.load.current': "ns=3;i=100209",
        'ups.battery.change_recommended': "ns=3;i=100135",
        'ups.alarm.battery_deep_discharge': "ns=3;i=100237",
        'ups.alarm.battery_temperature_high': "ns=3;i=100239",
        'ups.alarm.device_overtemperature': "ns=3;i=100255",
        'ups.alarm.input_voltage_high': "ns=3;i=100252",
        'ups.alarm.output_overload': "ns=3;i=100246",
        'ups.alarm.ups_fault': "ns=3;i=100243",
        }

UPS_CONFIGS={
        'ups-br5': MONITOR_PARAMS_COMMON,
        'ups-sclr5': MONITOR_PARAMS_COMMON,
        'ups-dev1.5': MONITOR_PARAMS_DEV1_5,
        }


def send_to_zabbix_sender(data_list):
    if not data_list:
        return

    # Proba wysylania pojedynczych danych
    #json_data={
    #        "request": "sender data",
    #        "data":[
    #            {"host": host, "key": key, "value": value}
    #            for host, key, value in data_list
    #            ]
    #        }
    for host, key, value in data_list:
        command=[
            ZABBIX_SENDER_PATH,
            "-z", ZABBIX_SERVER,
            "-p", str(ZABBIX_PORT),
            "-s", host,
            "-k", key,
            "-o", str(value)
            ]

        try:
       # json_payload = json.dumps(json_data)
        #print(f"DEBUG: Wysyłany ładunek JSON do Zabbix Sender:\n{json_payload}")

        #Kod zapsujacy w tmp/zabbix_json
       # temp_file_path = "/tmp/zabbix_json/zabbix_payload.json"
       # with open(temp_file_path, "w") as f:
       #     f.write(json_payload)
       # print(f"DEBUG: Ładunek JSON zapisany do pliku: {temp_file_path}")


            process = subprocess.run(
                command,
        #        input=json_payload.encode('utf-8'),
                capture_output=True,
                #text=True,        # DO Zakomentowania ze zwgledu na blad formatu json na wyjsciu zabbix_sender
                check=False
                )

            stdout = process.stdout.decode('utf-8').strip()
            stderr = process.stderr.decode('utf-8').strip()

            print(f"Zabbix Sender Output dla '{key}': {stdout}")
            if process.returncode != 0:
                print(f"Zabbix Sender Error dla '{key}' (Code {process.returncode}): {stderr}", file=sys.stderr)
                print(f"Sent data: host={host}, key={key}, value={value}", file=sys.stderr)
                logging.error(f"Zabbix Sender Error dla '{key}' (Code {process.returncode}): {stderr}")
                logging.error(f"Sent data: host={host}, key={key}, value={value}")


        except FileNotFoundError:
            print("Błąd: zabbix_sender nie znaleziony. Upewnij się, że jest zainstalowany i dostępny w PATH.", file=sys.stderr)
            logging.critical("Błąd: zabbix_sender nie znaleziony.")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd podczas wysyłania danych do Zabbix Sender: {e}", file=sys.stderr)
            logging.critical(f"Błąd podczas wysyłania danych do Zabbix Sender: {e}")
            sys.exit(1)

def main():
    if len(sys.argv) < 4:
        print("Użycie: python3 send_ups_data_to_zabbix.py <UPS_IP_ADDRESS> <ZABBIX_HOST_NAME> <UPS_PASSWORD>")
        sys.exit(1)

    ups_ip_address = sys.argv[1]
    zabbix_host_name = sys.argv[2]
    ups_password = sys.argv[3]

    opcua_endpoint = f"opc.tcp://{ups_ip_address}:{OPCUA_PORT}"

    connection_status = 0
    data_to_send=[]
    client = None

#Wybór właściwych parametrów na podsawie nazwy hosta zabbixa

    current_monitor_params = None
    if zabbix_host_name in UPS_CONFIGS:
        current_monitor_params = UPS_CONFIGS[zabbix_host_name]
        print(f"Używam konfiguracji dla hosta: {zabbix_host_name}", file=sys.stderr)
        logging.info(f"Używam konfiguracji dla hosta: {zabbix_host_name}")
    else:
        print(f"Błąd: Nie znaleziono konfiguracji dla hosta Zabbix '{zabbix_host_name}'.", file=sys.stderr)
        logging.error(f"Nie znaleziono konfiguracji dla hosta Zabbix '{zabbix_host_name}'.")
        sys.exit(1)

    try:
        print(f"Łączenie z serwerem OPC UA ({ups_ip_address}): {opcua_endpoint}...")
        client = Client(opcua_endpoint)
        # client.set_security_string("Basic256Sha256,SignAndEncrypt,/etc/ssl/certs/client_cert.der,/etc/ssl/private/client_key.pem")  # Do Ewentualnego wykorzystania
        client.set_user(OPCUA_USERNAME)
        client.set_password(ups_password)
        client.session_timeout = 360000

        client.connect()
        connection_status=1
        print("Połączono pomyślnie.")
        logging.info("Połączono pomyślnie.")

        data_to_send.append((zabbix_host_name, "ups.connection.status", connection_status))

        for zabbix_key, node_id in current_monitor_params.items():
            if zabbix_key == "ups.connection.status":
                continue
            try:
                node = client.get_node(node_id)
                value = node.get_value()
                if isinstance(value, bool):
                    value = int(value)
                print(f"Odczytano '{zabbix_key}' (NodeID: {node_id}): {value}")
                data_to_send.append((zabbix_host_name, zabbix_key, value))
            except ua.uaerrors.BadAttributeIdInvalid:
                print(f"Błąd podczas odczytu NodeID {node_id} ({zabbix_key}): \"The attribute is not supported for the specified Node.\"(BadAttributeIdInvalid)", file=sys.stderr)
                logging.warning(f"Błąd podczas odczytu NodeID {node_id} ({zabbix_key}): Atrybut nie jest wspierany.")
                if zabbix_key.startswith("ups.alarm.") or zabbix_key.startswith("ups.battery.change_recommended"):
                    data_to_send.append((zabbix_host_name, zabbix_key, 0))
            except Exception as e:
                print(f"Błąd podczas odczytu NodeID {node_id} ({zabbix_key}): {e}", file=sys.stderr)
                logging.error(f"Błąd podczas odczytu NodeID {node_id} ({zabbix_key}): {e}")
                if zabbix_key.startswith("ups.alarm.") or zabbix_key.startswith("ups.battery.change_recommended"):
                    data_to_send.append((zabbix_host_name, zabbix_key, 0))

    except ConnectionRefusedError:
        print(f"Błąd: Połączenie odrzucone. Upewnij się, że UPS ({ups_ip_address}) jest dostępny i port {OPCUA_PORT} jest otwarty.", file=sys.stderr)
        logging.error(f"Błąd: Połączenie odrzucone z UPS ({ups_ip_address}).")
        connection_status=0
    except Exception as e:
        print(f"Wystąpił błąd podczas łączenia z serwerem OPC UA ({ups_ip_address}): {e}", file=sys.stderr)
        logging.critical(f"Wystąpił błąd podczas łączenia z serwerem OPC UA ({ups_ip_address}): {e}")
        connection_status=0
        if "BadUserAccessDenied" in str(e):
            print("Błąd: Dostęp do serwera OPC UA został odrzucony (BadUserAccessDenied). Sprawdź nazwę użytkownika i hasło oraz uprawnienia na serwerze UPS-a.", file=sys.sys.stderr)
        elif "BadSessionNotActivated" in str(e):
            print("Błąd: Sesja OPC UA nie została aktywowana (BadSessionNotActivated). To często oznacza problem z uwierzytelnieniem. Upewnij się, że używasz poprawnego użytkownika/hasła i że domyślne hasło zostało zmienione w interfejsie webowym UPS-a.", file=sys.stderr)
        elif "BadSecurityChecksFailed" in str(e) or "BadIdentityTokenRejected" in str(e):
            print("Błąd: Problemy z bezpieczeństwem lub uwierzytelnianiem. Sprawdź certyfikaty lub metody uwierzytelniania na serwerze UPS-a.", file=sys.stderr)
    finally:
        if connection_status==1:
            client.disconnect()
            connection_status=0
            print(f"\nRozłączono z serwerem OPC UA ({ups_ip_address}).")

        data_to_send.append((zabbix_host_name, "ups.connection.status", connection_status))

        if data_to_send:
            print("\nWysyłanie danych do Zabbix...")
            logging.info("Wysyłanie danych do Zabbix...")
            send_to_zabbix_sender(data_to_send)
        else:
            print("\nBrak danych do wysłania do Zabbix.")
            logging.warning("Brak danych do wysłania do Zabbix.")
            sys.exit(1)

if __name__=="__main__":
    main()