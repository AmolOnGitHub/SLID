import os
import random
import shutil

dev_folder = 'audio/dev'
sample_folder = 'audio/sample'

if os.path.exists(sample_folder):
    shutil.rmtree(sample_folder)
os.makedirs(sample_folder, exist_ok=True)

print("Initializing audio clip selection...")

for language in os.listdir(dev_folder):
    lang_path = os.path.join(dev_folder, language)
    
    if os.path.isdir(lang_path):
        audio_files = [f for f in os.listdir(lang_path) if os.path.isfile(os.path.join(lang_path, f))]
        
        selected_files = random.sample(audio_files, min(5, len(audio_files)))
        if (len(audio_files) < 5):
            print(f"Warning: Only {len(audio_files)} audio clips found for {language}. Skipping..")
            continue

        for file in selected_files:
            src = os.path.join(lang_path, file)
            dest = os.path.join(sample_folder, f"{language}_{file}")
            shutil.copy(src, dest)

print("Audio clips selected and copied successfully.")