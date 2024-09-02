import logging
from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl

# Configure logging
logging.basicConfig(level=logging.INFO)


class WebOSClass(object):
    def __init__(self, settings, service_id, callback):
        self.settings = settings
        self.service_id = service_id
        self.callback = callback
        self.client = WebOSClient(settings["host"])
        self.client.connect()
        self.save = False
        self.register_device()

    def do_action(self):
        system = SystemControl(self.client)
        system.notify(
            "This is a notification message!"
        )  # Show a notification message on the TV.

    def register_device(self):
        for status in self.client.register(self.settings):
            if status == WebOSClient.PROMPTED:
                self.callback("Please accept the connect on the TV!")
                self.save = True
            elif status == WebOSClient.REGISTERED:
                self.callback("Registration successful!")

        if "host" not in self.settings:
            self.settings["host"] = self.client.host
            self.save = True

    def close(self):
        self.client.close()
