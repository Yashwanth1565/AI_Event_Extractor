from pydantic import BaseModel


class EventSchema(BaseModel):
    event_name: str
    event_date: str
    event_time: str
    event_location: str
    organizer: str