import os
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, ttk
import pygame
import random

# Initialize pygame mixer
pygame.mixer.init()

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Advanced Music Player")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        self.playlist = []
        self.current_index = 0
        self.volume_level = 0.5
        self.shuffle = False

        self.track_label = tk.Label(
            self.root, text="🎶 No Track Playing", font=("Helvetica", 14), bg="#f0f0f0"
        )
        self.track_label.pack(pady=10)

        # Playlist Listbox + Scrollbar
        frame = tk.Frame(self.root, bg="black", bd=2)
        frame.pack(pady=5)

        self.scrollbar = Scrollbar(frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = Listbox(
            frame, width=60, height=10, yscrollcommand=self.scrollbar.set,
            font=("Courier", 10), bg="white", fg="black",
            selectbackground="lightblue", activestyle="dotbox"
        )
        self.listbox.pack(side=tk.LEFT)
        self.scrollbar.config(command=self.listbox.yview)

        # Control Buttons
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=20)

        tk.Button(control_frame, text="📂 Load Songs", width=15, command=self.load_songs).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="▶️ Play", width=15, command=self.play_song).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="⏸ Pause", width=15, command=self.pause_song).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="⏹ Stop", width=15, command=self.stop_song).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="⏮ Prev", width=15, command=self.prev_song).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="⏭ Next", width=15, command=self.next_song).grid(row=1, column=2, padx=5, pady=5)

        # Volume slider
        volume_frame = tk.Frame(self.root, bg="#f0f0f0")
        volume_frame.pack(pady=10)
        tk.Label(volume_frame, text="Volume", bg="#f0f0f0").pack()
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=1, value=0.5, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.pack()

        # Shuffle checkbox
        self.shuffle_var = tk.BooleanVar()
        self.shuffle_check = tk.Checkbutton(self.root, text="🔀 Shuffle", variable=self.shuffle_var, bg="#f0f0f0", command=self.toggle_shuffle)
        self.shuffle_check.pack()

    def load_songs(self):
        files = filedialog.askopenfilenames(title="Select MP3 Files", filetypes=[("MP3 files", "*.mp3")])
        for f in files:
            if f not in self.playlist:
                self.playlist.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))
                print(f"[+] Loaded: {os.path.basename(f)}")
        if not files:
            print("[!] No songs selected")

    def play_song(self):
        if not self.playlist:
            print("[!] No songs loaded.")
            return
        if self.shuffle_var.get():
            self.current_index = random.randint(0, len(self.playlist) - 1)
            print("[🔀] Shuffle enabled")
        else:
            selection = self.listbox.curselection()
            if selection:
                self.current_index = selection[0]
            else:
                print("[!] No song selected.")
                return

        song_path = self.playlist[self.current_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.set_volume(self.volume_level)
        pygame.mixer.music.play()
        print(f"[▶️] Now Playing: {os.path.basename(song_path)}")
        self.track_label.config(text=f"🎵 Now Playing: {os.path.basename(song_path)}")
        self.highlight_current_song()

    def pause_song(self):
        pygame.mixer.music.pause()
        print("[⏸] Playback Paused")
        self.track_label.config(text="⏸ Paused")

    def stop_song(self):
        pygame.mixer.music.stop()
        print("[⏹] Playback Stopped")
        self.track_label.config(text="⏹ Stopped")

    def prev_song(self):
        if self.current_index > 0:
            self.current_index -= 1
            print("[⏮] Previous Track")
            self.play_song()
        else:
            print("[!] Already at the first track")

    def next_song(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            print("[⏭] Next Track")
            self.play_song()
        else:
            print("[!] Already at the last track")

    def set_volume(self, val):
        self.volume_level = float(val)
        pygame.mixer.music.set_volume(self.volume_level)
        print(f"[🔊] Volume set to {round(self.volume_level * 100)}%")

    def toggle_shuffle(self):
        self.shuffle = self.shuffle_var.get()
        print(f"[🔀] Shuffle {'enabled' if self.shuffle else 'disabled'}")

    def highlight_current_song(self):
        self.listbox.select_clear(0, tk.END)
        self.listbox.select_set(self.current_index)
        self.listbox.activate(self.current_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
