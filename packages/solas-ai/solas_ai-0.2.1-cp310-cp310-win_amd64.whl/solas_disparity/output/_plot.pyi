from plotly.graph_objects import Figure as Figure
from solas_disparity import const as const
from solas_disparity.const import COLORS as COLORS
from solas_disparity.types import DisparityCalculation as DisparityCalculation
from solas_disparity.types._adverse_impact_ratio_by_quantile_column_type import AdverseImpactRatioByQuantileColumnType as AdverseImpactRatioByQuantileColumnType
from solas_disparity.types._adverse_impact_ratio_column_type import AdverseImpactRatioColumnType as AdverseImpactRatioColumnType
from solas_disparity.types._categorical_adverse_impact_ratio_column_type import CategoricalAdverseImpactRatioColumnType as CategoricalAdverseImpactRatioColumnType
from solas_disparity.types._odds_ratio_column_type import OddsRatioColumnType as OddsRatioColumnType
from solas_disparity.types._residual_standardized_mean_difference_column_type import ResidualStandardizedMeanDifferenceColumnType as ResidualStandardizedMeanDifferenceColumnType
from solas_disparity.types._standardized_mean_difference_column_type import StandardizedMeanDifferenceColumnType as StandardizedMeanDifferenceColumnType
from solas_disparity.ui import autoformatter as autoformatter
from typing import Optional

class plot:
    def __init__(self, disp) -> None: ...
    def __call__(self, column: Optional[str] = ..., group: Optional[str] = ..., condense: Optional[bool] = ..., top_n_segments: Optional[int] = ...) -> Figure: ...
