from ._enum_base import EnumBase as EnumBase

class OddsRatioColumnType(EnumBase):
    TOTAL: str
    LABEL_FAVORABLE: str
    PERCENT_LABEL_FAVORABLE: str
    LABEL_ODDS: str
    FAVORABLE: str
    PERCENT_FAVORABLE: str
    ODDS: str
    PERCENT_DIFFERENCE_FAVORABLE: str
    ODDS_RATIO: str
