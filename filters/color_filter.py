import cv2
import numpy as np
try:
    from filters.base import BaseFilter
except ImportError:
    from .base import BaseFilter

class ColorFilter(BaseFilter):
    def __init__(self):
        super().__init__("Color Enhancements")
        self.brightness = 0.0 # -100 to 100
        self.contrast = 0.0   # -100 to 100
        self.saturation = 1.0 # 0.0 to 3.0
        
    def apply(self, frame: np.ndarray) -> np.ndarray:
        # 1. Brightness & Contrast
        # Contrast: alpha = (contrast+100)/100
        # Brightness: beta = brightness
        alpha = (self.contrast + 100) / 100.0
        beta = self.brightness
        
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        
        # 2. Saturation
        if self.saturation != 1.0:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
            hsv[:, :, 1] = hsv[:, :, 1] * self.saturation
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            
        return frame

    def update_params(self, brightness=None, contrast=None, saturation=None):
        if brightness is not None: self.brightness = brightness
        if contrast is not None: self.contrast = contrast
        if saturation is not None: self.saturation = saturation
