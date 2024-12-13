import whisper
import os
import time

TEST_MODEL = "turbo"
AUDIO_DIR = "audio/mixed_sample"

identification_times = []
incorrect_files = []
correct_accuracy = []
incorrect_accuracy = []
incorrect_delta = []
english_identifications = 0

start_time = time.time()

model = whisper.load_model(TEST_MODEL)

end_time = time.time()

model_load_time = end_time - start_time

total_files = 0

for filename in os.listdir(AUDIO_DIR):
    print(f"Processing {filename}...")

    start_time = time.time()

    audio_path = os.path.join(AUDIO_DIR, filename)

    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
    _, probs = model.detect_language(mel)

    max_prob = max(probs.values())
    most_probable_language = max(probs, key=probs.get)
    correct_language = filename[:2]

    if most_probable_language != correct_language:
        incorrect_files.append(filename)
        incorrect_accuracy.append(max_prob)
        incorrect_delta.append(max_prob - probs[correct_language])

        print(f"\033[1;31mIncorrectly identified {filename}\033[0m as {most_probable_language} with a probability of {max_prob}.")
        print(f"Correct language's probability was {probs[correct_language]}.")

        if most_probable_language == "en":
            english_identifications += 1
    else:
        correct_accuracy.append(max_prob)

        print(f"\033[1;32mCorrectly identified {filename}\033[0m as {most_probable_language} with a probability of {max_prob}.")

    end_time = time.time()

    elapsed_time = end_time - start_time
    identification_times.append(elapsed_time)
    print(f"Identification took {elapsed_time:.2f} seconds.\n")

    total_files += 1


print(f"\nMODEL: {TEST_MODEL}")
print(f"Model load time: {model_load_time:.2f} seconds.")
print(f"Average identification time: {sum(identification_times) / len(identification_times):.2f} seconds.")
print(f"\nAccuracy for identifications: {len(correct_accuracy) / total_files * 100:.2f}%.")
print(f"Percentage of en identifications: {english_identifications / total_files * 100:.2f}%.\n")
print(f"Average probability for correct identifications: {sum(correct_accuracy) / len(correct_accuracy):.2f}.")
print(f"Average probability for incorrect identifications: {sum(incorrect_accuracy) / len(incorrect_accuracy):.2f}.")
print(f"Average delta in incorrect identifications (between identifed v.s. correct): {sum(incorrect_delta) / len(incorrect_delta):.2f}.")