import random
from faker import Faker
from faker.providers import address


class Location:

    Country = {
        "USA": "en_US",
        "UK": "en_GB",
        "Canada": "en_CA",
        "Australia": "en_AU",
        "Germany": "de_DE",
        "France": "fr_FR",
        "Italy": "it_IT",
        "Spain": "es_ES",
    }

    def __init__(self, country, city=None, region=None, timezone=None):
        self.country = country
        self.city = city
        self.region = region
        self.timezone = timezone

    def as_dict(self):
        return {
            "country": self.country,
            "city": self.city,
            "region": self.region,
            "timezone": self.timezone
        }
    
    @classmethod
    def generate_location_data(cls):
        """
        Generate random location data.
        
        args:
            faker: Faker instance for generating random data.
        
        """
        country = random.choice(cls.Country.keys())
        fake = Faker(cls.Country[country])

        # Generate random city, region, and timezone
        city, region, timezone = fake.local_latlng()
        while True:
            location = cls(
                country=fake.country(),
                city=fake.city(),
                region=fake.state(),
                timezone=fake.timezone()
            )
            yield location