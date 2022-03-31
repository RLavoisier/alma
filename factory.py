import asyncio

import names

from jobs import Job, MiningFoo
from robot import Robot
from stock import Stock


class Factory:
    stock = Stock()

    def __init__(self):
        "This class handles the workers and filling the stock from their work"
        self.workers = []
        # emulate a bdd id
        self.next_worker_id = 1

    def create_worker(self, job: Job = None) -> Robot:
        """This method add a new robot to the production line"""
        worker_name = names.get_first_name()
        while worker_name in [worker.name for worker in self.workers]:
            worker_name = names.get_first_name()

        if not job:
            job = MiningFoo()

        worker = Robot(worker_name, job, self.next_worker_id)
        self.workers.append(worker)
        self.next_worker_id += 1
        return worker

    async def make_work(self):
        """This method make the different worker do their jobs"""
        return await asyncio.gather(*(worker.work() for worker in self.workers))
