import cv2
import mediapipe as mp
import numpy as np
try:
    from filters.base import BaseFilter
except ImportError:
    from .base import BaseFilter

class EyeContactFilter(BaseFilter):
    def __init__(self):
        super().__init__("Eye Contact Mode")
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.intensity = 0.5 # 0.0 to 1.0
        
    def update_params(self, intensity=None):
        if intensity is not None: self.intensity = intensity
        
    def apply(self, frame: np.ndarray) -> np.ndarray:
        if self.intensity == 0:
            return frame
            
        h, w = frame.shape[:2]
        results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            return frame
        
        landmarks = results.multi_face_landmarks[0].landmark
        processed = frame.copy()
        
        # Eye socket and Iris landmarks
        # Left Eye socket roughly: 33, 133
        # Right Eye socket roughly: 362, 263
        eye_pairs = [
            {"iris": 468, "corners": [33, 133]}, # Left
            {"iris": 473, "corners": [362, 263]} # Right
        ]
        
        for pair in eye_pairs:
            iris = landmarks[pair["iris"]]
            c1 = landmarks[pair["corners"][0]]
            c2 = landmarks[pair["corners"][1]]
            
            # Real-world target is the center of the eye socket
            target_x = (c1.x + c2.x) / 2.0
            target_y = (c1.y + c2.y) / 2.0
            
            # Vector from iris to target
            dx = (target_x - iris.x) * w
            dy = (target_y - iris.y) * h
            
            ix, iy = int(iris.x * w), int(iris.y * h)
            radius = int(0.025 * w) # Region of influence
            
            # Localized warp: pull pixels in 'radius' towards (ix + dx, iy + dy)
            # using a simple displacement map
            y_start, y_end = max(0, iy-radius), min(h, iy+radius)
            x_start, x_end = max(0, ix-radius), min(w, ix+radius)
            
            roi = processed[y_start:y_end, x_start:x_end]
            if roi.size == 0: continue
            
            # Create a meshgrid for the ROI
            rows, cols = roi.shape[:2]
            map_x, map_y = np.meshgrid(np.arange(cols), np.arange(rows))
            map_x = map_x.astype(np.float32)
            map_y = map_y.astype(np.float32)
            
            # Calculate distance from center of ROI
            dist_x = map_x - cols/2
            dist_y = map_y - rows/2
            dist = np.sqrt(dist_x**2 + dist_y**2)
            
            # Weight function (gaussian-like) so only the center moves
            weight = np.exp(-(dist**2) / (2 * (radius/2)**2))
            
            # Apply displacement scaled by intensity
            map_x -= dx * weight * self.intensity
            map_y -= dy * weight * self.intensity
            
            # Remap the ROI
            warped_roi = cv2.remap(roi, map_x, map_y, cv2.INTER_LINEAR)
            processed[y_start:y_end, x_start:x_end] = warped_roi
            
        return processed
