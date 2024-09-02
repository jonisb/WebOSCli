import json
import keyring
from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl

# the service is just a namespace for your app
service_id = "LGWebOSTV"  # TODO: make this configurable


def main():
    try:
        settings = load_settings()
        client = WebOSClient(settings["host"])
        client.connect()
        register_device(client, settings)
        do_action(client)
    finally:
        client.close()


def do_action(client):
    system = SystemControl(client)
    system.notify(
        "This is a notification message!"
    )  # Show a notification message on the TV.


def register_device(client, settings):
    save = False
    for status in client.register(settings):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
            save = True
        elif status == WebOSClient.REGISTERED:
            print("Registration successful!")

    if "host" not in settings:
        settings["host"] = client.host
        save = True

    if save:
        save_settings(settings)


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
