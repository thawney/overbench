import sounddevice as sd
import numpy as np
import whisper
import tempfile
import os
import scipy.io.wavfile as wavfile
import keyboard
import time
import subprocess

# Settings
SAMPLE_RATE = 16000  # Whisper expects 16kHz sample rate
MAX_DURATION = 30  # Max duration to record in seconds

def record_audio(duration, sample_rate):
    print("Press and hold the spacebar to start recording...")
    recording = []
    recording_start_time = None

    while True:
        if keyboard.is_pressed('space'):
            if recording_start_time is None:
                recording_start_time = time.time()
                print("Recording started.")
            
            audio_chunk = sd.rec(int(sample_rate * 1), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()  # Wait until chunk is finished
            recording.append(audio_chunk.flatten())
            
            if time.time() - recording_start_time >= duration:
                print("Maximum recording duration reached.")
                break
        else:
            if recording_start_time is not None:
                print("Recording stopped.")
                break
        
        time.sleep(0.1)  # Small delay to prevent high CPU usage

    return np.concatenate(recording) if recording else np.array([])

def save_temp_wav(data, sample_rate):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    wavfile.write(temp_file.name, sample_rate, (data * 32767).astype(np.int16))
    return temp_file.name

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result['text']

def save_and_print_transcription(text):
    temp_txt_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
    with open(temp_txt_file.name, 'w') as f:
        f.write(text)
    
    print("Transcription saved to:", temp_txt_file.name)
    
    # Print the text file using lpr
    try:
        subprocess.run(['lpr', temp_txt_file.name], check=True)
        print("Printed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to print:", e)
    
    # Clean up temporary text file
    os.remove(temp_txt_file.name)

if __name__ == "__main__":
    # Record audio while spacebar is held
    audio_data = record_audio(MAX_DURATION, SAMPLE_RATE)
    
    if audio_data.size == 0:
        print("No audio recorded.")
    else:
        # Save to temporary file
        temp_file_path = save_temp_wav(audio_data, SAMPLE_RATE)
        
        # Transcribe audio
        transcription = transcribe_audio(temp_file_path)
        
        # Print transcription
        save_and_print_transcription(transcription)
        
        # Clean up temporary WAV file
        os.remove(temp_file_path)
