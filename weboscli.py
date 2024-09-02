import json
import keyring

# the service is just a namespace for your app
service_id = "LGWebOSTV"  # TODO: make this configurable


def main():
    settings = load_settings()

    save_settings(settings)


def save_settings(settings):
    # save settings to settings.json
    with open("settings.json", "w") as f:
        json.dump(settings, f)


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
