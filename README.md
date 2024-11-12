# Repository Moved to [dynamic-cast](https://github.com/Cxx-mlr/dynamic-cast)

This project has been moved to a new repository where the final version is actively maintained and updated. Please visit [dynamic-cast](https://github.com/Cxx-mlr/dynamic-cast) for the latest code and documentation.

## Old Example (for reference)

While this repository is no longer maintained, here's a sample of how the original `dynamic_cast` and `async_cast` decorators were used:

## Basic Arithmetic Operations
```python
# python >= 3.10.5
from dynamic_cast import dynamic_cast, async_cast
import asyncio

# example
@dynamic_cast
def sum(a: int, b: int) -> int:
    return a + b

@async_cast
async def async_sum(a: float, b: int) -> float:
    return a + b

@dynamic_cast
def add_one(x: float) -> float:
    return x + 1.01

assert sum(1, 2) == 3
assert sum("3", "4") == 7
assert add_one("1.0") == 2.01
assert asyncio.run(async_sum("1.01", 2)) == 3.01
```

```py
from dynamic_cast import dynamic_cast, async_cast
import asyncio

@dynamic_cast
def multiply(a: int, b: int) -> int:
    return a * b

@async_cast
async def async_multiply(a: float, b: float) -> float:
    return a * b

@dynamic_cast
def subtract(x: float, y: float) -> float:
    return x - y

assert multiply(3, 4) == 12
assert multiply("5", "6") == 30
assert subtract("10.5", "2.5") == 8.0
assert asyncio.run(async_multiply("2.0", "3.5")) == 7.0
```

## String Manipulations

```python
from dynamic_cast import dynamic_cast, async_cast
import asyncio

@dynamic_cast
def concatenate(x: str, y: str) -> str:
    return x + y

@async_cast
async def async_upper(s: str.upper) -> str:
    return s

@dynamic_cast
def repeat_string(s: str, times: int) -> str:
    return s * times

assert concatenate("Hello, ", "World!") == "Hello, World!"
assert concatenate(1, 2) == "12"
assert repeat_string(12, "3") == "121212"
assert asyncio.run(async_upper("hello")) == "HELLO"
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
