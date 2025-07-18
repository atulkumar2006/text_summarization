import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    # Convert to WAV if not already
    if not file_path.endswith(".wav"):
        audio = AudioSegment.from_file(file_path)
        audio.export("converted.wav", format="wav")
        audio_path = "converted.wav"
    else:
        audio_path = file_path

    # Recognize speech
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "API unavailable or quota exceeded"

def upload_file():
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg")]
    )
    if file_path:
        messagebox.showinfo("Processing", "Transcribing, please wait...")
        result = transcribe_audio(file_path)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, result)

# --- GUI Setup ---
root = tk.Tk()
root.title("Speech to Text App")
root.geometry("600x400")
root.resizable(False, False)

# Upload Button
upload_btn = tk.Button(root, text="Upload Audio File", font=("Arial", 12), command=upload_file)
upload_btn.pack(pady=20)

# Text Box
text_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
text_box.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

root.mainloop()
