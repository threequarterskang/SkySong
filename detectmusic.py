import numpy as np
import sounddevice as sd
import librosa
import time
import pretty_midi

sample_rate = 44100 # Sample rate for recording
chunk_size = 1024 
min_freq = 65
max_freq = 2093

start_time = time.time()

recorded_data = []

MIDI_FILE = "pitch_results.mid"

print("Recording audio....")
print("Press Ctrl+C to stop recording.")

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    
    audio_data = indata[:, 0].astype(np.float32)

    rms = np.sqrt(np.mean(audio_data**2))
    if rms < 0.01:
        return
    
    try:

        f0 = librosa.yin(y=audio_data, sr=sample_rate, fmin=min_freq, fmax=max_freq)

        valid_f0 = f0[~np.isnan(f0) & (f0 > 0)]

        if len(valid_f0) > 0:

            mean_pitch = float(np.mean(valid_f0))

            midi_num = int(np.round(librosa.hz_to_midi(mean_pitch)))

            note_name = librosa.midi_to_note(int(np.round(midi_num)))

            current_offset = round(time.time() - start_time, 2)

            recorded_data.append((current_offset, note_name, midi_num, round(mean_pitch, 2)))

            print(f"\rdetected pitch: {mean_pitch} hz, notename: {note_name}", end="")

    except Exception as e:
        print(f"\nError in pitch detection: {e}")

def save_results():
    if not recorded_data:
        print("No pitch data detected.")
        return
    
    print(f"\nSaving results to pitch_results.txt...")

    pm = pretty_midi.PrettyMIDI()

    instrument = pretty_midi.Instrument(program=0)

    frame_duration = chunk_size / sample_rate

    for item in recorded_data:
        offset, note_name, midi_num, mean_pitch = item

        note = pretty_midi.Note(
            velocity = 100,
            pitch = midi_num,
            start = offset,
            end = offset + frame_duration
        )

        instrument.notes.append(note)

    pm.instruments.append(instrument)
    pm.write(MIDI_FILE)
    print(f"Results saved to {MIDI_FILE}.")
   
try:
    with sd.InputStream(
        channels = 1,
        samplerate = sample_rate,
        blocksize = chunk_size,
        callback = audio_callback
        ):
        while True:
            sd.sleep(1000)

except KeyboardInterrupt:
    save_results()
    print("\nRecording stopped.")
        




