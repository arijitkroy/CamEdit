import cv2
import numpy as np
try:
    from filters.base import BaseFilter
except ImportError:
    from .base import BaseFilter

class UpscaleFilter(BaseFilter):
    def __init__(self):
        super().__init__("Image Sharpening")
        self.sharpen_strength = 0.5 # 0.0 to 1.0
        
    def apply(self, frame: np.ndarray) -> np.ndarray:
        # Kernel for sharpening
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]]) * self.sharpen_strength + \
                 np.array([[0, 0, 0],
                           [0, 1, 0],
                           [0, 0, 0]]) * (1 - self.sharpen_strength)
                           
        sharpened = cv2.filter2D(frame, -1, kernel)
        return sharpened

    def update_params(self, sharpen_strength=None):
        if sharpen_strength is not None: self.sharpen_strength = sharpen_strength
