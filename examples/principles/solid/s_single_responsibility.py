# S: Single Responsibility. A class should have one reason to change.
# Use when: one class mixes jobs that change for different reasons (data, storage, reports).
# Source: https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html


# Bad: a DB change and a report change both edit this one class.
class UserBad:
    def __init__(self, email):
        self.email = email

    def save(self):
        return f"INSERT {self.email}"

    def report(self):
        return f"User report: {self.email}"


# Good: one class per reason to change.
class User:
    def __init__(self, email):
        self.email = email


class UserRepository:  # changes when storage changes
    def save(self, user: User):
        return f"INSERT {user.email}"


class UserReport:  # changes when the report format changes
    def render(self, user: User):
        return f"User report: {user.email}"


u = User("a@b.com")
print(UserRepository().save(u))
print(UserReport().render(u))
assert UserRepository().save(u) == UserBad("a@b.com").save()  # same behaviour, now split by reason to change
