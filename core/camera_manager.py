import cv2
from pygrabber.dshow_graph import FilterGraph

class CameraManager:
    @staticmethod
    def get_available_cameras():
        """
        Returns a list of tuples (index, name).
        Prioritizes built-in or integrated cameras if identifiable.
        """
        graph = FilterGraph()
        devices = graph.get_input_devices()
        
        cameras = []
        for index, name in enumerate(devices):
            cameras.append((index, name))
            
        # Prioritize "Integrated", "Built-in", "FaceTime", or common internal names
        # Sort so that those containing such keywords are first
        priority_keywords = ["integrated", "built-in", "facetime", "hd camera", "front"]
        
        def priority_sort(cam):
            name = cam[1].lower()
            for i, kw in enumerate(priority_keywords):
                if kw in name:
                    return i # Lower number = higher priority
            return 100 # Default low priority
            
        cameras.sort(key=priority_sort)
        return cameras

if __name__ == "__main__":
    cm = CameraManager()
    print("Found Cameras (Prioritized):")
    for idx, name in cm.get_available_cameras():
        print(f"[{idx}] {name}")
