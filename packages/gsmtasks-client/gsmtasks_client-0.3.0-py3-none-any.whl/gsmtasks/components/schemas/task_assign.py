from __future__ import annotations

import typing
import lapidary_base
import pydantic
import gsmtasks.components.schemas.location
import lapidary_base.absent


class TaskAssign(pydantic.BaseModel):
    notes: typing.Annotated[
        typing.Union[
            str,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    location: typing.Annotated[
        typing.Union[
            gsmtasks.components.schemas.location.Location,
            None,
            lapidary_base.absent.Absent,
        ],
        pydantic.Field(),
    ] = lapidary_base.absent.ABSENT

    assignee: typing.Annotated[str, pydantic.Field()]

    class Config(pydantic.BaseConfig):
        use_enum_values = True
        extra = pydantic.Extra.allow


TaskAssign.update_forward_refs()
