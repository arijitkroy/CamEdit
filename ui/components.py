import customtkinter as ctk

class StyledSlider(ctk.CTkFrame):
    def __init__(self, master, label, from_, to, initial, update_cb):
        super().__init__(master, fg_color="transparent")
        self.label_var = ctk.StringVar(value=f"{label}: {initial:.1f}")
        self.update_cb = update_cb
        
        lbl = ctk.CTkLabel(self, textvariable=self.label_var, font=("Outfit", 12))
        lbl.pack(side="top", anchor="w", padx=5)
        
        self.slider = ctk.CTkSlider(self, from_=from_, to=to,
                                  command=self._on_change,
                                  button_color="#3A7EBF",
                                  progress_color="#3A7EBF")
        self.slider.set(initial)
        self.slider.pack(fill="x", padx=5, pady=5)
        
    def _on_change(self, val):
        self.label_var.set(f"{self.label_var.get().split(':')[0]}: {val:.1f}")
        self.update_cb(val)

class FilterToggle(ctk.CTkFrame):
    def __init__(self, master, label, toggle_cb):
        super().__init__(master, fg_color="#2b2b2b", corner_radius=8)
        self.toggle_cb = toggle_cb
        
        lbl = ctk.CTkLabel(self, text=label, font=("Outfit Bold", 13))
        lbl.pack(side="left", padx=10, pady=10)
        
        self.switch = ctk.CTkSwitch(self, text="", command=self._on_toggle,
                                  progress_color="#3A7EBF")
        self.switch.pack(side="right", padx=10)
        
    def _on_toggle(self):
        self.toggle_cb(self.switch.get())
