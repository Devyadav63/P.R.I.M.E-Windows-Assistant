import customtkinter as ctk
import numpy as np
import tkinter as tk
import sounddevice as sd
import math
import colorsys
import time
import threading
import speech_recognition as sr
import os
import webbrowser
import pyautogui
import datetime
import wikipedia
import pyttsx3
import openai
from ocr_read import ocr_extracter
import pywhatkit
import ctypes
from Shot import Take_Shot

from Gemini_API import Answer
import prime  # Your voice assistant module

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GradientVisualizerCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="black", highlightthickness=0, **kwargs)
        self.waveform_data = np.zeros(120)
        self.smoothed_data = np.zeros(120)
        self.base_radius = 120
        self.start_time = time.time()

        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=44100)
        self.stream.start()
        self.update_waveform()

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)
        amplitude = np.abs(indata).mean() * 300
        self.waveform_data = np.roll(self.waveform_data, -1)
        self.waveform_data[-1] = amplitude

    def update_waveform(self):
        self.delete("wave")
        self.delete("text")

        cx, cy = self.winfo_width() // 2, self.winfo_height() // 2
        smoothing = 0.2
        self.smoothed_data = self.smoothed_data * (1 - smoothing) + self.waveform_data * smoothing

        outer_points = []
        inner_points = []
        num_points = len(self.smoothed_data)

        for i, amp in enumerate(self.smoothed_data):
            angle = (i / num_points) * 2 * math.pi
            radius = self.base_radius + amp
            x_outer = cx + radius * math.cos(angle)
            y_outer = cy + radius * math.sin(angle)
            x_inner = cx + self.base_radius * math.cos(angle)
            y_inner = cy + self.base_radius * math.sin(angle)

            outer_points.append((x_outer, y_outer))
            inner_points.append((x_inner, y_inner))

        outer_points.append(outer_points[0])
        inner_points.append(inner_points[0])

        full_shape = outer_points + inner_points[::-1]
        flat_points = [coord for pt in full_shape for coord in pt]

        hue_shift = (time.time() - self.start_time) * 0.1
        hue = hue_shift % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        fill_color = f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

        self.create_polygon(flat_points, fill=fill_color, outline="", tags="wave")

        for i in range(num_points):
            x1, y1 = outer_points[i]
            x2, y2 = outer_points[i + 1]
            self.create_line(x1, y1, x2, y2, fill="white", width=1, tags="wave")

        self.create_text(cx, cy, text="P.R.I.M.E", font=("Helvetica", 14, "bold"),
                         fill="white", tags="text", anchor="center")

        self.after(50, self.update_waveform)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("P.R.I.M.E Interface")
        self.geometry("800x550")
        self.minsize(600, 450)

        self.assistant_running = False

        self.label = ctk.CTkLabel(self, text="P.R.I.M.E", font=ctk.CTkFont(size=28, weight="bold"))
        self.label.pack(pady=(20, 10))

        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.switch = ctk.CTkSwitch(self, text="Text Box", command=self.toggle_display)
        self.switch.pack(pady=(0, 10))
        self.switch.select()

        self.input_frame = None
        self.textbox = None
        self.ask_button = None
        self.visualizer_canvas = None
        self.speak_button = None

        self.log_textbox = None  # Initialized inside toggle_display()

        self.toggle_display()

    def toggle_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        self.display_frame.grid_columnconfigure(0, weight=3)
        self.display_frame.grid_columnconfigure(1, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)

        # Log Box on the right
        self.log_textbox = ctk.CTkTextbox(self.display_frame, width=200)
        self.log_textbox.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.log_textbox.insert("end", "Logs:\n")
        self.log_textbox.configure(state="disabled")

        # Remove speak button if it exists
        if self.speak_button:
            self.speak_button.pack_forget()

        if self.switch.get() == 1:
            # TEXTBOX MODE
            text_frame = ctk.CTkFrame(self.display_frame)
            text_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

            input_frame = ctk.CTkFrame(text_frame)
            input_frame.pack(fill="x", pady=10, padx=10)

            self.textbox = ctk.CTkEntry(input_frame, placeholder_text="Type something...", height=35)
            self.textbox.pack(side="left", expand=True, fill="x", padx=(0, 10))

            self.ask_button = ctk.CTkButton(input_frame, text="Ask", width=80, command=self.ask_query)
            self.ask_button.pack(side="right")

        else:
            # VISUALIZER MODE
            self.visualizer_canvas = GradientVisualizerCanvas(self.display_frame)
            self.visualizer_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

            if not self.speak_button:
                self.speak_button = ctk.CTkButton(self, text="Start", command=self.toggle_assistant)

            self.speak_button.pack(pady=(5, 10))

    def toggle_assistant(self):
        if not self.assistant_running:
            self.speak_button.configure(text="Stop")
            threading.Thread(target=self.start_assistant).start()
        else:
            self.stop_assistant()
            self.speak_button.configure(text="Start")

    def handle_query(self, query):
        query = query.lower()

        if "hello" in query:
            self.safe_log("User greeted.")
            prime.speak("Hello Sir")

        elif "who are you" in query:
            self.safe_log("User asked about assistant.")
            prime.speak("I am prime, your personal voice assistant.")

        elif "what is your name" in query:
            self.safe_log("User asked my name.")
            prime.speak("I am prime, your personal AI.")

        elif "screenshot" in query:
            self.safe_log("Taking screenshot...")
            Take_Shot()
            prime.speak("Screenshot taken.")
        elif "what time is it" in query or "current time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.safe_log(f"Time: {current_time}")
            prime.speak(f"The time is {current_time}")

        elif "what date is today" in query or "today's date" in query:
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            self.safe_log(f"Date: {today}")
            prime.speak(f"Today's date is {today}")

        elif "shutdown system" in query:
            self.safe_log("Shutting down system.")
            prime.speak("Shutting down the system. Goodbye!")
            os.system("shutdown /s /t 1")

        elif "restart system" in query:
            self.safe_log("Restarting system.")
            prime.speak("Restarting the system now.")
            os.system("shutdown /r /t 1")

        elif "lock screen" in query:
            self.safe_log("Locking the screen.")
            prime.speak("Locking your system.")
            ctypes.windll.user32.LockWorkStation()

        elif "minimize all" in query:
            self.safe_log("Minimizing all windows.")
            prime.speak("Minimizing all windows.")
            pyautogui.hotkey("win", "d")

        elif "maximize all" in query:
            self.safe_log("Maximizing all windows.")
            prime.speak("Restoring all windows.")
            pyautogui.hotkey("win", "d")

        elif "note" in query:
            self.safe_log("Taking a note...")
            prime.speak("What should I write?")
            note = prime.Listenme()
            if note != "None":
                with open("notes.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()}: {note}\n")
                self.safe_log(f"Note saved: {note}")
                prime.speak("Note has been saved.")
            else:
                prime.speak("Didn't catch that note.")

        elif "joke" in query:
            self.safe_log("Telling a joke.")
            joke = "Why did the computer go to the doctor? Because it had a virus!"
            prime.speak(joke)
            self.safe_log(f"Joke: {joke}")

        elif "weather" in query:
            self.safe_log("Opening weather information.")
            prime.speak("Opening the weather forecast.")
            webbrowser.open("https://www.google.com/search?q=current+weather")

        elif "who is" in query or "what is" in query:
            try:
                self.safe_log(f"Searching Wikipedia for: {query}")
                person = query.replace("who is", "").replace("what is", "").strip()
                summary = wikipedia.summary(person, sentences=2)
                prime.speak(summary)
                self.safe_log(f"Wikipedia: {summary}")
            except Exception as e:
                prime.speak("I couldn't find that on Wikipedia.")
                self.safe_log(f"Wikipedia Error: {e}")


        elif "read" in query:
            self.safe_log("Reading screen using OCR...")
            text = ocr_extracter()
            prime.speak(text)
            self.safe_log(f"OCR Read: {text}")

        elif "open google" in query:
            self.safe_log("Opening Google...")
            prime.speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in query:
            self.safe_log("Opening YouTube...")
            prime.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "read clipboard" in query or "speak clipboard" in query:
            try:
                import pyperclip
                text = pyperclip.paste()
                if text:
                    self.safe_log(f"Clipboard content: {text}")
                    prime.speak(f"You copied: {text}")
                else:
                    self.safe_log("Clipboard is empty.")
                    prime.speak("Your clipboard is empty.")
            except Exception as e:
                self.safe_log("Clipboard read error.")
                prime.speak("Sorry, I couldn't access your clipboard.")


        elif "open command prompt" in query:
            self.safe_log("Opening CMD...")
            prime.speak("Opening Command Prompt")
            os.system("start cmd")

        elif "open camera" in query:
            self.safe_log("Opening Camera...")
            prime.speak("Opening Camera")
            os.system("start microsoft.windows.camera:")

        elif "volume up" in query:
            self.safe_log("Increasing volume...")
            prime.speak("Increasing volume")
            pyautogui.press("volumeup")

        elif "volume down" in query:
            self.safe_log("Decreasing volume...")
            prime.speak("Decreasing volume")
            pyautogui.press("volumedown")

        elif "mute" in query:
            self.safe_log("Muting volume...")
            prime.speak("Volume muted")
            pyautogui.press("volumemute")

        elif "unmute" in query:
            self.safe_log("Unmuting volume...")
            prime.speak("Volume unmuted")
            pyautogui.press("volumemute")  # toggle

        elif "play music" in query:
            self.safe_log("Playing music on YouTube...")
            prime.speak("What should I play?")
            music_query = prime.Listenme()
            if music_query != "None":
                self.safe_log(f"Searching: {music_query}")
                pywhatkit.playonyt(music_query)
                prime.speak("Playing now.")
            else:
                prime.speak("Didn't catch that.")

        elif "write code" in query:
            self.safe_log("User requested code generation.")
            prime.speak("Please tell me what code you want.")
            prompt = prime.Listenme()
            if prompt != "None":
                self.safe_log(f"Code Prompt: {prompt}")
                answer = Answer(prompt)
                prime.speak("Here is the code.")
                self.safe_log(answer)
            else:
                prime.speak("Didn't catch that.")

        elif "search on google" in query:
            self.safe_log("User wants to search something.")
            prime.speak("What should I search?")
            query_text = prime.Listenme()
            if query_text != "None":
                self.safe_log(f"Searching for: {query_text}")
                prime.speak("Searching now.")
                pywhatkit.search(query_text)
            else:
                prime.speak("Didn't catch that.")

        elif 'play on YouTube'.lower() in query.lower():
            prime.speak("What Should I play on youtube sir")
            yts = prime.Listenme()
            self.safe_log("Searching For your query sir")
            prime.speak("Searching For your query sir")
            pywhatkit.playonyt(yts)
            time.sleep(5)
            prime.speak("May this help you sir")
        elif 'search on YouTube'.lower() in query.lower():
            prime.speak("What Should I search on youtube sir")
            yts = prime.Listenme()
            self.safe_log("Searching For your query sir")
            prime.speak("Searching For your query sir")
            webbrowser.open("https://www.youtube.com/results?search_query=" + yts)
            time.sleep(3)
            prime.speak("This is what I found sir")

        elif "gemini" in query:
            self.safe_log("User wants an answer from Gemini.")
            prompt = query.split("gemini", 1)[1].strip()
            if prompt != "None":
                self.safe_log(f"Question: {prompt}")
                result = Answer(prompt)
                prime.speak("Here's the answer.")
                self.safe_log(result)
                prime.speak(result)
            else:
                prime.speak("Didn't catch that.")

        elif "bye" in query or "exit" in query or "stop" in query:
            self.safe_log("User ended session.")
            prime.speak("Goodbye sir.")
            self.listening = False

        else:
            self.safe_log(f"Unknown command: {query}")

    def start_assistant(self):
        self.assistant_running = True
        self.safe_log("Assistant started.")
        prime.speak("Assistant started")
        prime.speak("Hello Dev Sir, I welcome you, How can I help you sir")
        self.safe_log("Hello Dev Sir, I welcome you, How can I help you sir")

        self.run_assistant_logic()

    def run_assistant_logic(self):
        if self.switch.get() == 1:
            return

        while self.assistant_running:
            self.safe_log("Listening...")
            query = prime.Listenme()
            self.handle_query(query)

    def stop_assistant(self):
        self.assistant_running = False
        self.safe_log("Assistant stopped.")
        threading.Thread(target=prime.speak, args=("Assistant stopped",)).start()

    def ask_query(self):
        query = self.textbox.get() if self.textbox else ""
        if query:
            self.handle_query(query)
            self.safe_log(f"User Said: {query}")

    def safe_log(self, message):
        self.after(0, self.log_message, message)

    def log_message(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see("end")


if __name__ == "__main__":
    app = App()
    app.mainloop()
