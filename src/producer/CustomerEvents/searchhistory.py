import random
from faker import Faker

class SearchHistory:

    @classmethod
    def generate_serach_history_data(cls):
        """
        Generate random search history data.
        """
        search_history = []
        f = Faker('en_GB')

        for i in range(random.randint(1, 5)):
            search_history.append({
                "search_id": "s" + str(random.randint(100000, 999999)),
                "timestamp": str(random.randint(2000, 2025)) + "-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28)) + "T" + str(random.randint(0, 23)) + ":" + str(random.randint(0, 59)) + ":" + str(random.randint(0, 59)),
                "query": random.choice(['quantum', 'nebula', 'photon', 'galaxy', 'cosmos']),
                "results_count": random.randint(10, 100),
            })

        return search_history