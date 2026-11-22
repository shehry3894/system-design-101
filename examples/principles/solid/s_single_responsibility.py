#
# Definition: A class should have only one reason to change → it should do one thing and do it well.
# Why: Reduces coupling, improves readability, and makes testing easier.

# ❌ Bad: Class does too many things (handles data + report generation)
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def save_to_db(self):
        print("Saving user to DB")

    def generate_report(self):
        print("Generating user report")

# ✅ Good: Split responsibilities
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user: User):
        print("Saving user to DB")

class UserReport:
    def generate(self, user: User):
        print("Generating user report")
