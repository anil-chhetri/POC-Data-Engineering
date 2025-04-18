import json
import random
import inspect

class Recommendations:

    recom_algorithms =["collaborative", "content_based", "hybrid"]

    @classmethod
    def generate_recommendations(cls):
        recom = []

        for i in range(random.randint(1, 3)):
            recom.append({
                "content_id": "m" + str(random.randint(100000, 999999)),
                "position": i+1,
                "algorithm": random.choice(Recommendations.recom_algorithms),
                "clicked" : random.choice([True, False]),
            })

        return recom