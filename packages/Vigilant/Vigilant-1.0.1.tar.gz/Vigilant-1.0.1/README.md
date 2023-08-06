# Vigilant
*Vigilant* is a small library, trying to make testing easier.<br>

`pip install Vigilant`

# How to use
After installing the library:
```py
from vigilant import test, run


@test('Description', args={'number': 1})
def demonstration(number):
    assert 1 + number == 2


run()  # Run all tests.

# PASS  demonstration:4 -> Description.

# Failing: 0
# Passed: 1
```