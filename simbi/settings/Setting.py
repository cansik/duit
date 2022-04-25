from typing import Optional

from simbi.model.DataField import DataField
from simbi.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME


class Setting:
    def __init__(self, name: Optional[str] = None, exposed: bool = True):
        self.name = name
        self.exposed = exposed

    def __ror__(self, model) -> DataField:
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        model.__setattr__(SETTING_ANNOTATION_ATTRIBUTE_NAME, self)
        return model
