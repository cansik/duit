# Simbi
Simbi is a toolkit with helpful code for python.

It is based on the ideas of [cansik/bildspur-base](https://github.com/cansik/bildspur-base) and [cansik/bildspur-ui](https://github.com/cansik/bildspur-ui).

## Example

```python
class Config:
    def __init__(self):
        self.age = DataModel(5) | NumberAnnotation("Age")
        self.hungry = DataModel(True) | BooleanAnnotation("Hungry")
        self.year = DataModel(2021) | NumberAnnotation("Year", 2000, 2050)
        self.temperature = DataModel(30.2) | SliderAnnotation("Temperature", 0, 40)
```