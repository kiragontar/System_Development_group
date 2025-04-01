import json
import datetime
import os

class BookingEventsManager:
    def __init__(self, filename="booking_events.json"):
        self.filename = filename
        self.events = self.load_events()

    def load_events(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
        else:
            return []

    def save_events(self):
        with open(self.filename, "w") as f:
            json.dump(self.events, f, indent=4)

    def log_event(self, booking_id, user_id, event_type, event_data):
        print(f"Logging event: booking_id={booking_id}, user_id={user_id}, event_type={event_type}, event_data={event_data}")
        event = {
            "booking_id": booking_id,
            "user_id": user_id,
            "event_type": event_type,
            "event_data": event_data,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.events.append(event)
        self.save_events()

    def get_events(self, booking_id=None, event_type=None, start_date=None, end_date=None):
        filtered_events = self.events[:]  # Create a copy

        if booking_id:
            filtered_events = [e for e in filtered_events if e["booking_id"] == booking_id]
        if event_type:
            filtered_events = [e for e in filtered_events if e["event_type"] == event_type]
        if start_date:
            filtered_events = [e for e in filtered_events if datetime.datetime.fromisoformat(e["timestamp"]) >= start_date]
        if end_date:
            filtered_events = [e for e in filtered_events if datetime.datetime.fromisoformat(e["timestamp"]) <= end_date]

        return filtered_events