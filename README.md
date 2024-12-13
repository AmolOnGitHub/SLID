# Single language tests

[sample files](other/sample.txt)

Samples were randomly selected from VoxLingua107's dev dataset, 5 for each language x 27 languages.

### Measurements taken

Given a clip of language x:

- Accuracy for identification: Model predicts language x this percentage of times.
- Average probability for correct identifications: Model predicts language x with probability p, average of p.
- Average probability for incorrect identifications: Model predicts some other language y, with probability q, average of q.
- Average delta in incorrect identifications: Average of difference between q and probability of x.

## [Whisper](https://github.com/openai/whisper?tab=readme-ov-file)

### Tiny - 1G

```
MODEL: tiny
Model load time: 0.37 seconds.
Average identification time: 0.15 seconds.

Accuracy for identifications: 76.30%.

Average probability for correct identifications: 0.86.
Average probability for incorrect identifications: 0.54.
Average delta in incorrect identifications (between identifed v.s. correct): 0.43.
```

### Base - 1G

```
MODEL: base
Model load time: 0.64 seconds.
Average identification time: 0.30 seconds.

Accuracy for identifications: 80.00%.

Average probability for correct identifications: 0.92.
Average probability for incorrect identifications: 0.52.
Average delta in incorrect identifications (between identifed v.s. correct): 0.41.
```

### Small - 2G

```
MODEL: small
Model load time: 1.67 seconds.
Average identification time: 1.01 seconds.

Accuracy for identifications: 85.19%.

Average probability for correct identifications: 0.93.
Average probability for incorrect identifications: 0.64.
Average delta in incorrect identifications (between identifed v.s. correct): 0.47.
```

### Turbo - 6G

```
MODEL: turbo
Model load time: 17.06 seconds.
Average identification time: 5.43 seconds.

Accuracy for identifications: 91.85%.

Average probability for correct identifications: 0.98.
Average probability for incorrect identifications: 0.64.
Average delta in incorrect identifications (between identifed v.s. correct): 0.50.
```

## [SpeechBrain ECAPA](https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa)

```
Model load time: 3.03 seconds.
Average identification time: 0.11 seconds.

Accuracy for identifications: 91.85%.

Average probability for correct identifications: 0.96.
Average probability for incorrect identifications: 0.73.
Average delta in incorrect identifications (between identifed v.s. correct): 0.63.
```


## Analysis

Clearly, SpeechBrain ECAPA model's accuracy & identification time make it the ideal choice. However, it is quite confident when it makes incorrect decisions. 

Amongst the Whisper models, `Small` offers a good balance between identification time and acccuracy.
`Turbo` matches SpeechBrain's accuracy, but the identification time is very high.

# Mixed language (x-en) tests

[sample files](audio/mixed_sample/)

Samples were interleaved with random english clips from the dev dataset, creating clips with primarily 'x' language, with some portion of english (2:1 ratio, 'x' is any other language - not english). 

[Interleaved sampler code.](other/mixed_sample.py)

Around 5 for each language, 30 languages.

### Measurements taken

Given a clip of language x-en:

- Accuracy for identifications: Model predicts language x this percentage of times.
- Percentage of en identifications: Model predicts language as en this percentage of times.

Other terms are same as [here](#measurements-taken).

## Whisper

### Base

```
MODEL: base
Model load time: 0.67 seconds.
Average identification time: 0.34 seconds.

Accuracy for identifications: 47.97%.
Percentage of en identifications: 36.49%.

Average probability for correct identifications: 0.80.
Average probability for incorrect identifications: 0.62.
Average delta in incorrect identifications (between identifed v.s. correct): 0.53.
```

### Turbo

```
MODEL: turbo
Model load time: 20.97 seconds.
Average identification time: 6.44 seconds.

Accuracy for identifications: 45.95%.
Percentage of en identifications: 52.03%.

Average probability for correct identifications: 0.90.
Average probability for incorrect identifications: 0.89.
Average delta in incorrect identifications (between identifed v.s. correct): 0.83.
```

## SpeechBrain ECAPA

```
Model load time: 3.10 seconds.
Average identification time: 0.44 seconds.
Average audio length: 34.13 seconds.

Accuracy for identifications: 72.97%.
Percentage of en identifications: 10.14%.

Average probability for correct identifications: 0.92.
Average probability for incorrect identifications: 0.59.
Average delta in incorrect identifications (between identifed v.s. correct): 0.49.
```

## Analysis

SpeechBrain's model performs significantly better (on guessing x), with Whisper having a high prediction rate for english.