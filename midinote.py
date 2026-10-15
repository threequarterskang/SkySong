import mido
import sys

def midi_to_printnote(midi_path):
    mid = mido.MidiFile(midi_path)

    events = []
    current_time_ms = 0

    for msg in mid:
        current_time_ms += msg.time*1000

        if msg.type == 'note_on' and msg.velocity > 0:

            note = msg.note

            events.append((round(current_time_ms), note))  # 记录绝对时间和音符

    merged_tracks = {}
    for time, note in events:
        if time not in merged_tracks:
            merged_tracks[time] = []
        if note not in merged_tracks[time]:
            merged_tracks[time].append(note)

    sorted_times = sorted(merged_tracks.keys())

    script_output = []
    for i in range(len(sorted_times)):
        current_time = sorted_times[i]
        notes = sorted(merged_tracks[current_time])
        
        if i < len(sorted_times) - 1:
            delay = sorted_times[i + 1] - current_time
        else:
            delay = 0

        script_output.append((notes, round(delay)))

    print("[\n" + ",\n".join([f"    ({notes}, {delay})" for notes, delay in script_output]) + "\n]")
   
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the MIDI file.")
        sys.exit(1)
    
    midi_file_path = sys.argv[1]
    midi_to_printnote(midi_file_path)