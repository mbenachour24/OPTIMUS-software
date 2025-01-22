import asyncio
import logging
from .notification_manager import NotificationManager

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Norm:
    def __init__(self, norm_id, text, valid=True, complexity=1):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.log_event(f"Initialized with complexity {complexity} and validity {valid}")

    def invalidate(self):
        self.valid = False
        self.log_event("Invalidated")
        asyncio.run(NotificationManager().broadcast_update({
            'type': 'norm_update',
            'norm_id': self.id,
            'valid': self.valid
        }))

    def log_event(self, message):
        log_message = f"Norm {self.id}: {message}"
        logging.info(log_message)
        print(log_message)