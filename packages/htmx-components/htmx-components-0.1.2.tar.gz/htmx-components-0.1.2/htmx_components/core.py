import json
from abc import ABC
from pathlib import Path
from typing import Iterable, Union

from pydantic import BaseModel, Extra, root_validator
from pydantic.error_wrappers import ValidationError

Child = Union[str, "AbstractElement"]


class AbstractElement(ABC, BaseModel, extra=Extra.allow):
    """An abstract base class for all HTML elements"""

    children: Union[Child, Iterable[Child]] = None

    def __str__(self):
        """Convert to an HTML string"""

        # extract all the html attributes
        attrs = self.dict()
        tag = attrs.pop("element")  # element isn't an attribute
        if "children" in attrs:
            attrs.pop("children")  # nor is children
        if "classes" in attrs:
            attrs["class"] = attrs.pop("classes")  # renamed since it's a reserved keyword
        attrs = {k.replace("_", "-"): v for k, v in attrs.items()}  # convert snake_case

        # None children should produce empty html elements
        if self.children is None:
            children = ""
        # strings are passed through without conversion
        elif isinstance(self.children, str):
            children = self.children
        # individual AbstractElements are recursively converted to strings
        elif isinstance(self.children, self.__class__.__bases__):
            children = str(self.children)
        # the only valid case remaining is an iterable of AbstractElements
        else:
            children = "\n".join(str(child) for child in self.children)

        # write out the html tag
        attr_str = " ".join(f"{key}='{value}'" for key, value in attrs.items())
        html_str = f"<{tag} {attr_str}>\n{children}\n</{tag}>"
        return html_str


def create_element(element, attrs):
    """Create a class for an HTML element given its name and valid attributes"""

    class Element(AbstractElement, extra=Extra.allow):

        element: str = element

        @root_validator(pre=True, allow_reuse=True)
        def check_field_names(cls, values):
            """Above we allow extra fields - here we validate them"""

            # check every field
            for field, value in values.items():

                # check field names are valid
                if (
                    (field not in attrs)
                    and (not field.startswith("data_"))
                    and (not field.startswith("aria_"))
                    and (field != "children")
                ):
                    raise ValidationError(f"Invalid field name {field}")

                # any field can be a string
                if isinstance(value, str):
                    continue

                # children can also be an element
                if (field == "children") and isinstance(value, (str, AbstractElement)):
                    continue

                # children can also be an iterable of strings and elements
                if (
                    (field == "children")
                    and isinstance(value, Iterable)
                    and all(isinstance(v, (str, AbstractElement)) for v in values)
                ):
                    continue

                # all other field types are invalid
                raise ValidationError(f"Invalid type for {field}")

            return values

    return Element


# create a model for each element and make it importable by name from the module's namespace
__all__ = []
thisdir = Path(__file__).parent
with open(thisdir / "classes.json") as f:
    classes = json.load(f)
for element, attrs in classes.items():
    cls = element.title()
    globals()[cls] = create_element(element, attrs)
    __all__.append(cls)
