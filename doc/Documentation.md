# Documentation

Almost every application has a configuration that contains various attributes that define how the application behaves.
Typically, these attributes are contained in what is called a data model, which represents the data of the application.
In
Python, we can create a class with attributes to represent data. `duit` helps to work with data models by providing
tools and methods to implement recurring
and methods to implement recurring needs such as serialisation or observability.

The documentation gives an insight into the features of `duit` and explains the libraries core concepts.

## Event

One of the core component of duit is the `duit.event.Event.Event` class which implements the
classic [observer pattern](https://en.wikipedia.org/wiki/Observer_pattern) for generic values. Internally it stores a
list of event handlers and can be invoked to notify its listeners.

Here a basic example on how to create an event, register a listener and fire an event:

```python
from duit.event.Event import Event

# define event
on_new_age: Event[int] = Event()


# create an event handler
def on_birthday(value: int):
    print(f"You are now {value}")


# register handler on event - this can be repeated multiple times
on_new_age += on_birthday

# fire event multiple times
on_new_age(15)
on_new_age(16)
on_new_age(17)
```

Sometimes it is helpful to register a new handler and initially invoke it. `duit.event.Event.Event` has
the `invoke_latest(T)` method to just invoke the latest added event handler.

It is of course also possible to remove an event handler or check if it is already registered.

```python
if on_birthday in on_new_age:
    on_new_age -= on_birthday
```

The decision to use the `+=` and `-=` operator is because this syntax has proven itself in the programming language C#
and is simple to read and write. Of course there are also classic methods implemented like `contains()`, `append()`
and `remove()`.

## Data Field

The `duit.model.DataField.DataField` is a generic wrapper class for data attributes. Usually, it is used to capsule data
that represents the state of an application.
Because of that, it is necessary for other parts of the application to be notified when a state change happens. The
notification system is internally implemented by using the `duit.event.Event.Event` class which allows to register
listeners to data changes.

### Value

Here an example of how to work with a `duit.model.DataField.DataField`.

```python
import numpy as np
from duit.model.DataField import DataField

# creating example datafields
name = DataField("Test")
age = DataField(21)
data = DataField(np.zeros((5, 5)))

# display values
print(f"{name.value}: {age.value}")

# change value of the age
age.value += 1
```

The `duit.model.DataField.DataField` accepts any type of data but has to be initialized with a default value on setup.
The data itself is stored in the `value` attribute of the `duit.model.DataField.DataField`. Internally it uses
[generic typehints](https://docs.python.org/3/library/typing.html#building-generic-types-and-type-aliases) to support
code-completion and static type-checking tools.

A first advantage of wrapping the data into an object is, that the value now can be passed around by reference.

```python
def add_two(field: DataField):
    field.value += 2


age = DataField(21)
add_two(age)
print(age.value)  # outputs 23
```

### Observable

The `duit.model.DataField.DataField` class implements
the [observer pattern](https://en.wikipedia.org/wiki/Observer_pattern) and allows other classes or components of the
system to listen on changes of the value. The event which is fired when the data changes is called `on_changed`. It will
always notify the event handlers with the **new** value:

```python
# create event handler
def on_name_changed(new_name: str):
    print(f"New name: {new_name}")


# create datafield and register event handler
name = DataField("Test")
name.on_changed += on_name_changed

# change name
name.value = "Hello World"
```

If the `value` attribute is set with the exact same value (`__eq__`), the event does **not** fire. It is always possible
to fire the event manually by calling the method `fire()` or `fire_latest()`. Sometimes it is necessary to set the value
without firing an event. This can be done with the method `set_silent(T)` or completely disable the event invocation by
setting `publish_enabled = false`.

### Data Binding

Another feature that the `duit.model.DataField.DataField` enables is the possibility to
have [data bindings](https://en.wikipedia.org/wiki/Data_binding) between different attributes.

For example, it is possible to update other datafields when changing the value of another datafield (**one-way binding
**).

```python
a = DataField("A")
b = DataField("B")
c = DataField("C")

# bind a to b / c
a.bind_to(a)
a.bind_to(c)

# update value in a
a.value = "X"

print(b.value)  # outputs X

# important: this does not update a or c because it's a one-way binding
b.value = "BB"
```

#### Bidirectional Binding

It is also possible to synchronize the value of two attributes by creating a **two-way binding** or **bidirectional
binding**.

```python
from duit.model.DataField import DataField

a = DataField("A")
b = DataField("B")

a.bind_bidirectional(b)

a.value = "T"  # b gets updated to T
b.value = "X"  # a gets updated to X
```

#### Attribute Binding

Sometimes it can be helpful to bind directly to basic python attributes of variables. The `bind_to_attribute()` method
supports this behaviour.

```python
# example user class containing basic python attributes
class User:
    def __init__(self):
        self.name = "Test"


# create objects
user = User()
name = DataField("A")

# bind datafield name to user.name
name.bind_to_attribute(user, "name")
```

#### Converter Method

It is also possible to supply a converter method to the binding. This method is called when the value has changed and
before it has been written to the basic attribute.

```python
def to_upper(name: str) -> str:
    return name.upper()


name.bind_to_attribute(user, "name", to_upper)
```

#### Named Reference

Since attributes can not be passed by reference in python, the attribute name has to be supplied to the method as python
string. This can lead to problems when refactoring tools are used. To support refactorings and reference the actual
field, instead of its name, `duit` provides a helper method `duit.utils.name_reference.create_name_reference` to lookup
names of object attributes. It works by wrapping the actual object with a decorator class, which only returns the name
of the called attribute, instead of its value.

```python
from duit.model.DataField import DataField
from duit.utils.name_reference import create_name_reference

# every call to a user_ref attribute returns the attributes name instead of its value
user_ref = create_name_reference(user)
name.bind_to_attribute(user, user_ref.name)
```

## Data List

Since only the change of the entire value inside a `duit.model.DataField.DataField` is registered, change of values
inside a value are not triggered. The following example explains this behaviour:

```python
from duit.model.DataField import DataField

numbers = DataField([1, 2, 3])

numbers.value.append(5)  # this does not trigger on_changed
numbers.value = [5, 6, 7]  # this triggers on_changed
```

Since lists are an essential part of data models, `duit` implements the `duit.model.DataList.DataList` to support lists
with the same behaviour strategy as `duit.model.DataField.DataField`. It basically works like a normal
python [list](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists) but implements the observable
pattern.

```python
from duit.model.DataList import DataList

data = DataList([1, 2, 3])


def on_fire(value):
    print(f"list has changed: {value}")


data.on_changed += on_fire

data.append(5)
data.append(7)

for i in data:
    print(i)
```

It is also important to notice that `duit.model.DataList.DataList` inherits from `duit.model.DataField.DataField`.