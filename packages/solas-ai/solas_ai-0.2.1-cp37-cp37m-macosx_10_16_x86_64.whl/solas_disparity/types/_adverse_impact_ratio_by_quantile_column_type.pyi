from ._enum_base import EnumBase as EnumBase

class AdverseImpactRatioByQuantileColumnType(EnumBase):
    TOTAL: str
    LABEL_FAVORABLE: str
    PERCENT_LABEL_FAVORABLE: str
    FAVORABLE: str
    PERCENT_FAVORABLE: str
    PERCENT_DIFFERENCE_FAVORABLE: str
    AIR: str
