from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class TimeFormatEnum(enum.Enum):
    HHu_00003amm = "HH:mm"
    hu_00003ammu_000020A = "h:mm A"
