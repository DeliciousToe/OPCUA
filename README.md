# NodeID_Browser - Narzędzia do Przeglądania i Walidacji NodeID OPC UA

Ten branch zawiera zestaw narzędzi w języku Python, które służą do przeglądania przestrzeni adresowej serwerów OPC UA na urządzeniach Siemens SITOP UPS1600 24V/DC. Skrypty te są nieocenione podczas procesu identyfikacji i walidacji konkretnych NodeID, które odpowiadają za dane telemetryczne dostępne w systemach UPS.

## Cel

Głównym celem tych skryptów jest:
* **`opcua_nodes_browse.py`**: Umożliwienie rekurencyjnego przeglądania całej lub części przestrzeni adresowej serwera OPC UA, wyświetlając nazwy węzłów, ich NodeID i klasy. Jest to szczególnie przydatne do odkrywania struktury danych na UPS-ie.
* **`opcua_specific_nodes.py`**: Pozwala na bezpośrednie odczytanie wartości z predefiniowanych NodeID. Służy do szybkiej weryfikacji, czy konkretne NodeID dostarczają oczekiwane dane i w jakim formacie.

Te narzędzia są kluczowe podczas początkowej fazy konfiguracji monitoringu, gdy potrzebujemy ustalić, które NodeID odpowiadają za konkretne parametry (np. napięcie baterii, temperatura, statusy alarmowe).

## Wymagania

Aby skrypty działały poprawnie, niezbędne są następujące komponenty:

1.  **Python 3:** Skrypty zostały napisane w Pythonie 3.
2.  **Biblioteka `opcua-client`:** Do komunikacji z serwerem OPC UA.
    ```bash
    pip install opcua-client
    ```
3.  **Dostęp sieciowy do UPS-a:** Urządzenie UPS musi być dostępne pod wskazanym adresem IP oraz mieć aktywny serwer OPC UA.

## Konfiguracja

Przed uruchomieniem skryptów należy skonfigurować następujące parametry:

* **Adres IP UPS-a:** Zmienna `UPS_IP_ADDRESS`.
* **Port OPC UA:** Zmienna `OPCUA_PORT` (domyślnie 4840).
* **Poświadczenia OPC UA:** Zmienne `OPCUA_USERNAME` i `OPCUA_PASSWORD`.

**Ważne: Zarządzanie Poświadczeniami i Adresem IP**

**Te skrypty zawierają miejsca na wpisanie adresu IP oraz poświadczeń do serwera OPC UA. NIE POWINNY być one twardo zakodowane w wersji, którą umieszczasz w publicznym repozytorium GitHub.**

**Zaleca się, aby przed użyciem tych skryptów, wartości `UPS_IP_ADDRESS`, `OPCUA_USERNAME` i `OPCUA_PASSWORD` były dostarczane w bezpieczny sposób:**

* **Edycja przed uruchomieniem:** Przed uruchomieniem skryptu, zmień tymczasowo wartości w pliku, a następnie **nie zapisuj ich i nie commituj** do Git.
* **Zmienne środowiskowe:** Możesz zmodyfikować skrypty, aby odczytywały te wartości ze zmiennych środowiskowych.
    ```python
    import os
    UPS_IP_ADDRESS = os.environ.get('UPS_IP_ADDRESS', '127.0.0.1') # Domyślna wartość, jeśli zmienna nie ustawiona
    OPCUA_USERNAME = os.environ.get('OPCUA_USERNAME')
    OPCUA_PASSWORD = os.environ.get('OPCUA_PASSWORD')
    ```
    Następnie ustaw zmienne przed uruchomieniem:
    ```bash
    export UPS_IP_ADDRESS="10.201.5.12"
    export OPCUA_USERNAME="your_username"
    export OPCUA_PASSWORD="your_password"
    python3 opcua_nodes_browse.py
    ```
* **Argumenty wiersza poleceń:** Jest to bardzo elastyczna metoda dla narzędzi diagnostycznych. Możesz użyć modułu `argparse` do dodania obsługi argumentów takich jak `--ip`, `--user`, `--password`.

## Uruchomienie

### `opcua_nodes_browse.py`

Ten skrypt przegląda całą przestrzeń adresową OPC UA, co może zająć trochę czasu i wygenerować dużo danych. Domyślnie ustawiona jest maksymalna głębokość przeglądania (`max_depth=5`), którą można zmienić w kodzie.

```bash
# Upewnij się, że skonfigurowałeś IP i poświadczenia w skrypcie lub przez zmienne środowiskowe
python3 opcua_nodes_browse.py
