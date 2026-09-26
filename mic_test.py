import sounddevice as sd

print("Speak for 5 seconds")

audio = sd.rec(
    int(5*44100),
    samplerate=44100,
    channels=1
)

sd.wait()

print("Microphone works")