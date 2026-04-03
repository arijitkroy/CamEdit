from abc import ABC, abstractmethod
import numpy as np

class BaseFilter(ABC):
    def __init__(self, name="BaseFilter"):
        self.name = name
        self.enabled = False
        
    @abstractmethod
    def apply(self, frame: np.ndarray) -> np.ndarray:
        """
        Takes an image as a NumPy BGR array and returns the modified image.
        """
        pass
    
    def set_enabled(self, state: bool):
        self.enabled = state
