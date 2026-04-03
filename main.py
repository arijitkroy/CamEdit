import sys
import os
import warnings

# Add project root to sys.path
# Suppress warnings and TensorFlow Lite logging
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["GLOG_minloglevel"] = "3"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.engine import VideoEngine
from core.filter_chain import FilterChain
from filters.color_filter import ColorFilter
from filters.face_focus import FaceFocusFilter
from filters.eye_contact import EyeContactFilter
from filters.upscale_filter import UpscaleFilter
from ui.app_window import AppWindow

def main():
    # 1. Initialize filters
    color_filter = ColorFilter()
    face_focus = FaceFocusFilter()
    eye_contact = EyeContactFilter()
    upscale = UpscaleFilter()
    
    # 2. Setup Chain
    chain = FilterChain()
    chain.add_filter(color_filter)
    chain.add_filter(face_focus)
    chain.add_filter(eye_contact)
    chain.add_filter(upscale)
    
    # 3. Setup Engine
    engine = VideoEngine(chain)
    
    # 4. Start GUI
    app = AppWindow(engine, chain)
    
    try:
        app.mainloop()
    finally:
        # Cleanup
        engine.stop_capture()

if __name__ == "__main__":
    main()
