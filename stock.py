from dataclasses import dataclass
from uuid import uuid4

from common import Singleton


@dataclass
class FooBar:
    uuid: uuid4 = None

    def __init__(self):
        self.uuid = uuid4()

    def __repr__(self):
        return self.uuid


class Stock(Singleton):
    def __init__(self):
        """This Class handles the stock of money and foo/bar"""
        self.foo = 0
        self.bar = 0
        self.foobar_list = []
        self.money = 0

    @property
    def foobar(self):
        return len(self.foobar_list)

    def sell_foobar(self, qty: int = 1):
        """This method remove x quantity of foobars from the stock"""
        del self.foobar_list[:qty]

    def add_foo(self, qty: int = 1):
        """This method add some foos to the stockpile"""
        self.foo += qty

    def add_bar(self, qty: int = 1):
        """This method add some bars to the stockpile"""
        self.bar += qty

    def add_foobar(self, qty: int = 1):
        """This method add some foobars to the stockpile"""
        for i in range(qty):
            self.foobar_list.append(FooBar())

    def add_money(self, qty: int = 1):
        """This method add some money to the stockpile"""
        self.money += qty

    def __repr__(self):
        return f"Foo: {self.foo} / Bar: {self.bar} / Foobar: {self.foobar} / Money: {self.money} €"
