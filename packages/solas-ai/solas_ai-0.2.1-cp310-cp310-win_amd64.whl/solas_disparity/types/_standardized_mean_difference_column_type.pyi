from ._enum_base import EnumBase as EnumBase

class StandardizedMeanDifferenceColumnType(EnumBase):
    TOTAL: str
    AVERAGE_LABEL: str
    AVERAGE_OUTCOME: str
    STANDARD_DEVIATION_OF_OUTCOMES: str
    SMD: str
