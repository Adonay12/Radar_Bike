import pyaudio
import wave
from datetime import datetime

# Define parameters for recording
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
interval_seconds = 15  # Duration of each recording interval
total_duration = 600  # Total recording duration (10 minutes)

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Starting recording')

# Open a stream for recording
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# Calculate the number of intervals
num_intervals = total_duration // interval_seconds

# Record and save audio in intervals
for i in range(num_intervals):
    print(f'Recording interval {i + 1}/{num_intervals}')
    frames = []  # Initialize array to store frames

    # Get the current timestamp for the filename
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"recording_{current_time}.wav"

    # Record audio for the interval
    for _ in range(0, int(fs / chunk * interval_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f'Saved {filename}')

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PortAudio interface
p.terminate()

print('Finished recording')
