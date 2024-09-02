import json


def main():
    settings = load_settings()


def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {}

    return settings


if __name__ == "__main__":
    main()
