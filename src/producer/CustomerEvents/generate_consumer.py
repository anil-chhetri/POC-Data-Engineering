from faker import Faker
import random

from .device import Device
from .location import Location
from .content import Content
from .user_subscriptions import UserSubscriptions
from .eventdetails import EventDetails
from .user_action import UserAction
from .recommendations import Recommendations
from .searchhistory import SearchHistory


device_type = ['desktop', 'tablet', 'smartTV', 'mobile']
event_type = ['content_play', 'search', 'browse']

def generate_consumer_event_data() -> dict:
    device = Device.generate_device_data(random.choice(device_type)).__next__().as_dict()
    location = Location.generate_location_data().__next__().as_dict()
    content = Content.generate_content_data().__next__().as_dict()
    event_detail = EventDetails.generate_event_data().__next__().as_dict()
    user_action = UserAction.generate_user_action_data()


    consumer_events = {
        "device": device,
        "location": location,
        "content": content,
        "event_type": random.choice(event_type),
        "user_subscription": UserSubscriptions.generate_user_subscription().__next__().as_dict(),
        "timestamp": str(random.randint(1, 1000)) + "-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 31)) + "T" + str(random.randint(0, 23)) + ":" + str(random.randint(0, 59)) + ":" + str(random.randint(0, 59)),
        "event_details": event_detail,
        "user_action": list(user_action),
        "recommendations": Recommendations.generate_recommendations(),
        "search_history": SearchHistory.generate_serach_history_data(),
    }

    return consumer_events
   

if __name__ == "__main__":
    generate_consumer_event_data()