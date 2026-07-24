from dataclasses import dataclass
from typing import Callable, Optional, Sequence


@dataclass(frozen=True)
class ModelSpec:
    analysis: str
    dependent: str
    xvars: Sequence[str]
    controls: Sequence[str]
    sample: str = "Full sample"
    covariance: str = "cluster_firm"
    sample_rule: Optional[Callable] = None
    entity_effects: bool = True
    time_effects: bool = True
