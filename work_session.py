import asyncio

from factory import Factory
from game_settings import DEFAULT_WORK_SESSION_DURATION, DEFAULT_TIC_VALUE


class WorkSession:
    """This class represents a work session

    A work session has a duration during which the factory is working"""

    def __init__(self, factory: Factory, duration: int = DEFAULT_WORK_SESSION_DURATION):
        self.duration = duration
        self.remaining_time = duration
        self.factory = factory

    def start(self):
        while self.remaining_time > 0:
            asyncio.run(self.factory.make_work())
            self.remaining_time -= DEFAULT_TIC_VALUE
