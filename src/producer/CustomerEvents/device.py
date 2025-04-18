import random

class Device:

    os_type = {
        "mobile": ["Android", "iOS"],
        "desktop": ["Windows", "macOS", "Linux"],
        "tablet": ["Android", "iOS"],
        "smartTV": ["Android TV", "Tizen", "webOS"],
    }

    model_name = {
        "Android": ["Pixel 5", "Galaxy S21", "OnePlus 9", "Galaxy S21"],
        "iOS": ["iPhone 12", "iPad Pro", "iPhone SE"],
        "Windows": ["Surface Pro", "Dell XPS 13", "HP Spectre"],
        "macOS": ["MacBook Air", "MacBook Pro", "iMac"],
        "Linux": ["Dell XPS 13", "System76 Galago Pro", "Lenovo ThinkPad"],
        "Android TV": ["NVIDIA Shield", "Xiaomi Mi Box", "Roku"],
        "Tizen": ["Samsung Smart TV", "LG Smart TV"],
        "webOS": ["LG Smart TV", "Sony Smart TV"],
    }

    def __init__(self, type, os, os_version, app_version, model = None):
        self.type = type
        self.os = os
        self.os_version = os_version
        self.app_version = app_version
        self.model = model

    def as_dict(self):
        return {
            "type": self.type,
            "os": self.os,
            "os_version": self.os_version,
            "app_version": self.app_version,
            "model": self.model
        }
    
    @classmethod
    def generate_device_data(cls, type):
        """
        Generate device data based on the type of device.
        
        args:
            faker: Faker instance for generating random data.
            type: Type of device (mobile or desktop or tablet or smartTV).


        """
        while True:
            device_type =  cls(
                type=type,
                os=random.choice(Device.os_type[type]),
                os_version=str(random.uniform(10, 20)),
                app_version=str(random.randint(1,9)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 3)),
            )
            device_type.model = random.choice(Device.model_name[device_type.os])

            yield device_type
