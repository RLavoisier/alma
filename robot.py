import random

from game_settings import CHEER_MESSAGES
from jobs import Job


class Robot:
    def __init__(self, name: str, job: Job, id: int):
        """This class represents a robot worker"""
        self.name = f"{name} (rev {random.randint(1, 400)})"
        self.job = job
        self.id = id

    async def work(self):
        res = await self.job.process()
        if issubclass(type(res), Job):
            self.job = res
            print(
                f"/!\ Human ressources announcement /!\: "
                f"{self.name} is now working on {self.job.name}, "
                f"congratulations on your new job !"
            )
        elif res:
            if res.get("success"):
                print(
                    f"{self.name} has built {res['quantity']} {self.job.produce} "
                    f"in {round(res['time'], 2)} seconds, "
                    f"{random.choice(CHEER_MESSAGES)}"
                )
            else:
                print(
                    f"{self.name} failed to make {self.job.produce} ! We are working and correcting the bug..."
                )

    def __repr__(self):
        return f"Name:{self.name} - Job:{self.job.name}"
