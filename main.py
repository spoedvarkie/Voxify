import os
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import moviepy.editor as mp
import pyperclip
import whisper
import tempfile

# Define a temporary directory for storing audio files
TEMP_DIR = tempfile.mkdtemp()


class VideoToTextConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Text Converter")

        # Minimum size for the window
        self.root.minsize(700, 480)

        # Initialize spinner window attribute
        self.spinner_window = None

        # Define the font
        self.output_font = ("Arial", 12)

        # Create a frame to hold the output text area
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        # Create the output text area inside the frame
        self.output_text = tk.Text(self.frame, wrap=tk.WORD, font=self.output_font)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar only if the text extends past the visible block
        self.scrollbar_y = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))
        self.output_text.config(yscrollcommand=self.scrollbar_y.set)

        # Add buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.select_button = tk.Button(self.button_frame, text="Select Video", command=self.select_video)
        self.select_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.convert_button = tk.Button(self.button_frame, text="Convert to Text", command=self.convert_to_text)
        self.convert_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.copy_button = tk.Button(self.button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=root.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    def select_video(self):
        self.video_file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])

    def convert_to_text(self):
        if hasattr(self, 'video_file_path'):
            # Create the spinner window
            self.show_spinner()

            # Start the conversion process in a separate thread - for progress window to work
            conversion_thread = threading.Thread(target=self.perform_conversion)
            conversion_thread.start()
        else:
            self.output_text.insert(tk.END, "Please select a video file first.\n")

    def perform_conversion(self):
        # Proceed with the actual conversion
        filename = os.path.basename(self.video_file_path).split(".")[0]
        audio_path = os.path.join(TEMP_DIR, f"{filename}.wav")
        text = self.video_to_transcript(self.video_file_path, audio_path)

        # Remove leading whitespace if necessary
        text = text.strip()

        # Clear previous text & Inserts new text
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)

        # Destroy the spinner window
        self.spinner_window.destroy()

    def video_to_transcript(self, video_path, audio_path):
        # Load the video from file
        video = mp.VideoFileClip(video_path)
        # Extract audio from the video
        audio = video.audio
        # Write the audio to a temporary WAV file
        audio.write_audiofile(audio_path, codec='pcm_s16le')
        # First grab the relevant model for the task at hand
        model = whisper.load_model("base.en")
        # Transcribe the audio file using the selected model
        result = model.transcribe(audio_path)
        return result["text"]

    def copy_to_clipboard(self):
        text = self.output_text.get(1.0, tk.END)
        pyperclip.copy(text)

    def show_spinner(self):
        self.spinner_window = tk.Toplevel(self.root)
        self.spinner_window.title("Converting")

        # Calculate the position to center the spinner window
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()

        spinner_width = 245
        spinner_height = 150

        # Get main window middle XY coordinates, so progress window is displayed in middle of main window
        spinner_x = main_window_x + (main_window_width - spinner_width) // 2
        spinner_y = main_window_y + (main_window_height - spinner_height) // 2

        # Set the position and size of the spinner window
        self.spinner_window.geometry(f"{spinner_width}x{spinner_height}+{spinner_x}+{spinner_y}")
        self.spinner_window.resizable(False, False)

        # Add a label with spinner animation
        spinner_label = ttk.Label(self.spinner_window, text="Converting, please wait...")
        spinner_label.pack(padx=20, pady=20)

        # You can customize the spinner animation here
        spinner = ttk.Progressbar(self.spinner_window, mode='indeterminate')
        spinner.pack(padx=20, pady=20)
        spinner.start()

        # Update the GUI to ensure spinner window is rendered
        self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToTextConverter(root)
    root.mainloop()
