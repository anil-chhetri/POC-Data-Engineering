from faker import Faker
import random

from device import Device

device_type = ['desktop', 'tablet', 'smartTV', 'mobile']

def main():
    device = Device.generate_device_data(random.choice(device_type)).__next__().as_dict()
    print(device)

if __name__ == "__main__":
    main()