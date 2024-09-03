import logging
import argparse
import json
import keyring
from weboslib import WebOSClass, WebOSError

# Configure logging
logging.basicConfig(level=logging.INFO)


def main(service_id):
    settings = load_settings(service_id)
    try:
        with WebOSClass(settings, service_id, notify) as tv:
            if tv.is_connected():
                if tv.save:
                    save_settings(settings, service_id)
                tv.do_action()
    except WebOSError as e:
        logging.error(f"WebOS operation failed: {e}")


def notify(message):
    print(message)


def save_settings(settings, service_id):
    settings_no_key = settings.copy()
    client_key = settings_no_key.pop("client_key")
    if keyring.get_password(settings["service_id"], "client_key") != client_key:
        keyring.set_password(service_id, "client_key", client_key)

    # save settings to settings.json
    with open("settings.json", "w") as f:
        json.dump(settings_no_key, f)


def load_settings(service_id):
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"service_id": service_id}

    settings["client_key"] = keyring.get_password(settings["service_id"], "client_key")

    return settings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LG WebOS TV CLI")
    parser.add_argument(
        "--service_id", type=str, default="LGWebOSTV", help="Service ID for the app"
    )
    args = parser.parse_args()
    main(args.service_id)
