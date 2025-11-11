import cv2
import threading
import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Speak something...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                update_text(text)
                play_video(text)
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

# Function to update the recognized text in the GUI
def update_text(text):
    recognized_text.config(state=tk.NORMAL)
    recognized_text.insert(tk.END, text + "\n")
    recognized_text.config(state=tk.DISABLED)

# Function to map recognized words/phrases to videos and play them
def play_video(text):
    word_to_video = {
        "hello": "hello.mp4",
        "WhatsApp": "whatsapp.mp4",
        "afternoon": "afternoon.mp4",
        "good": "good.mp4",
        "goodbye": "goodbye.mp4",
        "how": "how.mp4",
        "morning": "morning.mp4",
        "night": "night.mp4",
        "you": "you.mp4",
        "u": "u.mp4",
        "see you later": "see_you_later.mp4",
        "take care": "take_care.mp4",
        "nice to meet you": "nice_to_meet_you.mp4",
        "same here": "same_here.mp4",
        "same": "same.mp4",
        "see": "see.mp4",
        "later": "later.mp4",
        "tomorrow": "tomorrow.mp4",
        "my": "my.mp4",
        "mine": "my.mp4",
        "name": "name.mp4",
        "I": "I.mp4",
        "want": "want.mp4",
        "thank you": "thank.mp4",
        "thanks": "thank.mp4",
        "please": "please.mp4",
        "sorry": "sorry.mp4",
        "I am sorry": "I_am_sorry.mp4",
        "Excuse": "excuse.mp4",
        "excuse me": "excuse_me.mp4",
        "help": "help.mp4",
        "stop": "stop.mp4",
        "go": "go.mp4",
        "love": "love.mp4",
        "I love you": "I_love_you.mp4",

        
        
    }

    if text in word_to_video:
        video_path = word_to_video[text]
        play_video_file(video_path)
    else:
        words = text.split()
        for word in words:
            if word in word_to_video:
                video_path = word_to_video[word]
                play_video_file(video_path)
            else:
                print(f"No video available for the word: {word}")

def play_video_file(video_path):
    cap = cv2.VideoCapture(video_path)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    frame_skip = 2  

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            for _ in range(frame_skip - 1):
                cap.read()
            
            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            video_display_panel.imgtk = imgtk
            video_display_panel.config(image=imgtk)
            root.update_idletasks()
            root.update()
        else:
            break
    cap.release()
    clear_image()  # Clear the image after the video ends

# Function to clear the image
def clear_image():
    video_display_panel.configure(image='')
    video_display_panel.image = None

def start_video_feed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            video_panel.imgtk = imgtk
            video_panel.config(image=imgtk)
        root.update_idletasks()
    cap.release()

root = tk.Tk()
root.title("Hand Sign Recognition")

root.attributes('-fullscreen', True)

video_panel = tk.Label(root)
video_panel.pack(side="left", padx=10, pady=10)

video_display_panel = tk.Label(root)
video_display_panel.place(relx=0.5, rely=0.5, anchor='center') 

recognized_text = tk.Text(root, state=tk.DISABLED, width=30, height=10)
recognized_text.pack(side="right", padx=10, pady=10)

speech_thread = threading.Thread(target=recognize_speech)
speech_thread.daemon = True
speech_thread.start()

video_thread = threading.Thread(target=start_video_feed)
video_thread.daemon = True
video_thread.start()

root.mainloop()
