#notification_manager.py

import os
import logging
import asyncio
import json
from fastapi.websockets import WebSocket

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.websocket_clients = set()  # Store multiple WebSocket connections
        self.notifications_file = "data/notifications.json"

        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Load notifications from file (if available)
        self.load_notifications()

    async def connect_websocket(self, websocket: WebSocket):
        """ Handle WebSocket connection. """
        await websocket.accept()
        self.websocket_clients.add(websocket)
        logging.info("New WebSocket client connected.")

        try:
            while True:
                data = await websocket.receive_text()
                logging.info(f"WebSocket received: {data}")
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
        finally:
            self.websocket_clients.remove(websocket)
            logging.info("WebSocket client disconnected.")

    async def broadcast_update(self, data):
        """ Broadcast updates to all connected WebSockets. """
        if self.websocket_clients:
            for client in list(self.websocket_clients):
                try:
                    await client.send_json(data)
                except Exception as e:
                    logging.error(f"Failed to broadcast update: {e}")
                    self.websocket_clients.remove(client)  # Remove disconnected client
        else:
            logging.warning("No active WebSockets to broadcast the update.")

    async def add_notification(self, message, type="info"):
        """ Add a notification and save it to file. """
        notification = {
            "message": message,
            "timestamp": asyncio.get_running_loop().time(),  # ✅ Use get_running_loop() instead of get_event_loop()
            "type": type
        }
        self.notifications.append(notification)
        self.save_notifications()

        # Broadcast update when notification is added
        await self.broadcast_update({"event": "new_notification", "notification": notification})

    def get_notifications(self):
        """ Return the list of notifications. """
        return self.notifications

    def save_notifications(self):
        """ Save the latest notifications to a file. """
        try:
            with open(self.notifications_file, "w") as f:
                json.dump(self.notifications[-100:], f)
        except Exception as e:
            logging.error(f"Failed to save notifications: {e}")

    def load_notifications(self):
        """ Load notifications from the file if available. """
        try:
            with open(self.notifications_file, "r") as f:
                self.notifications = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notifications = []

    async def notify_case_solved(self, case):
        """ Notify when a case is solved. """
        message = f"Case #{case.id} has been resolved ({'Constitutional' if case.constitutional else 'Unconstitutional'})"
        await self.add_notification(message, "case_solved")

        # Broadcast update for solved cases
        await self.broadcast_update({"event": "case_solved", "case_id": case.id})
