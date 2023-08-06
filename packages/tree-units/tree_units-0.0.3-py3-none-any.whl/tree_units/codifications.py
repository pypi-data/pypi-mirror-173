from typing import Iterator, Union

from pydantic import BaseModel, Field

from .resources import CitationAffector, Node, StatuteAffector, generic_mp


class CodeBaseMP(BaseModel):
    """Contains common fields for all tables that will reference the `codification_id` and its `material_path`. The `material_path` is the same identifier as the `id` of a `CodeUnit`."""

    codification_id: str
    material_path: str = generic_mp


class CodeUnit(Node):
    """Specific unit for Codification objects. Unlike a Statute which needs to be pre-processed, a Codification is human edited. A Codification is an attempt to unify disconnected Statutes into a single entity. For instance, the `Family Code of the Philippines` is contained in Executive Order No. 209 (1987). However it has since been amended by various laws such as Republic Act No. 8533 (1998) and Republic Act No. 10572 (2013) among others. In light of the need to record a history, each Codification may contain a `history` field."""

    id: str = generic_mp
    history: list[Union[CitationAffector, StatuteAffector]] | None = Field(
        None,
        title="Unit History",
        description="Used in Codifications to show each statute or citation affecting the unit.",
    )
    units: list["CodeUnit"] = Field(None)

    @classmethod
    def create_branches(
        cls, units: list[dict], parent_id: str = "1."
    ) -> Iterator["CodeUnit"]:
        """Each material path tree begins with a root of 1. (see prep_root()) so that each branch will be a material path to the root."""
        for counter, u in enumerate(units, start=1):
            children = []  # default unit being evaluated
            id = f"{parent_id}{str(counter)}."
            history = u.pop("history", None)
            if subunits := u.pop("units", None):  # potential children
                children = list(cls.create_branches(subunits, id))  # recursive
            yield CodeUnit(
                **u,
                id=id,
                history=history,
                units=children,
            )
