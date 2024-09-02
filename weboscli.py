import json
import keyring


def main():
    settings = load_settings()


def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        # the service is just a namespace for your app
        service_id = "LGWebOSTV"  # TODO: make this configurable
        settings = {"service_id": service_id}

    settings["client_key"] = keyring.get_password(settings["service_id"], "client_key")

    return settings


if __name__ == "__main__":
    main()
