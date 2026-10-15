import sys
import os
import mido
import traceback
from basic_pitch.inference import predict_and_save
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
def wavtomidi_by_ai(wav_file_dir, output_dir):
    print(f"Ready to convert wav where is in {wav_file_dir} to midi file by Spotify Basic Pitch...")

    predict_and_save(
        audio_path_list=[wav_file_dir],
        output_directory=output_dir,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=0.6,
        frame_threshold=0.5,
        minimum_note_length=80
    )

    base_name = os.path.splitext(os.path.basename(wav_file_dir))[0]

    return os.path.join(output_dir, f"{base_name}_basic_pitch.mid")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"please input the wave_file_path as the second parameter")
        sys.exit(1)

    wav_path = sys.argv[1]
    output_dir = "./midouput"
    os.makedirs(output_dir, exist_ok=True)

    try:
        midi_out = wavtomidi_by_ai(wav_path, output_dir)
    except Exception as e:
        print(f"fail to convert wav to midi: {e}")
        traceback.print_exc()
        sys.exit(1)
    
