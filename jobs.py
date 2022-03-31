import abc
import asyncio
import random

from game_settings import DEFAULT_TIC_VALUE, DEFAULT_ROBOT_FOO_COST, DEFAULT_SELL_FOOBAR_DURATION, \
    DEFAULT_ASSEMBLE_FOOBAR_DURATION
from stock import Stock


class Job(abc.ABC):
    name = None
    produce = None
    duration = 1
    stock = Stock()
    quantity_per_process = 1

    def __init__(self):
        self.add_to_stock = None
        self.remaining_time = self.get_duration()
        self.has_ressource = False

    async def process(self):
        # Fetching ressources if needed
        if not self.has_ressource:
            self.use_stock()

        # If no ressource available, nothing can be done
        if not self.has_ressource:
            return

        # checking if there's still time to spend on the work
        if self.remaining_time > 0:
            await asyncio.sleep(DEFAULT_TIC_VALUE)
            self.remaining_time -= DEFAULT_TIC_VALUE
            return

        # Checking if the job is successfully done
        success = self.is_success()

        if not success:
            return self.failure()

        # If job is successfull we add the ressource to the stock
        self.add_to_stock(self.quantity_per_process)
        result = {
            "success": True,
            "time": self.duration,
            "quantity": self.quantity_per_process,
        }
        self.prepare_new_work()
        return result

    def prepare_new_work(self):
        self.has_ressource = False
        self.remaining_time = self.get_duration()

    def get_duration(self):
        return self.duration

    def use_stock(self):
        self.has_ressource = True

    def is_success(self):
        return True

    def failure(self):
        self.prepare_new_work()


class MiningFoo(Job):
    """This job create a foo

    this job has a duration of 1 seconds for each production
    """

    name = "Mining foo"
    produce = "Foo"

    def __init__(self):
        super().__init__()
        self.add_to_stock = self.stock.add_foo


class MiningBar(Job):
    """This job create a bar

    this job has a duration of 0,5 to 2 seconds for each production
    """

    name = "Mining bar"
    produce = "Bar"

    def __init__(self):
        super().__init__()
        self.add_to_stock = self.stock.add_bar

    def get_duration(self):
        self.duration = random.uniform(0.5, 2)
        return self.duration


class AssemblingFooBar(Job):
    """This job create a FooBar from a foo and a bar

    this job has a duration of 2 seconds for each production
    """

    name = "Assembling Foobar"
    produce = "Foobar"
    duration = DEFAULT_ASSEMBLE_FOOBAR_DURATION

    def __init__(self):
        super().__init__()
        self.add_to_stock = self.stock.add_foobar

    def use_stock(self):
        if self.stock.foo > 0 and self.stock.bar > 0:
            self.stock.foo -= 1
            self.stock.bar -= 1
            self.has_ressource = True
        else:
            self.has_ressource = False

    def is_success(self):
        return random.randint(0, 100) <= 60

    def failure(self):
        self.stock.add_bar(1)
        self.prepare_new_work()
        return {"success": False}


class ChangeJob(Job):
    """This Job allows a robot to change his job"""

    duration = DEFAULT_ROBOT_FOO_COST

    def __init__(self, new_job):
        super().__init__()
        self.new_job = new_job

    async def process(self):
        if self.remaining_time > 0:
            await asyncio.sleep(DEFAULT_TIC_VALUE)
            self.remaining_time -= DEFAULT_TIC_VALUE
        else:
            return self.new_job

    @property
    def name(self):
        return f"Being reprogrammed to {self.new_job.name}"


class SellFooBar(Job):
    """This job sell foobars"""

    duration = DEFAULT_SELL_FOOBAR_DURATION
    name = "Selling Foobar"
    produce = "€"

    def __init__(self):
        super().__init__()
        self.add_to_stock = self.stock.add_money

    def use_stock(self):
        if self.stock.foobar > 0:
            # we can sell 1 to 5 foobar in 10 seconds
            # we first need to check the stock
            max_quantity = (
                self.stock.foobar if self.stock.foobar < 5 else random.randint(1, 5)
            )
            # then we choose the random amount we will sell
            qty = random.randint(1, max_quantity)
            self.quantity_per_process = qty
            self.stock.sell_foobar(qty)
            self.has_ressource = True
