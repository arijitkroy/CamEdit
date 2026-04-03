import customtkinter as ctk
import cv2
from PIL import Image
from core.camera_manager import CameraManager
from ui.components import StyledSlider, FilterToggle

class AppWindow(ctk.CTk):
    def __init__(self, engine, filter_chain):
        super().__init__()
        
        self.engine = engine
        self.filter_chain = filter_chain
        
        # Window setup
        self.title("CamEdit")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left Sidebar (Controls)
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self._setup_sidebar()
        
        # Main Area (Video & Selection)
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)
        
        self._setup_top_bar()
        self._setup_video_display()
        
        # State
        self.current_cam_idx = None
        self.update_video()
        
    def _setup_top_bar(self):
        top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent", height=60)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Camera Dropdown
        self.camera_list = CameraManager.get_available_cameras()
        cam_names = [f"{name} (ID:{id})" for id, name in self.camera_list]
        
        self.cam_dropdown = ctk.CTkComboBox(top_bar, values=cam_names, 
                                          width=250, command=self._on_settings_change)
        self.cam_dropdown.set("")
        self.cam_dropdown.pack(side="left", padx=10)
        
        # Resolution Dropdown
        self.res_list = ["640x480 (SD)", "1280x720 (HD)", "1920x1080 (FHD)", "2560x1440 (2K)"]
        self.res_dropdown = ctk.CTkComboBox(top_bar, values=self.res_list, 
                                          width=150, command=self._on_settings_change)
        self.res_dropdown.set(self.res_list[0])
        self.res_dropdown.pack(side="left", padx=10)
        
        # Start/Stop Button
        self.btn_vcam = ctk.CTkButton(top_bar, text="Enable Virtual Cam", 
                                     fg_color="#3A7EBF", command=self._toggle_vcam)
        self.btn_vcam.pack(side="right", padx=10)
        
    def _setup_video_display(self):
        # Placeholder or Video Label
        self.video_container = ctk.CTkFrame(self.main_area, fg_color="#1a1a1a", corner_radius=12)
        self.video_container.grid(row=1, column=0, sticky="nsew")
        self.video_container.grid_rowconfigure(0, weight=1)
        self.video_container.grid_columnconfigure(0, weight=1)
        
        self.video_label = ctk.CTkLabel(self.video_container, text="Select Camera to Start", 
                                       font=("Outfit", 16), text_color="#555555")
        self.video_label.grid(row=0, column=0)
        
    def _setup_sidebar(self):
        # Title
        lbl_title = ctk.CTkLabel(self.sidebar, text="MODIFIER PANEL", font=("Outfit Bold", 20), text_color="#3A7EBF")
        lbl_title.pack(pady=(30, 20), padx=20, anchor="w")
        
        # 1. Color Enhancement
        color_filter = self.filter_chain.filters[0] # Assuming first
        
        lbl_sec1 = ctk.CTkLabel(self.sidebar, text="Color Correction", font=("Outfit", 14, "bold"))
        lbl_sec1.pack(padx=20, anchor="w", pady=(10, 5))
        
        s1 = StyledSlider(self.sidebar, "Brightness", -100, 100, 0, lambda v: color_filter.update_params(brightness=v))
        s1.pack(fill="x", padx=15, pady=5)
        
        s2 = StyledSlider(self.sidebar, "Contrast", -100, 100, 0, lambda v: color_filter.update_params(contrast=v))
        s2.pack(fill="x", padx=15, pady=5)
        
        s3 = StyledSlider(self.sidebar, "Saturation", 0.0, 3.0, 1.0, lambda v: color_filter.update_params(saturation=v))
        s3.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(self.sidebar, text="").pack(pady=10) # Spacer
        
        # 2. AI Toggles
        # Face Focus
        f_filter = self.filter_chain.filters[1]
        
        self.s_zoom = StyledSlider(self.sidebar, "Zoom Level", 0.5, 2.0, 1.0, lambda v: f_filter.update_params(zoom_level=v))
        self.s_sens = StyledSlider(self.sidebar, "Sensitivity", 0.01, 1.0, 0.5, lambda v: f_filter.update_params(sensitivity=v))
        
        def toggle_face_focus(v):
            f_filter.set_enabled(v)
            if v:
                self.s_zoom.pack(fill="x", padx=15, pady=0)
                self.s_sens.pack(fill="x", padx=15, pady=(0, 10))
            else:
                self.s_zoom.pack_forget()
                self.s_sens.pack_forget()
                
        self.tg1 = FilterToggle(self.sidebar, "Auto Face Focus", toggle_face_focus)
        self.tg1.pack(fill="x", padx=20, pady=5)
        
        # Eye Contact
        e_filter = self.filter_chain.filters[2]
        
        self.s_eye = StyledSlider(self.sidebar, "Correction Intensity", 0.0, 1.0, 0.5, lambda v: e_filter.update_params(intensity=v))
        
        def toggle_eye_contact(v):
            e_filter.set_enabled(v)
            if v:
                self.s_eye.pack(fill="x", padx=15, pady=(0, 10))
            else:
                self.s_eye.pack_forget()

        self.tg2 = FilterToggle(self.sidebar, "Eye Contact Mode", toggle_eye_contact)
        self.tg2.pack(fill="x", padx=20, pady=5)
        
        # Image Sharpening
        u_filter = self.filter_chain.filters[3]
        
        self.u_slider = StyledSlider(self.sidebar, "Sharpening", 0.0, 1.0, 0.5, lambda v: u_filter.update_params(sharpen_strength=v))
        
        def toggle_sharpening(v):
            u_filter.set_enabled(v)
            if v:
                self.u_slider.pack(fill="x", padx=15, pady=0)
            else:
                self.u_slider.pack_forget()

        self.tg3 = FilterToggle(self.sidebar, "Image Sharpening", toggle_sharpening)
        self.tg3.pack(fill="x", padx=20, pady=5)
        
        # FPS Settings
        ctk.CTkLabel(self.sidebar, text="").pack(pady=5)
        lbl_fps = ctk.CTkLabel(self.sidebar, text="Target Output FPS", font=("Outfit", 12))
        lbl_fps.pack(padx=20, anchor="w")
        
        self.fps_dropdown = ctk.CTkComboBox(self.sidebar, values=["15", "24", "30", "60"], 
                                          command=self._on_settings_change)
        self.fps_dropdown.set("30")
        self.fps_dropdown.pack(fill="x", padx=15, pady=5)
        
        self.filter_chain.filters[0].set_enabled(True) # Color is always enabled
        
    def _on_settings_change(self, *args):
        # Triggered by Camera choice, Resolution choice, or FPS option
        cam_choice = self.cam_dropdown.get()
        if not cam_choice: return
        
        res_choice = self.res_dropdown.get().split(" ")[0] # e.g. 1920x1080
        w, h = map(int, res_choice.split("x"))
        
        fps = int(self.fps_dropdown.get())
        cam_id = int(cam_choice.split("(ID:")[1][:-1])
        
        if self.engine.start_capture(cam_id, width=w, height=h, fps=fps):
            self.video_label.configure(text="")
            
    def _toggle_vcam(self):
        state = not self.engine.vcam_enabled
        self.engine.set_vcam_state(state)
        self.btn_vcam.configure(text="Disable Virtual Cam" if state else "Enable Virtual Cam",
                               fg_color="#BF3A3A" if state else "#3A7EBF")

    def update_video(self):
        frame = self.engine.latest_frame
        if frame is not None:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            
            # Scale to fit label
            container_w = self.video_container.winfo_width()
            container_h = self.video_container.winfo_height()
            
            if container_w > 1: # Window is rendered
                img.thumbnail((container_w, container_h), Image.Resampling.LANCZOS)
                
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.video_label.configure(image=ctk_img, text="")
            self.video_label.image = ctk_img
            
        self.after(15, self.update_video)
