from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class LocationTypeEnum(enum.Enum):
    Point = "Point"
