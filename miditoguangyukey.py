import mido
import sys

def midi_to_sky_script(midi_path, map_type):
    # 光遇 15 键映射表 (MIDI 编号 -> 光遇 1 到 15 号键)
    # 60 代表中央 C (Do)
    sky_map = {
        60: 1,  62: 2,  64: 3,  65: 4,  67: 5,  # 第一排 (A1-A5)
        69: 6,  71: 7,  72: 8,  74: 9,  76: 10, # 第二排 (B1-B5)
        77: 11, 79: 12, 81: 13, 83: 14, 84: 15  # 第三排 (C1-C5)
    }

    sky_map_c3 = {
        48: 1,  50: 2,  52: 3,  53: 4,  55: 5,  # 第一排 (A1-A5)
        57: 6,  59: 7,  60: 8,  62: 9,  64: 10, # 第二排 (B1-B5)
        65: 11, 67: 12, 69: 13, 71: 14, 72: 15  # 第三排 (C1-C5)
    }

    mid = mido.MidiFile(midi_path)
    
    # 提取所有有效的按键事件及其绝对时间(毫秒)
    events = []
    current_time_ms = 0
    
    for msg in mid:
        # mido 的 msg.time 是距离上一个事件的相对时间(秒)
        current_time_ms += msg.time * 1000
        
        # 只需要按键按下的事件 (Note On 且速度大于 0)
        if msg.type == 'note_on' and msg.velocity > 0:
            note = msg.note
            if midi_type == 'c3':
                # 如果音符不在光遇音域，尝试通过加减八度强转
                while note < 48 and note != 0: note += 12
                while note > 72 and note != 0: note -= 12
                if note in sky_map_c3:
                    events.append((round(current_time_ms), sky_map_c3[note]))
            else:
                # 如果音符不在光遇音域，尝试通过加减八度强转
                while note < 60 and note != 0: note += 12
                while note > 84 and note != 0: note -= 12
                if note in sky_map:
                    events.append((round(current_time_ms), sky_map[note]))

    if not events:
        print("没有检测到有效的音符。")
        return

    # 按时间将同时按下的音符(和弦)进行合并
    merged_tracks = {}
    for time, key in events:
        if time not in merged_tracks:
            merged_tracks[time] = []
        if key not in merged_tracks[time]: # 防止重复
            merged_tracks[time].append(key)
            
    # 排序时间点
    sorted_times = sorted(merged_tracks.keys())
    
    # 生成带延迟的格式: ( [keys], delay )
    script_output = []
    for i in range(len(sorted_times)):
        current_time = sorted_times[i]
        keys = sorted(merged_tracks[current_time]) # 按键从小到大排序
        
        # 计算距离下一个音符的延迟
        if i < len(sorted_times) - 1:
            delay = sorted_times[i+1] - current_time
        else:
            delay = 0 # 最后一个音符延迟为 0
            
        script_output.append((keys, round(delay)))

    # 打印输出结果
    print("[\n" + ",\n".join([f"    ({keys}, {delay})" for keys, delay in script_output]) + "\n]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the MIDI file.")
        sys.exit(1)
    
    midi_file_path = sys.argv[1]
    midi_type = sys.argv[2]
    midi_to_sky_script(midi_file_path, midi_type)
