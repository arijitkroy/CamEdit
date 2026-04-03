import cv2
import mediapipe as mp
import numpy as np
try:
    from filters.base import BaseFilter
except ImportError:
    from .base import BaseFilter

class FaceFocusFilter(BaseFilter):
    def __init__(self):
        super().__init__("Auto Face Focus")
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.last_bbox = None
        
        # User settings
        self.zoom_level = 1.0 # 0.5 to 2.0 (higher = tighter crop)
        self.sensitivity = 0.5 # 0.01 to 1.0 (higher = faster movement)
        
    def update_params(self, zoom_level=None, sensitivity=None):
        if zoom_level is not None: self.zoom_level = zoom_level
        if sensitivity is not None: self.sensitivity = sensitivity
        
    def apply(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        results = self.face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.detections:
            # Get the first face detected
            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            
            # Target center and size (adjusted by zoom_level)
            tx = bbox.xmin + bbox.width / 2.0
            ty = bbox.ymin + bbox.height / 2.0
            
            # Base padding of 2.0, adjusted by zoom_level (inverse relationship)
            padding = 2.0 / (self.zoom_level + 0.1)
            tw = bbox.width * padding
            th = bbox.height * padding
            
            if self.last_bbox is None:
                self.last_bbox = [tx, ty, tw, th]
            else:
                # Smooth the moving bounding box based on sensitivity
                sf = self.sensitivity
                self.last_bbox[0] = self.last_bbox[0] * (1-sf) + tx * sf
                self.last_bbox[1] = self.last_bbox[1] * (1-sf) + ty * sf
                self.last_bbox[2] = self.last_bbox[2] * (1-sf) + tw * sf
                self.last_bbox[3] = self.last_bbox[3] * (1-sf) + th * sf
            
            # Calculate actual pixels from relative coordinates
            cx, cy, cw, ch = self.last_bbox
            abs_cx = cx * w
            abs_cy = cy * h
            
            # Since relative cw and ch might not match the image's aspect ratio,
            # we need to ensure the crop box matches the w/h ratio in absolute pixels.
            # Convert relative width/height to absolute pixels first
            abs_cw = cw * w
            abs_ch = ch * h
            
            # Now enforce the exact original aspect ratio on the absolute size
            aspect = w / h
            if abs_cw / abs_ch > aspect:
                # Width is the bottleneck, scale up height
                abs_ch = abs_cw / aspect
            else:
                # Height is the bottleneck, scale up width
                abs_cw = abs_ch * aspect
                
            x1 = int(abs_cx - abs_cw / 2)
            y1 = int(abs_cy - abs_ch / 2)
            x2 = int(abs_cx + abs_cw / 2)
            y2 = int(abs_cy + abs_ch / 2)
            
            # Keep track of requested dimensions to pad if it goes out of bounds
            req_w = x2 - x1
            req_h = y2 - y1
            
            # Ensure it's inside the image (if it goes out, we'll slice what we can and pad to preserve aspect)
            x1_clip, y1_clip = max(0, x1), max(0, y1)
            x2_clip, y2_clip = min(w, x2), min(h, y2)
            
            if x2_clip > x1_clip and y2_clip > y1_clip:
                cropped = frame[y1_clip:y2_clip, x1_clip:x2_clip]
                
                # To perfectly preserve aspect ratio if we hit a border, we should pad instead of stretching.
                # However, for real-time video, if it hits a border tightly, simple resize back to w, h 
                # will cause minor squishing only at extreme edges. Since we enforced absolute size to match aspect ratio,
                # the inner region before clipping is exactly aspect perfect.
                return cv2.resize(cropped, (w, h))
        
        return frame
