from locust import HttpUser, task
import random


class FactorialTest(HttpUser):
    numbers = (1, 5, 10, 120, 2147483647)

    @task
    def endpoint1(self):
        self.client.get(f"/prime/{random.choice(self.numbers)}")
