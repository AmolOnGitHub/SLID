import os
import shutil

sample_dir = os.path.join('audio', 'sample')
if os.path.exists(sample_dir):
    shutil.rmtree(sample_dir)
os.makedirs(sample_dir)

with open('sample.txt', 'r') as f:
    for line in f:
        line = line.replace('├──', '').replace('└──', '').strip()
        filename = line
        if not filename:
            continue
        if not filename.endswith('.wav'):
            continue
        lang_id = os.path.splitext(filename)[0]
        if '_' not in lang_id:
            continue
        lang, id = lang_id.split('_', 1)
        source_file = os.path.join('audio', 'dev', lang, f"{id}.wav")
        dest_file = os.path.join('audio', 'sample', filename)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copyfile(source_file, dest_file)