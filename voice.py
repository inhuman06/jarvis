import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import time

engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Continuously listens to the background and captures audio when speech is detected."""
    sample_rate = 16000
    filename = "temp_audio.wav"
    
    # Threshold determines how loud you need to speak to trigger it.
    # 0.03 is usually perfect for close microphones. Increase it if it triggers on background noise.
    THRESHOLD = 0.03 
    SILENCE_DURATION = 1.5  # Stop recording after 1.5 seconds of silence
    
    print("\n[🫥 JARVIS is idling... Speak to wake him up]")
    
    audio_buffer = []
    recording = False
    silence_start = None
    
    # Define a callback function to process audio blocks from the microphone in real-time
    def callback(indata, frames, time_info, status):
        nonlocal recording, silence_start, audio_buffer
        # Calculate the volume level (Root Mean Square)
        volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
        
        if volume_norm > THRESHOLD:
            if not recording:
                print("[🎙️ Wake word/Speech detected! Recording...]")
                recording = True
            silence_start = None  # Reset silence timer because you are speaking
            audio_buffer.append(indata.copy())
        elif recording:
            # If we were recording but it's now quiet, start tracking silence duration
            audio_buffer.append(indata.copy())
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > SILENCE_DURATION:
                # We have hit enough silence, stop the stream
                raise sd.CallbackStop

    # Start the real-time microphone monitoring stream
    try:
        with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback, blocksize=1024):
            while recording is False or (silence_start is None or time.time() - silence_start <= SILENCE_DURATION):
                sd.sleep(100)
    except sd.CallbackStop:
        pass  # Recording finished cleanly
    except Exception as e:
        print(f"Microphone Stream Error: {e}")
        return None

    # Process and transcribe the recorded audio block
    if audio_buffer:
        try:
            # Combine all recorded audio frames into one file
            audio_data = np.concatenate(audio_buffer, axis=0)
            write(filename, sample_rate, (audio_data * 32767).astype(np.int16))
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(filename) as source:
                audio = recognizer.record(source)
                query = recognizer.recognize_google(audio)
            
            if os.path.exists(filename):
                os.remove(filename)
                
            print(f"You said: {query}")
            return query
            
        except Exception:
            if os.path.exists(filename):
                os.remove(filename)
            return None
    return None