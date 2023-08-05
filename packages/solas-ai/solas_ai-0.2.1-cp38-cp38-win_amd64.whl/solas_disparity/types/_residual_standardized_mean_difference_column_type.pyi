from ._enum_base import EnumBase as EnumBase

class ResidualStandardizedMeanDifferenceColumnType(EnumBase):
    TOTAL: str
    AVERAGE_PREDICTION: str
    AVERAGE_LABEL: str
    AVERAGE_RESIDUAL: str
    STANDARD_DEVIATION_OF_RESIDUALS: str
    RESIDUAL_SMD: str
