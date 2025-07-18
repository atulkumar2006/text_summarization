import tkinter as tk
from tkinter import scrolledtext, messagebox
from transformers import pipeline
import threading

# Load the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Main summarization function
def summarize_text():
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text to summarize.")
        return

    # Disable the summarize button during processing
    summarize_button.config(state=tk.DISABLED)
    output_box.delete("1.0", tk.END)

    def process():
        try:
            summary = summarizer(input_text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            output_box.insert(tk.END, summary)
        except Exception as e:
            output_box.insert(tk.END, f"Error: {e}")
        finally:
            summarize_button.config(state=tk.NORMAL)

    # Run in separate thread to keep GUI responsive
    threading.Thread(target=process).start()

# Create GUI window
window = tk.Tk()
window.title("Text Summarization Tool")
window.geometry("800x600")
window.config(padx=20, pady=20)

# Input label and text box
tk.Label(window, text="Enter Long Article/Text:", font=("Arial", 12, "bold")).pack(anchor="w")
input_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=15, font=("Arial", 10))
input_box.pack(pady=10)

# Summarize button
summarize_button = tk.Button(window, text="Summarize Text", command=summarize_text, font=("Arial", 12), bg="#4CAF50", fg="white")
summarize_button.pack(pady=10)

# Output label and text box
tk.Label(window, text="Summary:", font=("Arial", 12, "bold")).pack(anchor="w")
output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=10, font=("Arial", 10))
output_box.pack(pady=10)

# Start the GUI event loop
window.mainloop()
