import cv2
import threading
import time
from typing import Optional
import numpy as np
import pyvirtualcam
import queue

class VideoEngine:
    def __init__(self, filter_chain):
        self.cap = None
        self.filter_chain = filter_chain
        self.frame_queue = queue.Queue(maxsize=1)
        self.running = False
        self.virtual_cam = None
        self.vcam_enabled = False
        self.current_frame = None
        self._thread = None
        
        self.target_w = 640
        self.target_h = 480
        self.target_fps = 30
        
    def start_capture(self, device_id: int, width: int = 640, height: int = 480, fps: int = 30):
        if self.running:
            self.stop_capture()
        
        self.target_w = width
        self.target_h = height
        self.target_fps = fps
        
        self.cap = cv2.VideoCapture(device_id)
        if not self.cap.isOpened():
            return False
            
        # Apply properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        
        self.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        return True
        
    def stop_capture(self):
        self.running = False
        if self._thread:
            self._thread.join()
        if self.cap:
            self.cap.release()
        if self.virtual_cam:
            self.virtual_cam.close()
            self.virtual_cam = None
            
    def set_vcam_state(self, state: bool):
        self.vcam_enabled = state
        if not state and self.virtual_cam:
            self.virtual_cam.close()
            self.virtual_cam = None

    def _run_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            
            # Apply all filters
            processed = self.filter_chain.apply_all(frame)
            self.current_frame = processed
            
            # Virtual camera output
            if self.vcam_enabled:
                if not self.virtual_cam:
                    h, w = processed.shape[:2]
                    try:
                        self.virtual_cam = pyvirtualcam.Camera(width=w, height=h, fps=30)
                        print(f"Virtual Camera Output: {self.virtual_cam.device}")
                    except Exception as e:
                        print(f"Virtual Camera failed to start: {e}")
                        self.vcam_enabled = False
                
                if self.virtual_cam:
                    # pyvirtualcam expects RGB, OpenCV is BGR
                    v_frame = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
                    self.virtual_cam.send(v_frame)
                    self.virtual_cam.sleep_until_next_frame()
            
            # Push to UI queue
            if self.frame_queue.full():
                self.frame_queue.get_nowait()
            self.frame_queue.put(processed)
            
    @property
    def latest_frame(self):
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None
