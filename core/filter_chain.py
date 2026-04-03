import numpy as np
from typing import List
try:
    from filters.base import BaseFilter
except ImportError:
    from .base import BaseFilter

class FilterChain:
    def __init__(self):
        self.filters: List[BaseFilter] = []
        
    def add_filter(self, filter_obj: BaseFilter):
        self.filters.append(filter_obj)
        
    def apply_all(self, frame: np.ndarray) -> np.ndarray:
        """
        Sequentially apply all enabled filters.
        """
        processed_frame = frame.copy()
        for f in self.filters:
            if f.enabled:
                processed_frame = f.apply(processed_frame)
        return processed_frame
