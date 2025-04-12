from faker import Faker
import random

from device import Device
from location import Location
from content import Content
from user_subscriptions import UserSubscriptions

import pprint

device_type = ['desktop', 'tablet', 'smartTV', 'mobile']
event_type = ['content_play', 'search', 'browse']

def main():
    device = Device.generate_device_data(random.choice(device_type)).__next__().as_dict()

    location = Location.generate_location_data().__next__().as_dict()

    content = Content.generate_content_data().__next__().as_dict()


    consumer_events = {
        "device": device,
        "location": location,
        "content": content,
        "event_type": random.choice(event_type),
        "user_subscription": UserSubscriptions.generate_user_subscription().__next__().as_dict(),
        "timestamp": str(random.randint(1, 1000)) + "-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 31)) + "T" + str(random.randint(0, 23)) + ":" + str(random.randint(0, 59)) + ":" + str(random.randint(0, 59))
    }

    pprint.pprint(consumer_events)
   

if __name__ == "__main__":
    main()