import random
import inspect
from datetime import datetime

class UserAction:

    action_type = ['pause', 'completed', 'change quality', 'playback_speed']
    quality = ['HD', 'SD', '4K']

    def __init__(self, action_type):
        self.action_type = action_type


    def as_dict(self):
        """
        Convert the UserAction object to a dictionary representation.
        """
        return {
            key: value for key, value in vars(self).items() if value is not None
        }
        

    def random_timestamp(self):
        min_year = '2000'
        max_year = '2024'

        year = random.randint(int(min_year), int(max_year))
        month = random.randint(1, 12)
        day = random.randint(1, 27)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return datetime(year, month, day, hour, minute, second).isoformat()
    
    @staticmethod
    def remove_quality(old_quality):
        new_quality = UserAction.quality
        return [x for x in new_quality if x != old_quality]
    

    def generate_user_action_details(self):
        """
        Generate random user action details.
        """
        if self.action_type == 'pause':
            self.timestamp = self.random_timestamp()
            self.duration = random.randint(100, 1000)
        
        elif self.action_type == 'completed':
            self.timestamp = self.random_timestamp()
            self.duration = random.randint(100, 1000)
            self.completed = True

        elif self.action_type == 'change quality':
            self.timestamp = self.random_timestamp()
            self.old_quality = random.choice(UserAction.quality)
            self.new_quality = random.choice(UserAction.remove_quality(self.old_quality))

        elif self.action_type == 'playback_speed':
            self.timestamp = self.random_timestamp()
            self.old_speed = random.uniform(0.5, 2.0)
            self.new_speed = random.uniform(0.5, 2.0)
            
        
    @classmethod
    def generate_user_action_data(cls):
        """
        Generate random user action data.
        """

        user_actions = []
        for _ in range(random.randint(1, 5)):
            ua  = cls(action_type=random.choice(UserAction.action_type))
            ua.generate_user_action_details()
            user_actions.append(ua.as_dict())

        return user_actions