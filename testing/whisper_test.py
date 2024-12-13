import whisper
import pycountry

def get_language_name(code):
    try:
        language = pycountry.languages.get(alpha_2=code)
        return language.name if language else "Unknown"
    except KeyError:
        return "Invalid language code"


file = "output.wav"

model = whisper.load_model("base")
audio = whisper.load_audio(file)
audio = whisper.pad_or_trim(audio)

mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

_, probs = model.detect_language(mel)


top_probs = {lang: prob for lang, prob in sorted(probs.items(), key=lambda item: item[1], reverse=True)}

cumulative_prob = 0.0
top_75_probs = {}

for lang, prob in top_probs.items():
    if cumulative_prob > 0.75:
        break
    top_75_probs[lang] = prob
    cumulative_prob += prob


print()

for lang, prob in top_75_probs.items():
    print(f"Language: {get_language_name(lang)} ({lang}), Probability: {prob}")

print("\nsuccess")