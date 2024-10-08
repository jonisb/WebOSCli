import logging
from typing import Dict, Callable, Optional
from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl, MediaControl, ApplicationControl

# Configure logging
logging.basicConfig(level=logging.INFO)


class WebOSError(Exception):
    """Custom exception for WebOS-related errors."""

    pass


class WebOSClass(object):
    def __init__(
        self, settings: Dict[str, str], service_id: str, callback: Callable[[str], None]
    ):
        """
        Initialize the WebOS client.

        :param settings: Dictionary containing connection settings
        :param service_id: Unique identifier for the service
        :param callback: Function to call for status updates
        """
        self.settings = settings
        self.service_id = service_id
        self.callback = callback
        self.save = False
        self.client: Optional[WebOSClient] = None
        self._system: Optional[SystemControl] = None
        self._media: Optional[MediaControl] = None
        self._application: Optional[ApplicationControl] = None

        try:
            self.client = WebOSClient(settings["host"])
            self.client.connect()
            self.register_device()
        except Exception as e:
            logging.error(f"Failed to initialize WebOS client: {e}")
            raise WebOSError(f"Failed to initialize WebOS client: {e}")

    def register_device(self) -> None:
        """Register the device with the TV."""
        for status in self.client.register(self.settings):
            if status == WebOSClient.PROMPTED:
                logging.info("Please accept the connection on the TV!")
                self.callback("Please accept the connection on the TV!")
                self.save = True
            elif status == WebOSClient.REGISTERED:
                logging.info("Registration successful!")
                self.callback("Registration successful!")

        if "host" not in self.settings:
            self.settings["host"] = self.client.host
            self.save = True

    def close(self) -> None:
        """Close the connection to the TV."""
        if self.client:
            self.client.close()

    def is_connected(self) -> bool:
        """Check if the client is connected to the TV."""
        return self.client is not None and self.client.connection is not None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def system(self) -> SystemControl:
        if not self._system:
            self._system = SystemControl(self.client)
        return self._system

    @property
    def media(self) -> MediaControl:
        if not self._media:
            self._media = MediaControl(self.client)
        return self._media

    @property
    def application(self) -> ApplicationControl:
        if not self._app:
            self._application = ApplicationControl(self.client)
        return self._application
