from opcua import Client
import sys

UPS_IP_ADDRESS = "IP"
OPCUA_PORT = 4840
OPCUA_ENDPOINT = f"opc.tcp://{UPS_IP_ADDRESS}:{OPCUA_PORT}"

OPCUA_USERNAME = "USERNAME"
OPCUA_PASSWORD = "PASSWORD"

def browse_node(node, indent=0, max_depth=5):
    if indent > max_depth:
        return

    try:
        children = node.get_children()
        for child in children:
            display_name_obj = child.get_display_name()
            display_name = display_name_obj.to_string() if display_name_obj else "[Unknown]"
            node_id = child.nodeid.to_string()
            node_class = child.get_node_class()

            print(f"{'  ' * indent}- {display_name} (NodeID: {node_id}, Class: {node_class.name})")

            if node_class.name in ["Object", "Folder"]:
                browse_node(child, indent + 1, max_depth)
    except Exception as e:
        current_node_id = node.nodeid.to_string() if hasattr(node, 'nodeid') else "[Unknown Node]"
        print(f"{'  ' * indent}  (Error Browse children of {current_node_id}: {e})", file=sys.stderr)


def main():
    client = Client(OPCUA_ENDPOINT)
    client.set_user(OPCUA_USERNAME)
    client.set_password(OPCUA_PASSWORD)
    client.session_timeout = 360000
    is_connected = False
    try:
        print(f"Łączenie z serwerem OPC UA: {OPCUA_ENDPOINT}...")
        client.connect()
        is_connected = True
        print("Połączono pomyślnie.")
        root_node = client.get_root_node()
        print("\n--- Dostępne przestrzenie nazw (NamespaceArray) ---")
        try:
            namespace_array_node = client.get_node("i=2255")
            namespace_uris = namespace_array_node.get_value()
            for i, uri in enumerate(namespace_uris):
                print(f"  Namespace Index {i}: {uri}")
            print("--------------------------------------------------")
        except Exception as e:
            print(f"Błąd podczas odczytu NamespaceArray: {e}", file=sys.stderr)
            print("Kontynuuję przeglądanie głównego drzewa obiektów.", file=sys.stderr)

        objects_node = root_node.get_children()[0]

        print("\n--- Przeglądanie przestrzeni adresowej serwera OPC UA (główne obiekty) ---")
        browse_node(objects_node, max_depth=3)

    except ConnectionRefusedError:
        print(f"Błąd: Połączenie odrzucone. Upewnij się, że UPS jest dostępny pod adresem {UPS_IP_ADDRESS} i port {OPCUA_PORT} jest otwarty.", file=sys.stderr)
        print("Sprawdź ustawienia firewalla na UPS-ie i w sieci.", file=sys.stderr)
    except Exception as e:
        print(f"Wystąpił błąd podczas łączenia lub przeglądania: {e}", file=sys.stderr)
        if "BadUserAccessDenied" in str(e):
            print("Błąd: Dostęp do serwera OPC UA został odrzucony (BadUserAccessDenied).", file=sys.stderr)
            print("Sprawdź nazwę użytkownika i hasło oraz uprawnienia na serwerze UPS-a.", file=sys.stderr)
        elif "BadSessionNotActivated" in str(e):
            print("Błąd: Sesja OPC UA nie została aktywowana (BadSessionNotActivated). To często oznacza problem z uwierzytelnieniem.", file=sys.stderr)
            print("Upewnij się, że używasz poprawnego użytkownika/hasła i że domyślne hasło zostało zmienione w interfejsie webowym UPS-a.", file=sys.stderr)
        elif "BadSecurityChecksFailed" in str(e) or "BadIdentityTokenRejected" in str(e):
            print("Błąd: Problemy z bezpieczeństwem lub uwierzytelnianiem. Sprawdź certyfikaty lub metody uwierzytelniania.", file=sys.stderr)
    finally:
        if is_connected == True:
            client.disconnect()
            is_connected = False
            print("\nRozłączono z serwerem OPC UA.")
        else:
            print("\nNie można było rozłączyć, ponieważ połączenie nie zostało nawiązane.")


if __name__ == "__main__":
    main()