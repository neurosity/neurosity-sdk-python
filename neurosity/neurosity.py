from typing import Callable
import atexit
import pyrebase
from neurosity.config import PyRebase


class neurosity_sdk:
    """The Official Neurosity Python SDK 🤯"""

    def __init__(self, options: dict) -> None:
        """
        Args:
            options (dict): Configuration options for device_id and environment
        """
        if "device_id" not in options:
            raise ValueError("Neurosity SDK: A device ID is required to use the SDK")

        options.setdefault("environment", "production")
        self.client_id = None
        self.user = None
        self.token = None
        self.options = options
        pyrebase_config = (
            PyRebase.STAGING
            if options["environment"] == "staging"
            else PyRebase.PRODUCTION
        )
        self.firebase = pyrebase.initialize_app(pyrebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.subscription_ids = []
        atexit.register(self.exit_handler)

    def exit_handler(self) -> None:
        """Remove the client and all subscriptions"""
        self.remove_client()
        self.remove_all_subscriptions()

    def get_server_timestamp(self) -> dict:
        """Get the server timestamp"""
        return {".sv": "timestamp"}

    def login(self, credentials: dict) -> None:
        """
        Args:
            credentials (dict): Your email and password
        """
        if self.user is not None and self.token is not None:
            print("Neurosity SDK: The SDK is already authenticated.")
            return

        self.user = self.auth.sign_in_with_email_and_password(
            credentials["email"], credentials["password"]
        )
        self.token = self.user["idToken"]

        if self.client_id is None:
            self.add_client()

    def add_client(self) -> None:
        """Add a client"""
        device_id = self.options["device_id"]
        clients_path = f"devices/{device_id}/clients"
        timestamp = self.get_server_timestamp()
        push_result = self.db.child(clients_path).push(timestamp, self.token)
        self.client_id = push_result["name"]

    def remove_client(self):
        """Remove the client"""
        client_id = self.client_id
        if client_id:
            device_id = self.options["device_id"]
            client_path = f"devices/{device_id}/clients/{client_id}"
            self.db.child(client_path).remove(self.token)

    # @TODO: handle response
    def add_action(self, action: dict):
        """
        Args:
            action (dict): Dictionary of action data including:
                command, action, message
        """
        if "command" not in action:
            raise ValueError("A command is required for actions")

        if "action" not in action:
            raise ValueError("An action is required for actions")

        device_id = self.options["device_id"]
        actions_path = f"devices/{device_id}/actions"

        action.setdefault("responseRequired", False)
        action.setdefault("responseTimeout", None)

        push_result = self.db.child(actions_path).push(action, self.token)
        return push_result

    def add_subscription(self, metric: str, label: str, atomic: bool) -> str:
        """Add subscription"""
        client_id = self.client_id
        device_id = self.options["device_id"]
        subscription_id = self.db.generate_key()
        subscription_path = f"devices/{device_id}/subscriptions/{subscription_id}"

        subscription_payload = {
            "atomic": atomic,
            "clientId": client_id,
            "id": subscription_id,
            "labels": [label],
            "metric": metric,
            "serverType": "firebase",
        }

        self.db.child(subscription_path).set(subscription_payload, self.token)

        # caching subscription ids locally for unsubscribe teardown on exit
        self.subscription_ids.append(subscription_id)

        return subscription_id

    def remove_subscription(self, subscription_id: str) -> None:
        """Remove the given subscription"""
        device_id = self.options["device_id"]
        subscription_path = f"devices/{device_id}/subscriptions/{subscription_id}"
        self.db.child(subscription_path).remove(self.token)

    def remove_all_subscriptions(self) -> None:
        """Remove all subscriptions"""
        device_id = self.options["device_id"]
        subscriptions_path = f"devices/{device_id}/subscriptions"
        data = {}

        for subscription_id in self.subscription_ids:
            data[subscription_id] = None

        self.db.child(subscriptions_path).update(data, self.token)

    def stream_metric(
        self, callback: Callable, metric: str, label: str, atomic: bool
    ) -> Callable:
        """
        Args:
            callback (Callable): The callback that gets called on each epoch.
                Sample data is passed to the callback.
            metric (str): The brainwave metric to stream.
            label (str): The brainwave metric label, possible values:
                'raw', 'rawUnfiltered', 'psd', 'powerByBand'
            atomic (bool): Whether the metric is atomic or not.
        """
        subscription_id = self.add_subscription(metric, label, atomic)

        if atomic:
            metric_path = f"metrics/{metric}"
        else:
            metric_path = f"metrics/{metric}/{label}"

        def teardown(subscription_id):
            self.remove_subscription(subscription_id)
            self.subscription_ids.remove(subscription_id)

        return self.stream_from_path(callback, metric_path, teardown, subscription_id)

    def stream_from_path(
        self, callback: Callable, path_name: str, teardown=None, subscription_id=None
    ) -> Callable:
        """Stream data from a given path"""
        device_id = self.options["device_id"]

        path = f"devices/{device_id}/{path_name}"
        stream_id = subscription_id or self.db.generate_key()

        initial_message = {}

        def stream_handler(message):
            if message["path"] == "/":
                initial_message[message["stream_id"]] = message
                full_payload = message["data"]
            else:
                child = message["path"][1:]
                full_payload = initial_message[message["stream_id"]]["data"]
                if message["data"] is None:
                    # delete key if value is `None`
                    full_payload.pop(child, None)
                else:
                    full_payload[child] = message["data"]

            callback(full_payload)

        stream = self.db.child(path).stream(
            stream_handler, self.token, stream_id=stream_id
        )

        def unsubscribe():
            if teardown:
                teardown(stream_id)
            stream.close()

        return unsubscribe

    def get_from_path(self, path_name: str):
        """Get data from a given path"""
        device_id = self.options["device_id"]
        path = f"devices/{device_id}/{path_name}"
        snapshot = self.db.child(path).get(self.token)
        return snapshot.val()

    def add_marker(self, label: str):
        """Add a marker"""
        if not label:
            raise ValueError("A label is required for markers")

        return self.add_action(
            {
                "command": "marker",
                "action": "add",
                "message": {"label": label, "timestamp": self.get_server_timestamp()},
            }
        )

    def brainwaves_raw(self, callback: Callable) -> Callable:
        """Subscribe to the filtered raw brainwave data."""
        return self.stream_metric(callback, "brainwaves", "raw", False)

    def brainwaves_raw_unfiltered(self, callback: Callable) -> Callable:
        """Subscribe to the unfiltered raw brainwave data."""
        return self.stream_metric(callback, "brainwaves", "rawUnfiltered", False)

    def brainwaves_psd(self, callback: Callable) -> Callable:
        """Subscribe to the filtered power spectrum density (PSD) brainwave data."""
        return self.stream_metric(callback, "brainwaves", "psd", False)

    def brainwaves_power_by_band(self, callback: Callable) -> Callable:
        """Subscribe to the filtered power by band brainwave data."""
        return self.stream_metric(callback, "brainwaves", "powerByBand", False)

    def signal_quality(self, callback: Callable) -> Callable:
        """Standard deviation based signal quality metrics."""
        return self.stream_metric(callback, "signalQuality", None, True)

    def accelerometer(self, callback: Callable) -> Callable:
        return self.stream_metric(callback, "accelerometer", None, True)

    def calm(self, callback: Callable) -> Callable:
        """
        Constantly fires and predicts user's calm level from passive cognitive state.
        Calm is a probability from 0.0 to 1.0.
        """
        return self.stream_metric(callback, "awareness", "calm", False)

    def focus(self, callback: Callable) -> Callable:
        """
        Constantly fires and predicts user's focus level from passive cognitive state based on the gamma brainwave between 30 and 44 Hz.
        Focus is a probability from 0.0 to 1.0.
        """
        return self.stream_metric(callback, "awareness", "focus", False)

    def kinesis(self, label, callback: Callable) -> Callable:
        """Fires when a user attempts to trigger a side effect from defined thoughts."""
        return self.stream_metric(callback, "kinesis", label, False)

    def kinesis_predictions(self, label: str, callback: Callable) -> Callable:
        return self.stream_metric(callback, "predictions", label, False)

    def status(self, callback: Callable) -> dict:
        return self.stream_from_path(callback, "status")

    def settings(self, callback: Callable) -> dict:
        return self.stream_from_path(callback, "settings")

    def status_once(self) -> dict:
        return self.get_from_path("status")

    def settings_once(self) -> dict:
        return self.get_from_path("settings")

    def get_info(self) -> dict:
        return self.get_from_path("info")
