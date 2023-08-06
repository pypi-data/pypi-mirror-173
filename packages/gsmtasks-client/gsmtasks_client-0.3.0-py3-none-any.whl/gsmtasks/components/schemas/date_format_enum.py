from __future__ import annotations

import typing
import lapidary_base
import pydantic
import enum


class DateFormatEnum(enum.Enum):
    dotted = "DD.MM.YYYY"
    iso = "YYYY-MM-DD"
    dmy = "DD/MM/YYYY"
    us = "MM/DD/YYYY"
