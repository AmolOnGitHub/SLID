import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier
import os
import time

AUDIO_DIR = "audio/mixed_sample"
TENSOR_ORDER = "ab, af, am, ar, as, az, ba, be, bg, bn, bo, br, bs, ca, ceb, cs, cy, da, de, el, en, eo, es, et, eu, fa, fi, fo, fr, gl, gn, gu, gv, ha, haw, hi, hr, ht, hu, hy, ia, id, is, it, he, ja, jv, ka, kk, km, kn, ko, la, lb, ln, lo, lt, lv, mg, mi, mk, ml, mn, mr, ms, mt, my, ne, nl, nn, no, oc, pa, pl, ps, pt, ro, ru, sa, sco, sd, si, sk, sl, sn, so, sq, sr, su, sv, sw, ta, te, tg, th, tk, tl, tr, tt, uk, ur, uz, vi, war, yi, yo, zh"
TENSOR_ORDER_LOOKUP = TENSOR_ORDER.split(", ")
TENSOR_ORDER_LOOKUP = {language: index for index, language in enumerate(TENSOR_ORDER_LOOKUP)}

identification_times = []
incorrect_files = []
correct_accuracy = []
incorrect_accuracy = []
incorrect_delta = []
audio_lengths = []
english_identifications = 0

print("\nLoading model...")

start_time = time.time()

model = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")

end_time = time.time()

model_load_time = end_time - start_time

print("Model loaded.\n")
total_files = 0

for filename in os.listdir(AUDIO_DIR):
    print(f"{total_files + 1} | Processing {filename}...")

    start_time = time.time()

    audio_path = os.path.join(AUDIO_DIR, filename)

    signal = model.load_audio(audio_path)
    prediction = model.classify_batch(signal)

    sample_rate = torchaudio.info(audio_path).sample_rate
    audio_length_seconds = torchaudio.info(audio_path).num_frames / sample_rate
    audio_lengths.append(audio_length_seconds)

    max_prob = prediction[1].exp().item()
    most_probable_language = prediction[3][0][:2]
    correct_language = filename[:2]
    correct_prob = prediction[0].exp().numpy()[0][TENSOR_ORDER_LOOKUP[correct_language]]

    if most_probable_language != correct_language:
        incorrect_files.append(filename)
        incorrect_accuracy.append(max_prob)
        incorrect_delta.append(max_prob - correct_prob)

        print(f"\033[1;31mIncorrectly identified {filename}\033[0m as {most_probable_language} with a probability of {max_prob}.")
        print(f"Correct language's probability was {correct_prob}.")

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


print(f"Model load time: {model_load_time:.2f} seconds.")
print(f"Average identification time: {sum(identification_times) / len(identification_times):.2f} seconds.")
print(f"Average audio length: {sum(audio_lengths) / len(audio_lengths):.2f} seconds.")
print(f"\nAccuracy for identifications: {len(correct_accuracy) / total_files * 100:.2f}%.")
print(f"Percentage of en identifications: {english_identifications / total_files * 100:.2f}%.\n")
print(f"Average probability for correct identifications: {sum(correct_accuracy) / len(correct_accuracy):.2f}.")
print(f"Average probability for incorrect identifications: {sum(incorrect_accuracy) / len(incorrect_accuracy):.2f}.")
print(f"Average delta in incorrect identifications (between identifed v.s. correct): {sum(incorrect_delta) / len(incorrect_delta):.2f}.")
