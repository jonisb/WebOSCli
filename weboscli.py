import json
import keyring
from pywebostv.connection import WebOSClient

# the service is just a namespace for your app
service_id = "LGWebOSTV"  # TODO: make this configurable


def main():
    try:
        settings = load_settings()
        client = WebOSClient(settings["host"])
        client.connect()

        save_settings(settings)
    finally:
        client.close()


def save_settings(settings):
    settings_no_key = settings.copy()
    client_key = settings_no_key.pop("client_key")
    if keyring.get_password(settings["service_id"], "client_key") != client_key:
        keyring.set_password(service_id, "client_key", client_key)

    # save settings to settings.json
    with open("settings.json", "w") as f:
        json.dump(settings_no_key, f)


def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"service_id": service_id}

    settings["client_key"] = keyring.get_password(settings["service_id"], "client_key")

    return settings


if __name__ == "__main__":
    main()
