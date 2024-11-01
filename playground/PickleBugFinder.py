import pickle

from duit.event.Event import Event
from duit.model.DataField import DataField


def pickle_get_attributes(obj):
    return obj.__class__, obj.__dict__


def pickle_restore_attributes(cls, attributes):
    obj = cls.__new__(cls)
    obj.__dict__.update(attributes)
    return obj


def check_if_pickle(obj):
    obj_class, obj_attrs_dict = pickle_get_attributes(obj)

    obj_attrs_dict["__class__"] = obj_class

    for nm, attr in obj_attrs_dict.items():
        print(f"{nm} {type(attr)}")
        try:
            pickle_str = pickle.dumps(attr)
        except TypeError as e:
            print(f"CANNOT PICKLE {nm} of type {type(attr)}")


field = DataField("a")
event = Event()
check_if_pickle(event)
