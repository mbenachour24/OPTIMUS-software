import os
import logging
import asyncio

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.websocket = None
        try:
            os.makedirs('data', exist_ok=True)
            os.remove('data/notifications.json')
            logging.info("Cleared old notifications file")
        except FileNotFoundError:
            logging.info("No old notifications file to clear")

    async def broadcast_update(self, data):
        if self.websocket:
            try:
                await self.websocket.broadcast(data)
                logging.info(f"Broadcasted update: {data}")
            except Exception as e:
                logging.error(f"Failed to broadcast update: {e}")
        else:
            logging.warning("No active WebSocket to broadcast the update.")