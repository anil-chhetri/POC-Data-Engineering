import random
class UserSubscriptions: 

    def __init__(self, plan, start_date, billing_cycle, connected_services):
        """
        Initialize a UserSubscriptions object with the given attributes.  
        
        Args:   
            plan (str): Subscription plan name.
            start_date (str): Start date of the subscription.
            billing_cycle (str): Billing cycle (e.g., monthly, yearly).
            connected_services (list): List of connected services.
        """
        
        self.plan = plan
        self.start_date = start_date
        self.billing_cycle = billing_cycle
        self.connected_services = connected_services


    def as_dict(self):
        """
        Convert the UserSubscriptions object to a dictionary representation.
        
        Returns:
            dict: Dictionary representation of the UserSubscriptions object.
        """
        return {
            "plan": self.plan,
            "start_date": self.start_date,
            "billing_cycle": self.billing_cycle,
            "connected_services": self.connected_services
        }
    
    @classmethod
    def generate_user_subscription(cls):
        """
        Generate user subscription data.
        
        Returns:
            UserSubscriptions: A UserSubscriptions object with random data.
        """
        while True:
            plans = ["Basic", "Standard", "Premium"]
            billing_cycles = ["monthly", "yearly"]
            connected_services = ["Netflix", "Hulu", "Amazon Prime", "Disney+", "HBO Max"]

            plan = random.choice(plans)
            start_date = str(random.randint(2000, 2023)) + "-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 31))
            billing_cycle = random.choice(billing_cycles)
            connected_services = random.sample(connected_services, random.randint(1, len(connected_services)))

            yield cls(plan, start_date, billing_cycle, connected_services)