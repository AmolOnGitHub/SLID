import os
import random
import subprocess
import shutil
from pydub import AudioSegment


def interleave_audios(en_file_path, wav_file_path, output_path="output.wav"):
    en_audio = AudioSegment.from_file(en_file_path)
    wav_audio = AudioSegment.from_file(wav_file_path)
    
    wav_chunk_duration = 2000  # 2 seconds
    en_chunk_duration = 1000   # 1 second
    
    en_pos = 0
    wav_pos = 0
    
    final_audio = AudioSegment.silent(duration=0)
    
    while en_pos < len(en_audio):
        wav_end = wav_pos + wav_chunk_duration

        if wav_end > len(wav_audio):
            remaining = wav_audio[wav_pos:]

            loop_part = (wav_chunk_duration - len(remaining))
            loop_part = wav_audio[:loop_part] if loop_part <= len(wav_audio) else wav_audio * ((loop_part // len(wav_audio)) + 1)
            wav_chunk = remaining + loop_part

            wav_pos = loop_part.duration_seconds * 1000
        else:
            wav_chunk = wav_audio[wav_pos:wav_end]
            wav_pos = wav_end

            if wav_pos >= len(wav_audio):
                wav_pos = 0
        
        final_audio += wav_chunk
        

        en_end = en_pos + en_chunk_duration

        if en_end > len(en_audio):
            en_chunk = en_audio[en_pos:]
            en_pos = len(en_audio) 
        else:
            en_chunk = en_audio[en_pos:en_end]
            en_pos = en_end
        
        final_audio += en_chunk
    

    final_audio.export(output_path, format="wav")


BASE_DIR = 'audio/dev/'
EN_DIR = os.path.join(BASE_DIR, 'en')
OUTPUT_DIR = 'audio/mixed_sample/'

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

en_files = [f for f in os.listdir(EN_DIR) if f.endswith('.wav')]

subdirs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and d != 'en']

for subdir in subdirs:
    subdir_path = os.path.join(BASE_DIR, subdir)
    wav_files = [f for f in os.listdir(subdir_path) if f.endswith('.wav')]
    selected_files = random.sample(wav_files, min(5, len(wav_files)))

    print(f'\nProcessing {subdir}...\n')

    for wav_file in selected_files:
        en_file = random.choice(en_files)

        wav_file_path = os.path.join(subdir_path, wav_file)
        en_file_path = os.path.join(EN_DIR, en_file)

        print(f'\tInterleaving {wav_file} and {en_file}...')

        output_filename = f'{subdir}_{wav_file[:-4]}_{en_file}'
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        interleave_audios(en_file_path, wav_file_path, output_path)
        
        print(f"\tDone.")