import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier

TENSOR_ORDER = "ab, af, am, ar, as, az, ba, be, bg, bn, bo, br, bs, ca, ceb, cs, cy, da, de, el, en, eo, es, et, eu, fa, fi, fo, fr, gl, gn, gu, gv, ha, haw, hi, hr, ht, hu, hy, ia, id, is, it, he, ja, jv, ka, kk, km, kn, ko, la, lb, ln, lo, lt, lv, mg, mi, mk, ml, mn, mr, ms, mt, my, ne, nl, nn, no, oc, pa, pl, ps, pt, ro, ru, sa, sco, sd, si, sk, sl, sn, so, sq, sr, su, sv, sw, ta, te, tg, th, tk, tl, tr, tt, uk, ur, uz, vi, war, yi, yo, zh"
TENSOR_ORDER_LOOKUP = TENSOR_ORDER.split(", ")
TENSOR_ORDER_LOOKUP = {language: index for index, language in enumerate(TENSOR_ORDER_LOOKUP)}

model = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")

signal = model.load_audio("audio/personal/ta.wav")

prediction = model.classify_batch(signal)

print(f"Predictions: {prediction[0].exp().numpy()[0][TENSOR_ORDER_LOOKUP['ta']]}")
print(f"\nEstimated language: {prediction[3][0][:2]} with probability {prediction[1].exp().item()}")
