import random


class EventDetails:

    quality = ['HD', 'SD', '4K']
    boolean_values = [True, False]
    network_types = ['WiFi', 'Mobile', 'Ethernet','cable']
    internet_speed = ['mbps', 'gbps']

    def __init__(self,play_duration
                 , play_percentage
                 , playback_quality
                 , buffering_incidents
                 , playback_speed
                 , paused
                 , completed
                 , network_type
                 , bandwidth):
        self.play_duration = play_duration
        self.play_percentage = play_percentage
        self.playback_quality = playback_quality
        self.buffering_incidents = buffering_incidents
        self.playback_speed = playback_speed
        self.paused = paused
        self.completed = completed
        self.network_type = network_type
        self.bandwidth = bandwidth

    def as_dict(self):
        return {
            "play_duration": self.play_duration,
            "play_percentage": self.play_percentage,
            "playback_quality": self.playback_quality,
            "buffering_incidents": self.buffering_incidents,
            "playback_speed": self.playback_speed,
            "paused": self.paused,
            "completed": self.completed,
            "network_type": self.network_type,
            "bandwidth": self.bandwidth
        }
    
    @classmethod
    def generate_event_data(cls):
        """
        Generate random event data.
        """

        while True:
            yield cls(
                play_duration= random.randint(1, 1000),
                play_percentage = random.uniform(0, 100),
                playback_quality = random.choice(EventDetails.quality),
                buffering_incidents = random.randint(0, 5),
                playback_speed = random.uniform(0.5, 2.0),
                paused = random.choice(EventDetails.boolean_values),
                completed = random.choice(EventDetails.boolean_values),
                network_type = random.choice(EventDetails.network_types),
                bandwidth = str(random.randint(10, 100)) + random.choice(EventDetails.internet_speed),
            )