import speech_recognition as sr
from tkinter import messagebox

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("🎤 Listening… speak now")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"📝 You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("❌ No speech detected")
            messagebox.showinfo("Voice Add", "No speech detected. Try again.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            messagebox.showinfo("Voice Add", "Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results; {e}")
            messagebox.showinfo("Voice Add", f"Error: {e}")
            return None
