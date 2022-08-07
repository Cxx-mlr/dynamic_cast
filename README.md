```python
from dynamic_cast import dynamic_cast, async_cast

@dynamic_cast
def sum(a: int, b: int) -> int:
    return a + b

@async_cast
async def async_sum(a: int, b: int) -> int:
    return a + b

@dynamic_cast
def add_one(x: float) -> float:
    return x + 1.01

assert sum(1, 2) == 3
assert sum("3", "4") == 7
assert add_one("1.0") == 2.01
assert asyncio.run(async_sum(1, 2)) == 3
```
