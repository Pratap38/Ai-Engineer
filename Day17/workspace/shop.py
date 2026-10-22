"""Small shop / billing module used as a playground for the coding agent.
Running this file executes self-checks; it prints ALL CHECKS PASSED when everything works."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def apply_discount(price, percent):
    """Price after a percentage discount, never below zero."""
    discounted = price - price * percent / 100
    return max(discounted, 0)

def is_odd(n):
    return n%2!=0
def is_even(n):
    return n % 2 == 0


def reverse_text(text):
    return text[::-1]


class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, name, price, qty=1):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if name in self.items:
            self.items[name]["qty"] += qty
        else:
            self.items[name] = {"price": price, "qty": qty}

    def remove_item(self, name):
        self.items.pop(name, None)

    def item_count(self):
        return sum(item["qty"] for item in self.items.values())

    def total(self):
        return sum(item["price"] * item["qty"] for item in self.items.values())

    def total_with_tax(self, tax_percent=18):
        return round(self.total() * (1 + tax_percent / 100), 2)


def run_checks():
    assert add(2, 3) == 5
    assert subtract(10, 4) == 6
    assert multiply(3, 4) == 12
    assert divide(10, 4) == 2.5
    assert average([2, 4, 6]) == 4
    assert average([]) == 0
    assert apply_discount(200, 10) == 180
    assert apply_discount(50, 150) == 0
    assert is_even(4) and not is_even(7)
    assert is_odd(3) and not is_odd(4)
    assert reverse_text("abc") == "cba"

    cart = Cart()
    cart.add_item("pen", 10, 3)
    cart.add_item("book", 100)
    cart.add_item("pen", 10, 2)
    assert cart.item_count() == 6
    assert cart.total() == 150
    assert cart.total_with_tax() == 177.0
    cart.remove_item("book")
    assert cart.total() == 50
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    run_checks()
