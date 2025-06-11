# first go download ollama and do some stuff there are tutorials in youtube so when you add your api then take a random photo maybe your with your friend baking cake then add path to code thats all is there is problem contact with me cahadabdulla@gmail.com I will answer you questions İ üish you nice day~Jahad
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
import pyttsx3
import threading
import speech_recognition as sr
import requests
import json
import subprocess
import time
import cv2
from datetime import datetime
import os
import math
import tkinter as tk

class LYNXAssistant:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("L.Y.N.X")
        
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        self.app.geometry(f"{screen_width}x{screen_height}+0+0")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.cap = None
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        
        self.is_listening = False
        self.camera_active = False
        self.camera_thread = None
        
        # Wave animation variables
        self.wave_offset = 0
        self.wave_canvas = None
        self.camera_frame_widget = None
        
        self.setup_ui()
        self.setup_bindings()
        
        self.speak("System is online, sir.")
    
    def setup_ui(self):
        self.bg = ctk.CTkFrame(self.app, fg_color="black")
        self.bg.pack(fill="both", expand=True)
        
        self.create_wave_background()
        self.create_title()
        self.create_logo()
        self.create_camera_display()
        self.create_chatbox()
        self.create_buttons()
    
    def create_wave_background(self):
        """Create animated wave background behind the logo"""
        self.wave_canvas = tk.Canvas(
            self.bg, 
            width=800, 
            height=600, 
            bg='black', 
            highlightthickness=0
        )
        self.wave_canvas.place(relx=1.0, rely=1.0, anchor="center")
        
        # Start wave animation
        self.animate_waves()
    
    def animate_waves(self):
        """Create animated wave effect"""
        try:
            self.wave_canvas.delete("wave")
            
            canvas_width = 800
            canvas_height = 600
            center_x = canvas_width // 2
            center_y = canvas_height // 2
            
            # Create multiple wave rings
            for ring in range(5):
                radius_base = 50 + ring * 40
                
                # Create wave points
                points = []
                for angle in range(0, 360, 10):
                    radian = math.radians(angle)
                    
                    # Create wave effect with sine function
                    wave_amplitude = 15 * math.sin(math.radians(self.wave_offset + ring * 30))
                    radius = radius_base + wave_amplitude * math.sin(radian * 4 + self.wave_offset * 0.1)
                    
                    x = center_x + radius * math.cos(radian)
                    y = center_y + radius * math.sin(radian)
                    
                    points.extend([x, y])
                
                # Color gradient for rings
                opacity = max(0.1, 0.5 - ring * 0.08)
                color_intensity = int(255 * opacity)
                
                if ring % 2 == 0:
                    color = f"#{0:02x}{color_intensity:02x}{color_intensity:02x}"  # Cyan-ish
                else:
                    color = f"#{color_intensity:02x}{color_intensity:02x}{255:02x}"  # Blue-ish
                
                # Draw the wave ring
                if len(points) >= 6:  # Need at least 3 points (6 coordinates)
                    self.wave_canvas.create_polygon(
                        points, 
                        fill="", 
                        outline=color, 
                        width=2, 
                        tags="wave",
                        smooth=True
                    )
            
            # Update wave offset for animation
            self.wave_offset += 5
            if self.wave_offset >= 360:
                self.wave_offset = 0
            
            # Schedule next frame
            self.app.after(50, self.animate_waves)
            
        except Exception as e:
            print(f"Wave animation error: {e}")
            # Retry after a delay if there's an error
            self.app.after(100, self.animate_waves)
    
    def create_title(self):
        frame = ctk.CTkFrame(self.bg, fg_color="transparent")
        frame.place(relx=0.5, rely=0.01, anchor="n")
        
        parts = [
            ("L", "cyan"),
            ("ive ", "white"),
            ("Y", "cyan"),
            ("our ", "white"),
            ("N", "cyan"),
            ("ext ", "white"),
            ("X", "cyan"),
            ("perience", "white"),
        ]
        
        for i, (text, color) in enumerate(parts):
            lbl = ctk.CTkLabel(
                frame, 
                text=text, 
                text_color=color,
                font=("Orbitron", 18, "bold"),
                bg_color="transparent"
            )
            lbl.grid(row=0, column=i, padx=1)
    
    def create_logo(self):
        try:
            logo_path = r"C:\Users\User\Downloads\ChatGPT_Image_Jun_10__2025__02_00_12_PM-removebg-preview.png"
            if os.path.exists(logo_path):
                self.original_logo_img = Image.open(logo_path)
                self.original_logo_img = self.original_logo_img.resize((400, 400), Image.Resampling.LANCZOS)
            else:
                # Create a futuristic placeholder logo
                self.original_logo_img = self.create_placeholder_logo()
        except Exception as e:
            print(f"Logo error: {e}")
            self.original_logo_img = self.create_placeholder_logo()
        
        self.logo_photo = ctk.CTkImage(self.original_logo_img, size=(400, 400))
        self.logo_label = ctk.CTkLabel(
            self.bg, 
            image=self.logo_photo, 
            text="",
            bg_color="transparent"
        )
        self.logo_label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.animate_logo()
    
    def create_placeholder_logo(self):
        """Create a futuristic placeholder logo if the original isn't found"""
        img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw concentric circles for a futuristic look
        center = 200
        colors = [(0, 255, 255, 100), (0, 200, 255, 80), (0, 150, 255, 60)]
        
        for i, color in enumerate(colors):
            radius = 150 - i * 30
            draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                        outline=color, width=3)
        
        return img
    
    def create_camera_display(self):
        """Create camera display area near the logo"""
        self.camera_frame = ctk.CTkFrame(
            self.bg,
            width=320,
            height=240,
            fg_color=("#1a1a1a", "#0d1117"),
            corner_radius=15,
            border_width=2,
            border_color=("#00ff41", "#00dd35")
        )
        self.camera_frame.place(relx=0.87, rely=0.18, anchor="center")
        
        # Camera status label
        self.camera_status_label = ctk.CTkLabel(
            self.camera_frame,
            text="LYNX VISION\nOFFLINE",
            font=("Orbitron", 14, "bold"),
            text_color=("#666666", "#555555")
        )
        self.camera_status_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Camera display label (hidden initially)
        self.camera_display_label = ctk.CTkLabel(
            self.camera_frame,
            text="",
            width=300,
            height=220
        )
        self.camera_display_label.place(relx=0.5, rely=0.5, anchor="center")
        self.camera_display_label.place_forget()  # Hide initially
    
    def create_chatbox(self):
        # Enhanced chatbox with better styling
        chatbox_frame = ctk.CTkFrame(
            self.bg, 
            fg_color=("#1a1a1a", "#0d1117"),
            corner_radius=15,
            border_width=2,
            border_color=("#00ffff", "#00cccc"),
            width=780,
            height=220
        )
        chatbox_frame.place(relx=0.1, rely=0.95, anchor="s", y=0)
        
        self.chatbox = ctk.CTkTextbox(
            chatbox_frame, 
            height=760, 
            width=250, 
            font=("Consolas", 12),
            fg_color="transparent",
            text_color=("#00ff00", "#00ff00"),
            corner_radius=10
        )
        self.chatbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.chatbox.configure(state="disabled")
    
    def create_buttons(self):
        # Main button container
        main_button_frame = ctk.CTkFrame(self.bg, fg_color="transparent")
        main_button_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        # Create horizontal layout with settings, talk, and exit buttons
        button_row = ctk.CTkFrame(main_button_frame, fg_color="transparent")
        button_row.pack(pady=(0, 15))
        
        # Settings button (left)
        self.settings_btn = ctk.CTkButton(
            button_row,
            text="⚙️\nSETTINGS",
            command=self.open_settings,
            font=("Orbitron", 12, "bold"),
            width=120,
            height=80,
            fg_color=("#ff6b35", "#dd5a2e"),
            hover_color=("#dd5a2e", "#bb4d26"),
            corner_radius=20,
            text_color="white",
            border_width=2,
            border_color=("#ffffff", "#ffffff")
        )
        self.settings_btn.pack(side="left", padx=(0, 20))
        
        # Main talk button (center)
        self.talk_btn = ctk.CTkButton(
            button_row,
            text="🎤\nTALK TO LYNX",
            command=self.start_conversation,
            font=("Orbitron", 20, "bold"),
            width=300,
            height=80,
            fg_color=("#00ffff", "#00dddd"),
            hover_color=("#00dddd", "#00bbbb"),
            text_color=("black", "black"),
            corner_radius=25,
            border_width=3,
            border_color=("#ffffff", "#ffffff")
        )
        self.talk_btn.pack(side="left", padx=10)
        
        # Exit button (right)
        self.exit_btn = ctk.CTkButton(
            button_row,
            text="🚪\nEXIT",
            command=self.safe_exit,
            font=("Orbitron", 12, "bold"),
            width=120,
            height=80,
            fg_color=("#ff4757", "#dd3e4a"),
            hover_color=("#dd3e4a", "#bb343f"),
            corner_radius=20,
            text_color="white",
            border_width=2,
            border_color=("#ffffff", "#ffffff")
        )
        self.exit_btn.pack(side="left", padx=(20, 0))
        
        # Camera button (below, centered)
        self.cam_btn = ctk.CTkButton(
            main_button_frame,
            text="📹 LYNX VISION",
            command=self.toggle_camera,
            font=("Orbitron", 16, "bold"),
            width=250,
            height=55,
            fg_color=("#00ff41", "#00dd35"),
            hover_color=("#00dd35", "#00bb2a"),
            corner_radius=20,
            text_color=("black", "black"),
            border_width=2,
            border_color=("#ffffff", "#ffffff")
        )
        self.cam_btn.pack(pady=(0, 10))
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(main_button_frame, fg_color="transparent")
        self.status_frame.pack()
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="● SYSTEM READY",
            font=("Orbitron", 12, "bold"),
            text_color=("#00ff41", "#00dd35")
        )
        self.status_label.pack()
        
        # Animate buttons
        self.animate_buttons()
    
    def animate_buttons(self):
        """Add subtle pulsing animation to main button"""
        try:
            current_time = time.time()
            pulse = 0.95 + 0.05 * math.sin(current_time * 3)
            
            # This creates a subtle size variation effect
            # Note: CustomTkinter doesn't support real-time size changes easily,
            # so we'll use color pulsing instead
            
            pulse_color_r = int(255 * pulse)
            pulse_color_g = int(255 * pulse)
            pulse_color = f"#{0:02x}{pulse_color_r:02x}{pulse_color_g:02x}"
            
            if hasattr(self, 'talk_btn'):
                self.talk_btn.configure(border_color=pulse_color)
            
            self.app.after(50, self.animate_buttons)
            
        except Exception as e:
            print(f"Button animation error: {e}")
            self.app.after(100, self.animate_buttons)
    
    def open_settings(self):
        """Placeholder for settings functionality"""
        self.speak("Settings panel not implemented yet, sir.")
        self.update_chatbox("LYNX: Settings functionality coming soon!")
    
    def safe_exit(self):
        """Safe exit with confirmation"""
        self.speak("Shutting down systems. Goodbye, sir.")
        self.stop_camera()  # Make sure camera is stopped before exit
        self.app.after(2000, self.app.quit)  # Wait 2 seconds before closing
    
    def setup_bindings(self):
        self.app.bind("<F11>", self.toggle_fullscreen)
        self.app.bind("<Escape>", self.end_fullscreen)
        self.app.bind("<KeyPress-space>", self.on_space_press)
        self.app.bind("<KeyRelease-space>", self.on_space_release)
        self.app.focus_set()  # Ensure the app can receive key events
    
    def animate_logo(self, scale=1.0, growing=True):
        try:
            new_size = int(400 * scale)
            # Update CTkImage size instead of PIL image
            self.logo_photo = ctk.CTkImage(self.original_logo_img, size=(new_size, new_size))
            self.logo_label.configure(image=self.logo_photo)
            
            step = 0.005  # Slower, more subtle animation
            delay = 30
            
            if growing:
                if scale < 1.04:
                    self.app.after(delay, lambda: self.animate_logo(scale + step, True))
                else:
                    self.app.after(delay, lambda: self.animate_logo(scale - step, False))
            else:
                if scale > 0.96:
                    self.app.after(delay, lambda: self.animate_logo(scale - step, False))
                else:
                    self.app.after(delay, lambda: self.animate_logo(scale + step, True))
        except Exception as e:
            print(f"Logo animation error: {e}")
    
    def speak(self, text):
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
        
        self.update_chatbox(f"LYNX: {text}")
        threading.Thread(target=_speak, daemon=True).start()
    
    def listen(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.update_chatbox("LYNX: Listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            self.speak("Speech recognition service error.")
            return ""
        except Exception as e:
            print(f"Listening error: {e}")
            return ""
    
    def update_chatbox(self, message):
        try:
            self.chatbox.configure(state="normal")
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.chatbox.insert("end", f"[{timestamp}] {message}\n")
            self.chatbox.configure(state="disabled")
            self.chatbox.yview("end")
        except Exception as e:
            print(f"Chatbox error: {e}")
    
    def query_ollama(self, prompt):
        messages = [
            {"role": "system", "content": "You are LYNX, a futuristic AI assistant for Mr.Jahad. Only reply clearly, wisely, and helpfully."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = requests.post(
                "http://localhost:11434/api/chat", 
                json={
                    "model": "mistral",
                    "messages": messages,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                return "API error occurred."
        except requests.exceptions.ConnectionError:
            return "Cannot connect to Ollama. Please make sure it's running."
        except requests.exceptions.Timeout:
            return "Request timed out."
        except Exception as e:
            print(f"API error: {e}")
            return "API connection failed."
    
    def run_command(self, response):
        try:
            data = json.loads(response)
            if data.get("action") == "open":
                target = data.get("target", "")
                if target:
                    subprocess.Popen(f"{target}.exe")
                    return f"{target.capitalize()} launched."
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"Command error: {e}")
        
        return response
    
    def activate_jarvis(self):
        if self.is_listening:
            return
        
        self.is_listening = True
        
        try:
            command = self.listen().lower()
            if not command:
                return
            
            self.update_chatbox(f"You: {command}")
            
            if any(keyword in command for keyword in ["what time is it", "current time", "tell the time", "time"]):
                current_time = datetime.now().strftime("%H:%M")
                self.speak(f"The time is {current_time}, sir")
                return
            
            elif any(keyword in command for keyword in ["what is the date", "what day is it", "date"]):
                today = datetime.now().strftime("%A, %B %d, %Y")
                self.speak(f"Today is {today}")
                return
            
            elif any(keyword in command for keyword in ["exit", "quit", "goodbye", "bye"]):
                self.safe_exit()
                return
            
            response = self.query_ollama(command)
            result = self.run_command(response)
            self.speak(result)
            
        except Exception as e:
            print(f"Activation error: {e}")
            self.speak("Sorry, an error occurred.")
        finally:
            self.is_listening = False
    
    def start_conversation(self):
        if not self.is_listening:
            threading.Thread(target=self.activate_jarvis, daemon=True).start()
    
    def toggle_camera(self):
        """Toggle camera on/off"""
        if self.camera_active:
            self.stop_camera()
        else:
            self.start_camera()
    
    def start_camera(self):
        """Start the camera feed"""
        if self.camera_active:
            return
        
        self.camera_active = True
        self.camera_status_label.configure(
            text="LYNX VISION\nONLINE", 
            text_color=("#00ff41", "#00dd35")
        )
        self.cam_btn.configure(text="📹 STOP VISION")
        
        # Start camera in a separate thread
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
        
        self.speak("LYNX Vision activated")
    
    def stop_camera(self):
        """Stop the camera feed"""
        if not self.camera_active:
            return
        
        self.camera_active = False
        self.camera_status_label.configure(
            text="LYNX VISION\nOFFLINE", 
            text_color=("#666666", "#555555")
        )
        self.cam_btn.configure(text="📹 LYNX VISION")
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # Hide camera display and show status
        self.camera_display_label.place_forget()
        self.camera_status_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.speak("LYNX Vision deactivated")
    
    def camera_loop(self):
        """Main camera loop for live feed"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.speak("Camera could not be opened")
                self.camera_active = False
                return
            
            # Hide status label and show camera display
            self.camera_status_label.place_forget()
            self.camera_display_label.place(relx=0.5, rely=0.5, anchor="center")
            
            fgbg = cv2.createBackgroundSubtractorMOG2()
            
            while self.camera_active:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Motion detection
                fgmask = fgbg.apply(frame)
                contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                motion_detected = False
                for cnt in contours:
                    if cv2.contourArea(cnt) > 500:
                        motion_detected = True
                        x, y, w, h = cv2.boundingRect(cnt)
                        
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, "Motion Detected", (x, y-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Add LYNX Vision overlay
                cv2.putText(frame, "LYNX VISION", (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Convert frame for tkinter display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_pil = frame_pil.resize((300, 220), Image.Resampling.LANCZOS)
                
                # Update the camera display in the GUI
                photo = ctk.CTkImage(frame_pil, size=(300, 220))
                self.camera_display_label.configure(image=photo)
                
                time.sleep(0.03)  # ~30 FPS
                
        except Exception as e:
            print(f"Camera loop error: {e}")
            self.speak("Camera error occurred")
        finally:
            if self.cap:
                self.cap.release()
                self.cap = None
            self.camera_active = False
    
    def start_camera_object_detection(self):
        """Legacy method - opens camera in separate window"""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.speak("Camera could not be opened")
                return
            
            self.speak("LYNX Vision activated in external window")
            fgbg = cv2.createBackgroundSubtractorMOG2()
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                
                fgmask = fgbg.apply(frame)
                contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for cnt in contours:
                    if cv2.contourArea(cnt) > 500:
                        x, y, w, h = cv2.boundingRect(cnt)
                        
                        label = "Motion Detected"
                        
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.imshow("LYNX Vision - Motion Detection", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
        except Exception as e:
            print(f"Camera error: {e}")
            self.speak("Camera error occurred")
        finally:
            cap.release()
            cv2.destroyAllWindows()
    
    def start_camera_thread(self):
        threading.Thread(target=self.start_camera_object_detection, daemon=True).start()
    
    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.app.attributes('-fullscreen')
        self.app.attributes('-fullscreen', not is_fullscreen)
    
    def end_fullscreen(self, event=None):
        self.app.attributes('-fullscreen', False)
    
    def on_space_press(self, event):
        if not self.is_listening:
            self.start_conversation()
    
    def on_space_release(self, event):
        pass
    
    def run(self):
        try:
            self.app.mainloop()
        except KeyboardInterrupt:
            print("Program interrupted by user")
        except Exception as e:
            print(f"Runtime error: {e}")
        finally:
            self.stop_camera()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        lynx = LYNXAssistant()
        lynx.run()
    except Exception as e:
        print(f"Program error: {e}")
        input("Press Enter to exit...")
