from typing import Iterator

from pydantic import BaseModel, Field

from .resources import Node, generic_mp
from .utils import has_short_title


class StatuteBaseMP(BaseModel):
    """Contains common fields for all tables that will reference the `statute_id` and the `material_path`"""

    statute_id: str
    material_path: str = generic_mp


class StatuteUnit(Node):
    """Specific unit for Statute objects. The `short_title` is used as a special field to look for the statute's title within the provisions."""

    id: str = generic_mp
    short_title: str | None = Field(
        None,
        description="Some unit captions / content signify a title.",
        max_length=500,
    )
    units: list["StatuteUnit"] | None = Field(None)

    @classmethod
    def create_branches(
        cls,
        units: list[dict],
        parent_id: str = "1.",
    ) -> Iterator["StatuteUnit"]:
        """Each material path tree begins with a root of 1. (see prep_root()) so that each branch will be a material path to the root."""
        for counter, u in enumerate(units, start=1):
            short = None
            children = []  # default unit being evaluated
            id = f"{parent_id}{str(counter)}."
            short = has_short_title(u)
            if subunits := u.pop("units", None):  # potential children
                children = list(cls.create_branches(subunits, id))  # recursive
            yield StatuteUnit(**u, id=id, short_title=short, units=children)

    @classmethod
    def extract_titles(cls, nodes: list["StatuteUnit"]) -> Iterator[str]:
        for node in nodes:
            if node.short_title:
                yield node.short_title
            if node.units:
                yield from cls.extract_titles(node.units)

    @classmethod
    def get_first_title(cls, nodes: list["StatuteUnit"]) -> str | None:
        titles = cls.extract_titles(nodes)
        title_list = list(titles)
        if title_list:
            return title_list[0]
        return None
