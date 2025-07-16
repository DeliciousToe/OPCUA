# Projekt Monitoringu Siemens SITOP UPS1600 24V/DC by OPC UA

## Skrypt `opcua_automated.py`

Ten skrypt w języku Python odpowiada za automatyczne zbieranie danych telemetrycznych z urządzeń Siemens SITOP UPS1600 24V/DC za pośrednictwem protokołu OPC UA i przesyłanie ich do serwera Zabbix. Jest to kluczowy element rozwiązania monitorującego, umożliwiający bieżący nadzór nad stanem i parametrami pracy UPS-ów.

### Cel

Głównym celem skryptu jest:
* Nawiązanie bezpiecznego połączenia z serwerem OPC UA na urządzeniach UPS.
* Odczytywanie zdefiniowanych parametrów (np. poziom baterii, napięcie, prąd, statusy alarmowe) za pomocą ich NodeID.
* Formatowanie zebranych danych i wysyłanie ich do serwera Zabbix za pomocą `zabbix_sender`.
* Obsługa błędów połączenia i odczytu, zapewniająca odporność działania.

### Wymagania

Aby skrypt działał poprawnie, niezbędne są następujące komponenty:

1.  **Python 3:** Skrypt został napisany w Pythonie 3.
2.  **Biblioteka `opcua-client`:** Do komunikacji z serwerem OPC UA.
    ```bash
    pip install opcua-client
    ```
3.  **`zabbix_sender`:** Narzędzie klienckie Zabbixa, które jest używane do przesyłania danych do serwera. Musi być zainstalowane i dostępne w ścieżce systemowej (`/usr/bin/zabbix_sender` lub innej wskazanej w konfiguracji).
    * Instrukcje instalacji dla różnych systemów operacyjnych znajdziesz w dokumentacji Zabbixa.
4.  **Dostęp do serwerów OPC UA na UPS-ach:** Urządzenia UPS muszą być dostępne sieciowo pod wskazanymi adresami IP oraz mieć aktywny serwer OPC UA z odpowiednimi uprawnieniami.
5.  **Serwer Zabbix:** Dane będą przesyłane do działającego serwera Zabbix.

### Konfiguracja

Przed uruchomieniem skryptu należy skonfigurować następujące parametry:

* **Adresy IP UPS-ów:** Zdefiniuj mapowanie nazw hostów Zabbixa na adresy IP UPS-ów w słowniku `UPS_MAPPING`.
* **Adres IP i port serwera Zabbix:** Zmienne `ZABBIX_SERVER` i `ZABBIX_PORT`.
* **Ścieżka do `zabbix_sender`:** Zmienna `ZABBIX_SENDER_PATH`.
* **NodeID monitorowanych parametrów:** Słowniki `MONITOR_PARAMS_COMMON` i `MONITOR_PARAMS_DEV1_5` zawierają mapowanie kluczy Zabbixa na NodeID OPC UA. **Należy je dostosować do specyfiki Twoich urządzeń UPS.** Zweryfikuj, czy wskazane NodeID odpowiadają faktycznym wartościom na Twoich UPS-ach.

**Ważne: Zarządzanie Poświadczeniami OPC UA**

Ten skrypt wymaga nazwy użytkownika i hasła do połączenia z serwerem OPC UA. **Wersja skryptu w tym repozytorium (branch `main`) celowo NIE zawiera zakodowanych poświadczeń (`OPCUA_USERNAME`, `OPCUA_PASSWORD`).**

Aby zapewnić bezpieczne działanie, rekomenduje się dostarczenie tych danych w następujący sposób:

* **Zmienne środowiskowe:** Ustaw zmienne środowiskowe `OPCUA_USERNAME` i `OPCUA_PASSWORD` w systemie, na którym uruchamiany jest skrypt.
    ```bash
    export OPCUA_USERNAME="your_username"
    export OPCUA_PASSWORD="your_password"
    ```
    Następnie w skrypcie można je odczytać np. za pomocą `os.environ.get('OPCUA_USERNAME')`.
* **Oddzielny plik konfiguracyjny (np. `.env` lub `.ini`):** Utwórz plik (np. `.env`) poza repozytorium Git, który będzie przechowywał poświadczenia. Upewnij się, że ten plik jest dodany do `.gitignore`, aby nigdy nie trafił do publicznego repozytorium.
* **Bezpieczne przechowywanie sekretów:** W środowiskach produkcyjnych rozważ użycie dedykowanych rozwiązań do zarządzania sekretami (np. HashiCorp Vault, Kubernetes Secrets).

**W przypadku, gdy używasz dedykowanego skryptu do przechowywania poświadczeń (np. `ups_opcua_info.py` w osobnym, prywatnym branchu), upewnij się, że jest on poprawnie zaimportowany i jego zawartość nigdy nie trafi do publicznego repozytorium.**

### Uruchomienie

Skrypt powinien być uruchamiany cyklicznie (np. co 60 sekund) za pomocą narzędzi takich jak `cron` w systemach Linux.

Przykład wpisu w `crontab` (dla użytkownika `root`):

```bash
# Uruchamia skrypt co minutę
* * * * * /usr/bin/python3 /path/to/your/opcua_automated.py >> /var/log/opcua_automated_cron.log 2>&1
