import os
import logging
import asyncio
import json

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.websocket = None
        self.notifications_file = 'data/notifications.json'

        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Load or clear notifications file
        try:
            os.remove(self.notifications_file)
            logging.info("Cleared old notifications file")
        except FileNotFoundError:
            logging.info("No old notifications file to clear")

    async def broadcast_update(self, data):
        """ Broadcast updates via WebSocket if available. """
        if self.websocket:
            try:
                await self.websocket.broadcast(data)
                logging.info(f"Broadcasted update: {data}")
            except Exception as e:
                logging.error(f"Failed to broadcast update: {e}")
        else:
            logging.warning("No active WebSocket to broadcast the update.")

    def add_notification(self, message, type="info"):
        """ Add a notification and save it to file. """
        notification = {
            "message": message,
            "timestamp": asyncio.get_event_loop().time(),
            "type": type
        }
        self.notifications.append(notification)
        self.save_notifications()

        # Broadcast update when notification is added
        asyncio.create_task(self.broadcast_update({"event": "new_notification", "notification": notification}))

    def get_notifications(self):
        """ Return the list of notifications. """
        return self.notifications

    def save_notifications(self):
        """ Save the latest notifications to a file. """
        try:
            with open(self.notifications_file, 'w') as f:
                json.dump(self.notifications[-100:], f)
        except Exception as e:
            logging.error(f"Failed to save notifications: {e}")

    def load_notifications(self):
        """ Load notifications from the file if available. """
        try:
            with open(self.notifications_file, 'r') as f:
                self.notifications = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notifications = []

    def notify_case_solved(self, case):
        """ Notify when a case is solved. """
        message = f"Case #{case.id} has been resolved ({'Constitutional' if case.constitutional else 'Unconstitutional'})"
        self.add_notification(message, "case_solved")

        # Broadcast update for solved cases
        asyncio.create_task(self.broadcast_update({"event": "case_solved", "case_id": case.id}))