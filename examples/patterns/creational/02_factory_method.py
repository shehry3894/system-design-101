# Factory Method: "Define an interface for creating an object, but let subclasses decide which class to instantiate."
# Use when: shared code needs an object, but each subclass picks the concrete type.
# Source: https://www.gofpattern.com/creational/patterns/factory-method-pattern.php
# Not the same as a "simple factory" (one function with if/else). That is handy, but it is not this GoF pattern.
from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, text: str) -> str: ...


class Email(Notification):
    def send(self, text):
        return f"email: {text}"


class SMS(Notification):
    def send(self, text):
        return f"sms: {text}"


class OrderService(ABC):
    @abstractmethod
    def create_notification(self) -> Notification: ...  # the factory method

    def confirm(self, order_id: int) -> str:  # shared logic: does not know Email or SMS
        return self.create_notification().send(f"order {order_id} confirmed")


class WebOrderService(OrderService):
    def create_notification(self):
        return Email()


class MobileOrderService(OrderService):
    def create_notification(self):
        return SMS()


print(WebOrderService().confirm(1))
print(MobileOrderService().confirm(2))
assert MobileOrderService().confirm(2) == "sms: order 2 confirmed"
