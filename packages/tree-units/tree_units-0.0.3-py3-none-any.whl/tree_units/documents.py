from typing import Iterator, Union

from pydantic import BaseModel, Field

from .resources import EventCitation, EventStatute, FTSQuery, Node, generic_mp
from .utils import Layers


class DocBaseMP(BaseModel):
    """Contains common fields for all tables that will reference the `document_id` and the `material_path`. The `material_path` is the same identifier as the `id` of a `DocUnit`."""

    document_id: str
    material_path: str = generic_mp


class DocUnit(Node):
    """Specific unit for Document objects."""

    id: str = generic_mp
    sources: list[Union[EventStatute, EventCitation, FTSQuery]] | None = Field(
        None,
        title="Legal Basis Sources",
        description="Used in Documents to show the basis of the content node.",
    )
    units: list["DocUnit"] = Field(None)

    @classmethod
    def create_branches(
        cls,
        units: list[dict],
        parent_id: str = "1.",
    ) -> Iterator["DocUnit"]:
        """Each material path tree begins with a root of 1. (see prep_root()) so that each branch will be a material path to the root."""
        if parent_id == "1.":
            Layers.DEFAULT.layerize(units)  # in place
        for counter, u in enumerate(units, start=1):
            children = []  # default unit being evaluated
            id = f"{parent_id}{str(counter)}."
            sources = u.pop("sources", None)
            if subunits := u.pop("units", None):  # potential children
                children = list(cls.create_branches(subunits, id))  # recursive
            yield DocUnit(
                **u,
                id=id,
                sources=sources,
                units=children,
            )
