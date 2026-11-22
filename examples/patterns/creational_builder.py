# Builder: build a complex object step by step, instead of one constructor with many arguments.
# Use when: an object has many optional parts and a 10-argument constructor gets unreadable.
# Source: https://www.gofpattern.com/creational/patterns/builder-pattern.php
# This chained form is Joshua Bloch's Builder (Effective Java, Item 2), the one you meet most in real code.
# The GoF version adds a Director that runs the same steps on different builders to get different results.
from dataclasses import dataclass, field


@dataclass
class HttpRequest:
    method: str = "GET"
    url: str = ""
    headers: dict = field(default_factory=dict)
    body: str | None = None


class HttpRequestBuilder:
    def __init__(self, url: str):
        self._request = HttpRequest(url=url)

    def method(self, method: str):
        self._request.method = method
        return self  # returning self allows chaining

    def header(self, key: str, value: str):
        self._request.headers[key] = value
        return self

    def json(self, body: str):
        self._request.body = body
        return self.header("Content-Type", "application/json")

    def build(self) -> HttpRequest:
        return self._request


req = (
    HttpRequestBuilder("https://api.example.com/orders")
    .method("POST")
    .header("Authorization", "Bearer <token>")
    .json('{"item": "pizza"}')
    .build()
)
print(req)
assert req.method == "POST" and req.headers["Content-Type"] == "application/json"
