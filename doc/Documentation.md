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
field instead of its name, `duit` provides a helper method `duit.utils.name_reference.create_name_reference` to lookup
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

## Annotation

This chapter explains the core concepts of annotations and how custom annotations can be created. If you are interested
in annotations provided by `duit`, please head over to the specific chapter:

- [Settings](#settings)
- [Arguments](#arguments)
- [User-Interface](#user-interface)

To be able to provide extended possibilities for `duit.model.DataField.DataField`, `duit` introduces the concept of
field [annotations](https://docs.oracle.com/javase/tutorial/java/annotations/basics.html) to python. In python there are
only so called [decorators](https://peps.python.org/pep-0318/) to extend functionality of an already existing method or
function. To flag a class attribute, there is currently no concept available.

### Custom Annotation

To create a custom annotation that can be applied to a `duit.model.DataField.DataField`, a new class that inherits from
the abstract class `duit.annotation.Annoation.Annoation` has to be implemented. An annotation is applied to a datafield
by creating a private field attribute. This allows annotations to be applied to any python object in the future. The
attribute name has to be provided as a static method. Here an example annotation which provides a help text for a
datafield.

```python
from duit.annotation.Annotation import Annotation, M


class MyHelpAnnotation(Annotation):

    def __init__(self, help_text: str):
        self.help_text = help_text

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        return "__my_help_annotation"

    def _apply_annotation(self, model: M) -> M:
        model.__setattr__(self._get_annotation_attribute_name(), self)
        return model
```

### Usage

At the moment, the concept of annotations can only be applied to existing datafields. Since the @-notation is not
possible to use due to python syntax restrictions, the annotation has to be applied by using the **right-or
** (`__ror__`) operator. This operator has been chosen to not interfere with the existing type hint system and to be
able to simply stack multiple annotations. Here an example on how to apply the custom `MyHelpAnnotation` to an existing
datafield. Because the `_apply_annotation` method returns the same DataField type which has been applied to the method,
syntax completion in IDEs still work for the `age` attribute.

```python
age = DataField(21) | MyHelpAnnotation(help_text="The age of the user.")
```

To find annotations inside objects, `duit` provides a helper class
called `duit.annotation.AnnotationFinder.AnnotationFinder`. The class can find annotations of a specific type or subtype
inside objects, and also recursively inside attributes of such an object. This allows for complex object structures, for
example for configurations. To find our custom `MyHelpAnnotation` annotation, it is possible to use the annotation
finder as shown in the following example.

```python
from duit.annotation.AnnotationFinder import AnnotationFinder


# create user class and instantiate an example object
class User:
    age = DataField(21) | MyHelpAnnotation(help_text="The age of the user.")


user = User()

# create an annotation finder to find MyHelpAnnotations
finder = AnnotationFinder(MyHelpAnnotation)
annotations = finder.find(user)

# display the results
for field_name, (data_field, annotation) in annotations:
    print(f"Help text of attribute {field_name}: {annotation.help_text}")
```

## Settings

The `duit.settings.Settings.Settings` class is an [annotation](#annotation)
based [JSON](https://www.json.org/json-en.html) serializer and deserializer for `duit.model.DataField.DataField`. By
default, every datafield already has this annotation on instantiation. Here an example on how to load and save objects
into a file that contain datafields.

```python
from duit.settings.Settings import DefaultSettings


# define and instantiate an example class User
class User:
    def __init__(self):
        self.name = DataField("Test")
        self.age = DataField(21)


user1 = User()

# save user
DefaultSettings.save("test.json", user1)

# load user
user2 = DefaultSettings.load("test.json", User)
```

Of course there are also intermediate methods, which just serialize (to `dict`) or convert the object to a JSON string:

```python
from duit.settings.Settings import DefaultSettings

# serialization
result_dict: Dict[str, Any] = DefaultSettings.serialize(user)
result_str = DefaultSettings.save_json(user)

# deserialization
obj_from_dict = DefaultSettings.deserialize(result_dict, User)
obj_from_json = DefaultSettings.load_json(result_str, User)
```

### Setting Annotation

By default, each `duit.model.DataField.DataField` contains a `duit.settings.Setting.Setting` annotation, which defines
the JSON attribute name and if the datafield is exposed (default: `True`). To restrict serialization of a specific
datafield, it is possible to overwrite the default settings annotation.

```python
from duit.settings.Setting import Setting


class CustomUser:
    def __init__(self):
        self.name = DataField("Test") | Setting(exposed=False)  # this datafield is not serialized
        self.age = DataField(21) | Setting(name="user-age")  # change the name of setting
```

The `CustomUser` would result in the following serialized JSON:

```json
{
  "user-age": 21
}
```

### Custom Settings

Instead of using the `DefaultSettings` instance, it is possible to create multiple
custom `duit.settings.Settings.Settings` instances, which contain different type adapters or have different
configuration parameters. For simplicity, it is recommended to just use the `DefaultSettings` class.

### Type Adapter

A type adapter defines how a specific type is serialized and deserialized. A `duit.settings.Settings.Settings` class
contains a list of type adapters which can be used to define the serialization behaviour of complex data types. For a
custom type adapter example, please have a look at `duit.settings.serialiser.PathSerializer.PathSerializer`.

To register a custom type, use the `serializers` list attribute fo the `duit.settings.Settings.Settings` class.

```python
DefaultSettings.serializers.append(YourCustomSerializer())
```

## Arguments


## User-Interface